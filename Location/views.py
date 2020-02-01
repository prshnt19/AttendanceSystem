from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated 
from .serializer import LocationSerializer
from .models import Location
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from geopy.distance import geodesic


class Location(APIView):
    permission_classes = (IsAuthenticated,)
    # def get(self,request):
        
    #     location = Location.objects.all()
    #     serializer = LocationSerializer(location, many=True)
    #     return Response({"location": serializer})
    def post(self,request):
        
        token_number = request.META.get('HTTP_AUTHORIZATION', None).split(' ')[1]
        token = Token.objects.get(key=token_number)
        user = token.user
        longitude = request.data.get('longitude')
        latitude = request.data.get('latitude')

        
        in_range(center_coordinates)
        return Response({'work':'sexy'})

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