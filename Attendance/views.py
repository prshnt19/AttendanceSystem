from django.shortcuts import render
from attendance_system.settings import BASE_DIR
import os
from voiceit2 import VoiceIt2
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

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
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
            user = User.objects.create(username=username, password=password, email=email)
        except:
            return Response({'status':'User Name exists'})

        center = Centers.object.get.filter(name=center_name).first()
        user_profile = UserProfile.objects.create(user=user, center=center, is_admin=False)

        return Response({'status':'User Created'})


# usr_6a69dbdcedca4d6ea82c90a9af31b9f5 prashant
# usr_afca986a9db2473d932228735d298957 siddharth
# usr_361ea5aa209047189cc7222ff249a4e5 arpit
# grp_b3f953e210494f5db673bbd520ff79d8 Developer


def voiceit_create_group(request):
    api_key = 'key_66f6eb3dbd0c4d7d85bf9e716b3813f4'
    api_token = 'tok_eff69e97da604bf7a6d13b8ed1400ce9'
    my_voiceit = VoiceIt2(api_key, api_token)
    description = "Developer"
    response = my_voiceit.create_group(description)
    return response['groupId']


def voiceit_create_user(request):
    api_key = 'key_66f6eb3dbd0c4d7d85bf9e716b3813f4'
    api_token = 'tok_eff69e97da604bf7a6d13b8ed1400ce9'
    my_voiceit = VoiceIt2(api_key, api_token)
    response = my_voiceit.create_user()
    response2 = my_voiceit.group_exists('gid')  #
    if response2['exists']:
        my_voiceit.add_user_to_group("grp_b3f953e210494f5db673bbd520ff79d8", response['userId'])
        return [True, response['userId']]
    else:
        return [False, response['userId']]


def voiceit_enroll_user(request):
    api_key = 'key_66f6eb3dbd0c4d7d85bf9e716b3813f4'
    api_token = 'tok_eff69e97da604bf7a6d13b8ed1400ce9'
    my_voiceit = VoiceIt2(api_key, api_token)
    user_id = 'usr_afca986a9db2473d932228735d298957'  #
    content_language = 'en-US'
    phrase = 'my face and voice identify me'
    video = open('siddharth1.mp4', 'rb')
    response = my_voiceit.create_video_enrollment(user_id=user_id, lang=content_language, phrase=phrase,
                                                  file_buffer=video)
    return response['responseCode']


def voiceit_identification(request):
    api_key = 'key_66f6eb3dbd0c4d7d85bf9e716b3813f4'
    api_token = 'tok_eff69e97da604bf7a6d13b8ed1400ce9'
    my_voiceit = VoiceIt2(api_key, api_token)
    group_id = 'gid'  #
    content_language = 'en-US'
    phrase = 'my face and voice identify me'
    video = open('siddharth1.mp4', 'rb')
    response = my_voiceit.voice_identification(group_id=group_id, lang=content_language, phrase=phrase,
                                               file_buffer=video)
    if response['responseCode'] == 'SUCC':
        return [True, response['user_id']]
    else:
        return [False, response['message']]


def voiceit_verification(request):
    api_key = 'key_66f6eb3dbd0c4d7d85bf9e716b3813f4'
    api_token = 'tok_eff69e97da604bf7a6d13b8ed1400ce9'
    my_voiceit = VoiceIt2(api_key, api_token)
    user_id = 'usr'  #
    content_language = 'en-US'
    phrase = 'my face and voice identify me'
    video = open('siddharth1.mp4', 'rb')
    response = my_voiceit.video_verification(user_id=user_id, lang=content_language, phrase=phrase,
                                             file_buffer=video)
    if response['responseCode'] == 'SUCC':
        return [True, response['message']]
    else:
        return [False, response['message']]


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
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
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

