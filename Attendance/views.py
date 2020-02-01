from django.shortcuts import render
from attendance_system.settings import BASE_DIR
import os
from voiceit2 import VoiceIt2
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

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
