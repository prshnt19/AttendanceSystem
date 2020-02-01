from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated 
from .serializer import LocationSerializer
from .models import Location
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from geopy.distance import geodesic
from Attendance.models import UserProfile


