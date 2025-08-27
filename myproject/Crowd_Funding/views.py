from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


# Create your views here.


def home(request):
    return render(request,'pages/pro.html')

def login_view(request):
    return render(request,'pages/login.html')
def register(request):
    return render(request,'pages/register.html')