from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"), 
    path("register/", views.register, name="register"),  
    path('logout/', views.logout_view, name='logout'),
    path("profile/", views.profile_view, name="profile"),
    path("addproject/", views.add_project, name="addproject"),
    path("project_detail/<int:project_id>/", views.project_detail, name="project_detail"),
    path("project/<int:project_id>/donate/", views.donate, name="donate"),
    path("project/<int:project_id>/comment/", views.add_comment, name="add_comment"),
    path("project/<int:project_id>/rate/", views.rate_project, name="rate_project"),
    path("project/<int:project_id>/cancel/", views.cancel_project, name="cancel_project"),
    path("projects/", views.project_list, name="project_list"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)