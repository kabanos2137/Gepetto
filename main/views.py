from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def create_acc(request):
    return render(request, "main/create-acc.html")

def create_acc_success(request):
    return render(request, "main/create-acc-success.html")

def app(request):
    return render(request, "main/app.html")

def create_assistant(request):
    return render(request, "main/create-assistant.html")

def assistant(request):
    return render(request, "main/assistant.html")

def conversation(request):
    return render(request, "main/conversation.html")

def m_app(request):
    return render(request, "main/m-app.html")