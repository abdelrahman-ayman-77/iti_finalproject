from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Project, Comment, Donation, Rating

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name", "email", "phone_number", "picture", "password"]