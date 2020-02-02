from django.db import models
import uuid
from django.contrib.auth.models import User


class Centers(models.Model):
    name = models.CharField(max_length=15, default=None)
    center_id = models.CharField(
         max_length=5,
         primary_key=True,
         default=str(uuid.uuid4())[31:],
         editable=False)
    voiceit_id = models.CharField(max_length=40, default=None)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    center = models.ForeignKey(Centers, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_office_admin = models.NullBooleanField(default=None)
    voiceit_id = models.CharField(max_length=40, default=None)
    contact_number = models.CharField(max_length=11, default=None)


class AttendanceTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    center = models.ForeignKey(Centers, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    location_verified = models.NullBooleanField(default=None)
    voice_face_verified = models.NullBooleanField(default=None)
    present = models.NullBooleanField(default=None)
    status = models.CharField(max_length=30, default='Not Present', blank=True)


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(upload_to='uploads/'+ str(user.name) +'/' )
