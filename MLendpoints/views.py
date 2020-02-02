from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated 
# from .serializer import LocationSerializer
from django.contrib.auth.models import User
from voiceit2 import VoiceIt2
from Attendance.models import UserProfile, AttendanceTable
import datetime
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from attendance_system.settings import BASE_DIR, api_key, api_token
import uuid
import os
from voiceit2 import VoiceIt2
from geopy.distance import geodesic
from math import radians, sin, cos, acos


# usr_6a69dbdcedca4d6ea82c90a9af31b9f5 prashant
# usr_afca986a9db2473d932228735d298957 siddharth
# usr_361ea5aa209047189cc7222ff249a4e5 arpit
# grp_b3f953e210494f5db673bbd520ff79d8 Developer


def voiceit_create_group(request):
    my_voiceit = VoiceIt2(api_key, api_token)
    description = "Developer"
    response = my_voiceit.create_group(description)
    return response['groupId']


def voiceit_create_user(group_id, user):
    my_voiceit = VoiceIt2(api_key, api_token)
    response = my_voiceit.create_user()
    os.mkdir(os.path.join(BASE_DIR, 'test', str(user.id)))
    response2 = my_voiceit.group_exists(group_id)  #
    if response2['exists']:
        my_voiceit.add_user_to_group(group_id, response['userId'])
        return [True, response['userId']]
    else:
        return [False, response['userId']]


def voiceit_enroll_user(user_id, file_path, phrase):
    my_voiceit = VoiceIt2(api_key, api_token)
    # user_id = 'usr_afca986a9db2473d932228735d298957'  #
    content_language = 'en-US'
    video = open(file_path, 'rb')
    response = my_voiceit.create_video_enrollment(user_id=user_id, lang=content_language, phrase=phrase,
                                                  file_buffer=video)
    return response['responseCode']


def voiceit_identification(request):
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


def voiceit_verification(user_id, file_path, phrase):
    my_voiceit = VoiceIt2(api_key, api_token) #
    content_language = 'en-US'
    video = open(file_path, 'rb')
    response = my_voiceit.video_verification(user_id=user_id, lang=content_language, phrase=phrase,
                                             file_buffer=video)
    if response['responseCode'] == 'SUCC':
        return [True, response['message']]
    else:
        return [False, response['message']]

class TrainVideo(APIView):
    permission_classes = (AllowAny,)
    # def get(self,request):

    #     location = Location.objects.all()
    #     serializer = LocationSerializer(location, many=True)
    #     return Response({"location": serializer})
    def post(self,request,format=None):
        token_number = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
        token = Token.objects.get(key=token_number)
        print(token_number)
        user = token.user
        print(user)

        file_name = upload(request.data['video'], user.id)

        phrase = 'my face and voice identify me'
        userprofile = UserProfile.objects.filter(user=user).first()
        print(userprofile)
        voiceit_enroll_user(userprofile.voiceit_id, file_name, phrase)

        return Response({'status':'sent'})

def upload(file, user_id):
    file_name = BASE_DIR + '/test/' + str(user_id) + '/' + str(user_id) + '__' + str(uuid.uuid4())[:3] + '.mp4'
    with open(file_name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    print(file_name)
    return file_name
    # if request.is_secure():
    #     protocol = 'https://'
    # else:
    #     protocol = 'http://'
    # return file_name
    # target_path = protocol + '127.0.0.1:8000/static/' + user_id

class TestVideo(APIView):
    permission_classes = (AllowAny,)
    # def get(self,request):
        
    #     location = Location.objects.all()
    #     serializer = LocationSerializer(location, many=True)
    #     return Response({"location": serializer})
    def post(self,request,format=None ):
        token_number = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
        token = Token.objects.get(key=token_number)
        user = token.user

        file_name = upload(request.data['video'], user.id)

        longitude = float(request.data.get('longitude'))
        latitude = float(request.data.get('latitude'))
        user_coordinates = (latitude, longitude)

        phrase = 'my face and voice identify me'
        userprofile = UserProfile.objects.filter(user=user).first()

        center = userprofile.center
        center_coordinates = (center.latitude, center.longitude)
        location_verified = in_range(center_coordinates, user_coordinates)

        attendancetable = AttendanceTable.objects.create(user=user, center=center)
        if location_verified is True:
            attendancetable.location_verified = True
            attendancetable.save()
        else:
            attendancetable.location_verified = False
            attendancetable.save() 
        res = voiceit_verification(userprofile.voiceit_id, file_name, phrase)
        
        if res[0] is True:
            attendancetable.voice_face_verified = True
            attendancetable.save()
        else:
            attendancetable.voice_face_verified = False
            attendancetable.save()
        if attendancetable.location_verified is True and attendancetable.voice_face_verified is True:
            attendancetable.present = True
            date_time = datetime.datetime.now()
            if (attendancetable.date < datetime.datetime(date_time.year, date_time.month, date_time.day) +
                                                    datetime.timedelta(hours=10)):
                attendancetable.status = 'On Time'
            else:
                attendancetable.status = 'Late'
            return Response({'video': 'verified', 'location': 'verified', 'response': res[1]})
        elif attendancetable.location_verified is True:
            attendancetable.status = 'Video Authentication Failed'
            return Response({'video': 'not_verified', 'location': 'verified', 'response': res[1]})
        elif attendancetable.voice_face_verified is True:
            attendancetable.status = 'Location Authentication Failed'
            return Response({'video': 'verified', 'location': 'not_verified', 'response': res[1]})
        else:
            return Response({'video': 'not_verified', 'location': 'not_verified', 'response': res[1]})



def in_range(center_coordinates, user_coordiantes):
    '''
    >>> from geopy.distance import geodesic
    >>> newport_ri = (41.49008, -71.312796)
    >>> cleveland_oh = (41.499498, -81.695391)
    >>> print(geodesic(newport_ri, cleveland_oh).miles)
    538.390445368
    '''
    distance = geodesic(center_coordinates, user_coordiantes).meters
    print(center_coordinates, user_coordiantes, distance)
    if distance < 30:
        return True
    else:
        return False
    # approximate radius of earth in km
    # R = 6373.0

    # lat1 = radians(52.2296756)
    # lon1 = radians(21.0122287)
    # lat2 = radians(52.406374)
    # lon2 = radians(16.9251681)

    # dlon = lon2 - lon1
    # dlat = lat2 - lat1

    # a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    # c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # distance = R * c/1000
# class test1(APIView):
#     # def get(self,request):
        
#     #     location = Location.objects.all()
#     #     serializer = LocationSerializer(location, many=True)
#     #     return Response({"location": serializer})
#     #    parser_classes = (MultiPartParser,)
#     permission_classes = (AllowAny,)
#     def post(self,request,format=None):
#         token_number = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
#         token = Token.objects.get(key=token_number)
#         user = token.user
#         print(user)
#         upload(request.data['video'], user.id)
#         file_obj = 1
#         print(file_obj)
#         return Response({'work':'sex'})
