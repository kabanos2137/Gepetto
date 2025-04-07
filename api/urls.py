from django.urls import path

from .views import user, login, assistant, conversation, message

urlpatterns = [
    path("user", user, name="user"),
    path("login", login, name="login"),
    path("assistant", assistant, name="assistant"),
    path("conversation", conversation, name="conversation"),
    path("message", message, name="message")
]