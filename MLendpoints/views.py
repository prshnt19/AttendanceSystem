from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from attendance_system.settings import BASE_DIR
import uuid
import os

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


def voiceit_create_user(group_id):
    api_key = 'key_66f6eb3dbd0c4d7d85bf9e716b3813f4'
    api_token = 'tok_eff69e97da604bf7a6d13b8ed1400ce9'
    my_voiceit = VoiceIt2(api_key, api_token)
    response = my_voiceit.create_user()
    os.mkdir(os.path.join(BASE_DIR, 'test', response['user_id']))
    response2 = my_voiceit.group_exists(group_id)  #
    if response2['exists']:
        my_voiceit.add_user_to_group(group_id, response['userId'])
        return [True, response['userId']]
    else:
        return [False, response['userId']]


def voiceit_enroll_user(user_id, file_path, phrase):
    api_key = 'key_66f6eb3dbd0c4d7d85bf9e716b3813f4'
    api_token = 'tok_eff69e97da604bf7a6d13b8ed1400ce9'
    my_voiceit = VoiceIt2(api_key, api_token)
    # user_id = 'usr_afca986a9db2473d932228735d298957'  #
    content_language = 'en-US'
    video = open(file_path, 'rb')
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

class TrainVideo(APIView):
    permission_classes = (IsAuthenticated,)
    # def get(self,request):
        
    #     location = Location.objects.all()
    #     serializer = LocationSerializer(location, many=True)
    #     return Response({"location": serializer})
    def post(self,request):
        token_number = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
        token = Token.objects.get(key=token_number)
        user = token.user

        file_name = upload(request.data['video'], user.id)
        
        phrase = 'my face and voice identify me'
        userprofile = UserProfile.objects.filter(user=user).first()
        voiceit_enroll_user(userprofile.voice_it, file_name, phrase)
        
        return Response({'work':'sexy'})

def upload(file, user_id):
    file_name = BASE_DIR + '/test/' + str(user_id) + '/' + str(user_id) + '__' + str(uuid.uuid4)[:3] + '.mp4'
    with open(file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_name        
    # if request.is_secure():
    #     protocol = 'https://'
    # else:
    #     protocol = 'http://'
    # return file_name
    # target_path = protocol + '127.0.0.1:8000/static/' + user_id


class test1(APIView):
    # def get(self,request):
        
    #     location = Location.objects.all()
    #     serializer = LocationSerializer(location, many=True)
    #     return Response({"location": serializer})
#    parser_classes = (MultiPartParser,)
    permission_classes = (AllowAny,)
    def post(self,request,format=None):
        token_number = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
        token = Token.objects.get(key=token_number)
        user = token.user
        upload(request.data['video'], user.id)
        file_obj = 1
        print(file_obj)
        return Response({'work':'sex'})