from django.urls import path
from .views import registeradmin, dashboard
from django.contrib.auth.decorators import login_required

app_name = 'attendance'

urlpatterns = [
    path("register/", registeradmin, name = "registeradmin"),

    path("dashboard/", dashboard, name="dashboard"),
]