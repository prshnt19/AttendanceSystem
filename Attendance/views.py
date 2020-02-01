from django.shortcuts import render
from attendance_system.settings import BASE_DIR
import os
from voiceit2 import VoiceIt2
from django.contrib.auth.models import User
from .models import UserProfile, Centers
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
from geopy.distance import geodesic
from MLendpoints.views import voiceit_create_user

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
        try:
            center = Centers.objects.filter(name=center_name).first()
        except:
            return  Response({'status':'Center Does not exist'})
        try:
            user = User.objects.create(username=username, password=password, email=email)
        except:
            return Response({'status':'User Name already exists'})
        
        return Response({'status':'User Created'})

def upload(request):
    user_id = request.POST('user_id')
    file = request.FILES['file']
    file_name = BASE_DIR + '/Attendance/' + user_id
    with open(file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    # target_path = protocol + '127.0.0.1:8000/static/' + user_id

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
                print(1)
                try:
                    center = Centers.objects.filter(name=center_name, center_id=center_token).first()
                except:
                    return forms.ValidationError('Center token or name Invalid')

                user_created = User.objects.create_user(username, email, password, first_name=first_name,
                                                        last_name=last_name)
                voiceit_id = voiceit_create_user(center_token)
                UserProfile.objects.create(user=user_created, center=center, is_office_admin=True, mobile=contact_number, voiceit_id=voiceit_id)
                print(2)
                user = authenticate(username=username, password=password)
                login(request, user)
                print(3)
                return HttpResponseRedirect('dashboard/')

            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form' : form})


def dashboard(request):
    return render(request, 'index.html')


def in_range():
    '''
    >>> from geopy.distance import geodesic
    >>> newport_ri = (41.49008, -71.312796)
    >>> cleveland_oh = (41.499498, -81.695391)
    >>> print(geodesic(newport_ri, cleveland_oh).miles)
    538.390445368
    '''
    centre_coordinates = (41.499498, -81.695356)
    user_coordiantes = (41.499498, -81.695391)
    distance = geodesic(centre_coordinates, user_coordiantes).meters
    print(distance)
    if distance < 30:
        return True
    else:
        return False

