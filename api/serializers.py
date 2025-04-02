from .models import UserCredentials
from rest_framework import serializers

class UserCredentialsSerializer(serializers.ModelSerializer): # Serializer for UserCredentials model
    class Meta: # Serializer class
        model = UserCredentials # Model to be serialized
        fields = ['id', 'name', 'email', 'password'] # Fields to be serialized