from django.urls import path
from .views import index, create_acc

urlpatterns = [
    path('', index, name='index'),
    path('create-acc', create_acc, name='create-acc'),
]