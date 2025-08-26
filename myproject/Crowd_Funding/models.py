from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================================================
# 🧑‍💻 Custom User Model (أساسي)
# =========================================================
class CustomUser(AbstractUser):
    """
    المستخدم المخصص (بدل User العادي)
    الحقول الأساسية: اسم، إيميل، باسورد، رقم موبايل، صورة شخصية
    """
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # رقم الموبايل 
    picture = models.ImageField(upload_to='user_pics/', blank=True, null=True)  # صورة البروفايل

    def __str__(self):
        return self.username


# ---------------------------------------------------------
# 📂 Categories (تصنيفات المشاريع)
# ---------------------------------------------------------
class Category(models.Model):
    """
    التصنيفات اللي بيضيفها الأدمن (مثلاً: تعليم، صحة، بيئة)
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------
# 📢 Projects (المشاريع الأساسية)
# ---------------------------------------------------------
class Project(models.Model):
    """
    المشروع الأساسي (الحملة) اللي بيعملها المستخدم
    """
    STATUS_CHOICES = [
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    #on_delete 
    #لو حذفنا المستخدم كل المشاريع المتعلقه بيه هتتحذف
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="projects")

    title = models.CharField(max_length=255)
    
    details = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)  # الهدف المالي

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True)

    featured = models.BooleanField(default=False)  # المشاريع المميزة من الأدمن

    def __str__(self):
        return self.title


# ---------------------------------------------------------
# 🖼️ Project Pictures (صورة واحدة على الأقل لكل مشروع)
# ---------------------------------------------------------
class ProjectPicture(models.Model):
    """
    صور المشروع (ممكن صورة واحدة كبداية)
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="pictures")
    image = models.ImageField(upload_to="project_pics/")

    def __str__(self):
        return f"Picture for {self.project.title}"


# ---------------------------------------------------------
# 🏷️ Project Tags (Tags أساسية للبحث)
# ---------------------------------------------------------
class ProjectTag(models.Model):
    """
        (Tags) للمشاريع للبحث
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tags")
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag


# ---------------------------------------------------------
# 💰 Donations (التبرعات الأساسية)
# ---------------------------------------------------------
class Donation(models.Model):
    """
    التبرعات اللي بيعملها المستخدمين للمشاريع
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="donations")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} donated {self.amount} to {self.project.title}"


# ---------------------------------------------------------
# 💬 Comments (تعليقات أساسية بدون ردود)
# ---------------------------------------------------------
class Comment(models.Model):
    """
    التعليقات على المشاريع (بدون Replies الآن)
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.title}"


# ---------------------------------------------------------
# ⭐ Ratings (التقييم الأساسي)
# ---------------------------------------------------------
class Rating(models.Model):
    """
    تقييم المشاريع (1 إلى 5 نجوم)
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveSmallIntegerField()  # 1–5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")  # مستخدم واحد يقيم المشروع مرة واحدة فقط

    def __str__(self):
        return f"{self.rating} stars by {self.user.username} on {self.project.title}"
