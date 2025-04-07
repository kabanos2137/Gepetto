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

class Assistant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    response_style = models.TextField()
    tone = models.TextField()
    profile_picture = models.TextField()

class AssistantPermissions(models.Model):
    user = models.ForeignKey(UserCredentials, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)

class Conversation(models.Model):
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_creation = models.DateTimeField(auto_now_add=True)

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message = models.JSONField() # [{ type: text, message: string }, { type: image, message: string }] etc.
    date_of_creation = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(UserCredentials, on_delete=models.CASCADE)