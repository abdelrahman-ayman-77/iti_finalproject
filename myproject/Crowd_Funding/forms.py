from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Project, Comment, Donation, ProjectPicture, ProjectTag, Rating

    
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name", "email", "phone_number", "picture", "password"]

# CATEGORY_CHOICES = [
#     ("education", "Education"),
#     ("health", "Health"),
#     ("tech", "Tech"),
#     ("arts", "Arts"),
#     ("community", "Community"),
# ]

class ProjectForm(forms.ModelForm):
    # category = forms.ChoiceField(choices=CATEGORY_CHOICES)  # هنا خليتها dropdown جاهزة

    class Meta:
        model = Project
        fields = [
            "title",
            "details",
            "category",
            "target_amount",
            "start_date",
            "end_date",
        ]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
class ProjectPictureForm(forms.ModelForm):
    class Meta:
        model = ProjectPicture
        fields = ["image"]

class ProjectTagForm(forms.Form):
    tags = forms.CharField(
        max_length=255,
        required=False,
        help_text="Enter tags separated by commas",
    )