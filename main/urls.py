from django.urls import path
from .views import index, create_acc, create_acc_success

urlpatterns = [
    path('', index, name='index'),
    path('create-acc', create_acc, name='create-acc'),
    path('create-acc-success', create_acc_success, name='create-acc-success'),
]