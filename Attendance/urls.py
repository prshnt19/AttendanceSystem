from django.urls import path
from .views import registeradmin, dashboard

app_name = 'attendance'

urlpatterns = [
    path("register/", registeradmin, name = "registeradmin"),

    path("", registeradmin, name="registeradmin"),
    path("dashboard/", dashboard, name="dashboard"),
    # path("upload/", upload, name="upload"),
]