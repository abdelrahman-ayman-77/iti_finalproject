from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

egypt_phone_validator = RegexValidator(
    regex=r"^01[0,1,2,5]\d{8}$",
    message="Enter a valid Egyptian phone number (e.g. 01012345678)."
)

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20,validators=[egypt_phone_validator],blank=True, null=True)  
    picture = models.ImageField(upload_to='user_pics/', blank=True, null=True)

    def __str__(self):
        return self.username



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):

    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="projects")

    title = models.CharField(max_length=255)
    
    details = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)  # الهدف المالي

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True)

    featured = models.BooleanField(default=False)  



class ProjectPicture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="pictures")
    image = models.ImageField(upload_to="project_pics/")

   

class ProjectTag(models.Model):
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tags")
    tag = models.CharField(max_length=50)


class Donation(models.Model):
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="donations")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveSmallIntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)

