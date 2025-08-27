from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import CustomUserForm ########
from .models import Project

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request,'pages/pro.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None

        if username:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {user.username} 👋")
                return redirect("home")
        
        messages.error(request, "Invalid email or password!")

    return render(request, "pages/login.html")








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



def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    return HttpResponse(f"مرحبا {request.user.username}! دي صفحة البروفايل بتاعتك.")
