from django.contrib import admin
from .models import UserProfile, Centers, Video, AttendanceTable

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Centers)
admin.site.register(Video)
admin.site.register(AttendanceTable)