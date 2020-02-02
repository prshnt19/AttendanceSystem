from django.urls import path
from .views import registeradmin, dashboard, statistics

app_name = 'attendance'

urlpatterns = [
    path("register/", registeradmin, name = "registeradmin"),

    # path("", registeradmin, name="registeradmin"),
    path("dashboard/", dashboard, name="dashboard"),
    path("statistics/", statistics, name="statistics"),
    # path("upload/", upload, name="upload"),
]