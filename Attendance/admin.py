from django.contrib import admin
from .models import UserProfile, Centers, Video, AttendanceTable


class UserProfileEntry(admin.ModelAdmin):
    list_display = ("user", "center", "voiceit_id", "contact_number")


class AttendanceTableEntry(admin.ModelAdmin):
    list_display = ("user", "center", "date", "location_verified", "voice_face_verified", "present")


class CenterEntry(admin.ModelAdmin):
    list_display = ("name", "center_id", "voiceit_id", "latitude", "longitude")


class VideoEntry(admin.ModelAdmin):
    list_display = ("user", "video")


admin.site.register(AttendanceTable, AttendanceTableEntry)
admin.site.register(Centers, CenterEntry)
admin.site.register(Video, VideoEntry)
admin.site.register(UserProfile, UserProfileEntry)
