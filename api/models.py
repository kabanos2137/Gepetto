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

class UserTokens(models.Model):
    user = models.ForeignKey(UserCredentials, on_delete=models.CASCADE)
    token = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.token}'

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

class ConversationPermissions(models.Model):
    user = models.ForeignKey(UserCredentials, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_view = models.BooleanField(default=False)

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message = models.TextField()
    date_of_creation = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(UserCredentials, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sent_by} on {self.date_of_creation} - ${self.message}'