from django.urls import path
from .views import index, create_acc, create_acc_success, app, m_app, create_assistant, assistant, conversation

urlpatterns = [
    path('', index, name='index'),
    path('create-acc', create_acc, name='create-acc'),
    path('create-acc-success', create_acc_success, name='create-acc-success'),
    path('app', app, name='app'),
    path("create-assistant", create_assistant, name="create-assistant"),
    path("assistant", assistant, name="assistant"),
    path("conversation", conversation, name="conversation"),
    path('m-app', m_app, name='m-app'),
]