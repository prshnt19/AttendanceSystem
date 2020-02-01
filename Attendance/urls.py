from django.urls import path
from .views import registeradmin, dashboard

app_name = 'attendance'

urlpatterns = [
    path("", registeradmin, name = "registeradmin"),
    path("dashboard/", dashboard, name="dashboard"),
]