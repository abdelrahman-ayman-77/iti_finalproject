"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Crowd_Funding.urls')),
]


if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # اكتب شرح هنا
    # الكود ده بيخلي السيرفر بتاع Django يقدر يخدم ملفات الميديا (زي الصور والفيديوهات) لما تكون في وضع التطوير (DEBUG=True)
    # لما تبقى في وضع الإنتاج (DEBUG=False)، لازم تستخدم سيرفر ويب زي Nginx أو Apache عشان يخدم ملفات الميديا دي.
    # الكود ده بيضيف URL patterns جديدة بتخلي Django يقدر يلاقي ملفات الميديا في المجلد اللي انت محدده في MEDIA_ROOT لما حد يطلبها من خلال MEDIA_URL.       