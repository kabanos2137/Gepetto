from django.urls import path
from .views import user, login

urlpatterns = [
    path("user", user, name="user"),
    path("login", login, name="login"),
]