import os

from django.urls import path
from dotenv import load_dotenv

from .views import user, login
from openai import AzureOpenAI

load_dotenv("./.confidential.env")

client = AzureOpenAI(
    azure_endpoint=os.getenv('OPENAI_API_BASE'),
    api_key=os.getenv('OPENAI_API_KEY'),
    api_version="2024-05-01-preview",
)

urlpatterns = [
    path("user", user, name="user"),
    path("login", login, name="login"),
]