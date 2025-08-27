from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import CustomUserForm
from .models import Project


# Create your views here.


def home(request):
    return render(request,'pages/pro.html')

def login_view(request):
    return render(request,'pages/login.html')
def register(request):
    error_message = None
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES)
        confirm_password = request.POST.get("confirm_password") 
        if form.is_valid():
            password = form.cleaned_data.get("password")
            if password != confirm_password:
                error_message = "Passwords do not match!"
            else:
                user = form.save(commit=False)
                user.set_password(password)
                user.save()
                return redirect("login")  
        else:
            error_message = "Please correct the errors below."
    else:
        form = CustomUserForm()

    return render(
        request, 
        "pages/register.html", 
        {"form": form, "error_message": error_message}
    )
