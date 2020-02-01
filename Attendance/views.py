from django.shortcuts import render
from attendance_system.settings import BASE_DIR
import datetime
import os
from voiceit2 import VoiceIt2
from django.contrib.auth.models import User
from .models import UserProfile, Centers, AttendanceTable
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import redirect
from MLendpoints.views import voiceit_create_user
from django.contrib.auth.decorators import login_required

#kind of login returns jwt token and stuff
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # userprofile = UserProfile.objects.get(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class register(APIView):

    def post(self,request):

        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        center_name = request.data.get('center_name')
        contact_number = request.data.get('contact')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        print(password)

        try:
            center = Centers.objects.filter(name=str(center_name)).first()
        except:
            return  Response({'status':'Center Does not exist'})
        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,last_name=last_name)
        except:
            return Response({'status':'User Name already exists'})

        token, created = Token.objects.get_or_create(user=user)

        res = voiceit_create_user(center.voiceit_id, user)
        user_profile_voice_it = res[1]

        user_profile = UserProfile.objects.create(user=user, center=center, is_office_admin=False, voiceit_id=user_profile_voice_it, contact_number=contact_number)
        return Response({'status':'User Created', 'token': token.key, 'user_name': user.username})


def registeradmin(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            center_token = userObj['centre_id']
            contact_number = userObj['contact']
            center_name = userObj['centre_name']
            first_name = userObj['first_name']
            last_name = userObj['last_name']

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                user_created = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                try:
                    center = Centers.objects.filter(name=center_name, center_id=center_token).first()
                except:
                    return forms.ValidationError('Center token or name Invalid')

                user_created = User.objects.create_user(username, email, password, first_name=first_name,
                                                        last_name=last_name)
                voiceit_id = voiceit_create_user(center_token)
                UserProfile.objects.create(user=user_created, center=center, is_office_admin=True, contact_number=contact_number, voiceit_id=voiceit_id)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('dashboard/')

            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form' : form})


@login_required(login_url='login')
def dashboard(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    print(request.user)
    center = user_profile.center
    employee_count = Centers.objects.filter(id=center.id).count()
    print(employee_count)
    employee_present = AttendanceTable.objects.filter(center=center.id, date=datetime.date.today()).count()
    print(employee_present)
    context = dict()
    return render(request, 'index.html', context)




