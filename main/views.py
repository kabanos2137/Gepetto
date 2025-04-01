from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def create_acc(request):
    return render(request, "main/create-acc.html")