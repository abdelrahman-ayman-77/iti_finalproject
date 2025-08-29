from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import CustomUserForm, ProjectForm ,ProjectPictureForm ,ProjectTagForm
from .models import CommentReport, Donation, Project, ProjectPicture, ProjectReport, ProjectTag ,Comment, Rating
from django.db.models import Avg
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import Project, Category

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
def add_project(request):
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        picture_form = ProjectPictureForm(request.POST, request.FILES)
        tag_form = ProjectTagForm(request.POST)
        if project_form.is_valid() and picture_form.is_valid() and tag_form.is_valid():
            project = project_form.save(commit=False)
            project.creator = request.user  
            project.save()

            picture = picture_form.save(commit=False)
            picture.project = project
            picture.save()

            tags_str = tag_form.cleaned_data["tags"]
            tags = [t.strip() for t in tags_str.split(",") if t.strip()]
            for tag in tags:
                ProjectTag.objects.create(project=project, tag=tag)

            return redirect("home")  
    else:
        project_form = ProjectForm()
        picture_form = ProjectPictureForm()
        tag_form = ProjectTagForm()

    return render(request, "pages/Createproject.html", {
        "project_form": project_form,
        "picture_form": picture_form,
        "tag_form": tag_form,
    })

@login_required
def profile_view(request):
    user = request.user
    return render(request, "pages/profile.html", {"user": user})




@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    comments = project.comments.all()
    donations = project.donations.all()
    
    if (project.total_donations()>=project.target_amount) or (project.end_date < timezone.now()):
        project.status="completed"
        project.save()
        
    # تقييم المستخدم الحالي (لو موجود)
    user_rating = Rating.objects.filter(project=project, user=request.user).first()
    user_rating_value = user_rating.rating if user_rating else 0
    
    # متوسط التقييمات
    avg_rating = project.ratings.aggregate(avg=Avg("rating"))["avg"]
    
    # لازم نمررهم للـ template
    return render(request, "pages/project_detail.html", {
        "project": project,
        "comments": comments,
        "donations": donations,
        "user_rating": user_rating_value,
        "avg_rating": avg_rating,
    })

@login_required
def donate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount:
            Donation.objects.create(
                project=project,
                user=request.user,
                amount=amount
            )
    return redirect("project_detail", project_id=project.id)

@login_required
def add_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(
                project=project,
                user=request.user,
                content=content
            )
    return redirect("project_detail", project_id=project.id)


@login_required
def rate_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        rating_value = request.POST.get("rating")
        if rating_value:
            rating_obj, created = Rating.objects.update_or_create(
                project=project,
                user=request.user,
                defaults={"rating": rating_value}
            )
    return redirect("project_detail", project_id=project.id)



def cancel_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = "cancelled"
    project.save()
    return redirect("project_detail", project_id=project_id)

def project_list(request):
    query = request.GET.get("q")  # search by name
    category_id = request.GET.get("category")  # filter by category

    projects = Project.objects.all()

    if query:
        projects = projects.filter(title__icontains=query)

    if category_id:
        projects = projects.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, "pages/project_list.html", {
        "projects": projects,
        "categories": categories,
        "selected_category": category_id,
        "query": query,
    })

@login_required
def report_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        description = request.POST.get("description")
        if description.strip():  # make sure it's not empty
            ProjectReport.objects.create(
                reporter=request.user,
                project=project,
                description=description,
            )
            messages.success(request, "Your report has been submitted.")
            return redirect("project_detail", project_id=project.id)
        else:
            messages.error(request, "Description is required.")

    return render(request, "report_project.html", {"project": project})

def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("home")  # change to your home page
    return redirect("profile", user_id=request.user.id)

