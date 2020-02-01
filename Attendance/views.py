from django.shortcuts import render
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
            center = Centers.object.get.filter(name=center_name).first()
        except:
            return  Response({'status':'Center Does not exist'})
        try:
            user = User.objects.create(username=username, password=password, email=email)
        except:
            return Response({'status':'User Name already exists'})
        
        return Response({'status':'User Created'})


def registeradmin(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            center_token = userObj['']
            contact_number = userObj['']
            center_name = userObj['']
            first_name = userObj['']
            last_name = userObj['']

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                user_created = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
                try:
                    center = Centers.objects.filter(name=center_name, center_id=center_token)
                except:
                    return forms.ValidationError('Center token or name Invalid')
                    
                UserProfile.objects.create(user=user_created, center = center, is_office_admin = True)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form' : form})
