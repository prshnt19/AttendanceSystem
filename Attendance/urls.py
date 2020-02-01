from django.urls import path
from .views import registeradmin, dashboard, upload

app_name = 'attendance'

urlpatterns = [
    path("", registeradmin, name="registeradmin"),
    path("dashboard/", dashboard, name="dashboard"),
    # path("upload/", upload, name="upload"),
]