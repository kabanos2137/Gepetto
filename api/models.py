from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your models here.
class UserCredentials(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name