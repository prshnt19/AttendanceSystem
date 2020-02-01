from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated 
from .serializer import LocationSerializer
from .models import Location
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


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

        

        return Response({'work':'sexy'})

