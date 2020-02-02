from django.shortcuts import render
from django.utils.translation import gettext as _
from attendance_system.settings import BASE_DIR, TIME_ZONE
import datetime
from django.utils.timezone import make_aware
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
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import redirect
from MLendpoints.views import voiceit_create_user
from django.contrib.auth.decorators import login_required


# kind of login returns jwt token and stuff
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # prashant edited arpit
        userprofile = UserProfile.objects.get(user=user)
        token, created = Token.objects.get_or_create(user=user)

        center = userprofile.center
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'center_id': center.pk
        })


class register(APIView):

    def post(self, request):

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
            return Response({'status': 'Center Does not exist'})
        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                            last_name=last_name)
        except:
            return Response({'status': 'User Name already exists'})

        token, created = Token.objects.get_or_create(user=user)

        res = voiceit_create_user(center.voiceit_id, user)
        user_profile_voice_it = res[1]

        user_profile = UserProfile.objects.create(user=user, center=center, is_office_admin=False,
                                                  voiceit_id=user_profile_voice_it, contact_number=contact_number)
        return Response({'status': 'User Created', 'token': token.key, 'user_name': user.username})


def registeradmin(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            center_token = userObj['centre_id']
            contact_number = userObj['contact']
            center_name = userObj['centre_name']
            first_name = userObj['first_name']
            last_name = userObj['last_name']

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                try:
                    # print(center_name, center_token)
                    center = Centers.objects.filter(name=center_name, voiceit_id=center_token).first()
                    # print(center)
                    # print(center.pk)
                except:
                    # return forms.ValidationError(_('Center token or name Invalid'), code='invalid')
                    return HttpResponse('Center token or name Invalid')
                user_created = User.objects.create_user(username, email, password, first_name=first_name,
                                                        last_name=last_name)
                print("1")
                voiceit_id = voiceit_create_user(center_token, user_created)
                UserProfile.objects.create(user=user_created, center=center, is_office_admin=True,
                                           contact_number=contact_number, voiceit_id=voiceit_id[1])

                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/dashboard/')

            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def dashboard(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    print(request.user)
    center = user_profile.center
    employees = UserProfile.objects.filter(center=center).values('user', 'user__first_name', 'user__last_name')
    print('employees:', employees)
    count_employee = employees.count()
    print(count_employee)
    date_time = datetime.datetime.now()
    # TIME_ZONE
    # aware_datetime = make_aware(date_time)
    # aware_datetime.tzinfo
    count_present = AttendanceTable.objects.filter(center=center, date__gte=date_time.date(),
                                                   date__lt=date_time.date() + datetime.timedelta(days=1)).count()
    print('count_present:', count_present)
    late = AttendanceTable.objects.filter(center=center,
                                          date__gte=datetime.datetime(date_time.year, date_time.month, date_time.day) +
                                                    datetime.timedelta(hours=9)).values('user_id')
    all_present = AttendanceTable.objects.filter(center=center,
                                          date__gte=datetime.datetime(date_time.year, date_time.month, date_time.day) +
                                                    datetime.timedelta(hours=0)).values('user_id')
    # timestamp = AttendanceTable.objects.filter(center=center, date__gte=date_time.date(),
    #                                                date__lt=date_time.date() + datetime.timedelta(days=1)).values('datetime')
    # print(timestamp,"-->timestamp")
    count_late = late.count()
    print('late:', late)
    print('count_late:', count_late)

    for employee in employees:
        employee['status'] = 'Absent'

        for on_timer in all_present:
            if employee['user'] == on_timer['user_id']:
                employee['status'] = 'On Time'

        for late_comer in late:
            if employee['user'] == late_comer['user_id']:
                employee['status'] = 'Late'



    print('employees:', employees)
    context = {'count_employee': count_employee, 'count_present': count_present, 'count_late': count_late,
               'employees': employees, 'yet_to_come': count_employee-count_present}
    return render(request, 'index.html', context)


def statistics(request):
    return render(request, "charts-chartjs.html")