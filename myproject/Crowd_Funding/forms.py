from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Project, Comment, Donation, ProjectPicture, ProjectTag, Rating

    
class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name", "email", "phone_number", "picture", "password"]



class ProjectForm(forms.ModelForm):

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



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email',
                  'picture', 'phone_number', 'birthdate',
                  'facebook_profile', 'country']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'readonly': True}),  # هنا هنخليه للعرض فقط
        }