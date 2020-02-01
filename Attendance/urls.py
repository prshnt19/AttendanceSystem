from django.urls import path
from .views import registeradmin


urlpatterns = [
    path("", registeradmin, name = "registeradmin"),
]