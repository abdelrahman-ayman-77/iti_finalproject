from django.shortcuts import render
from django.http import HttpResponse
from .models import Project


# Create your views here.


def home(request):
    return HttpResponse("Welcome to the Crowd Funding Platform 🚀")