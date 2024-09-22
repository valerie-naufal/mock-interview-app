"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main,name='index'),
    path('create-account/', views.create, name='create-account'),
    path('my-profile/',views.profile, name='my-profile'),
    path('bookings/',views.bookings, name='bookings'),
    path('statistics/',views.statistics, name='statistics'),
    path('host/',views.host, name='host'),
    path('feedback/',views.feedback, name='feedback'),
    path('home/',views.home, name='home'),
    path('host_interview_form/',views.host_interview_form, name='host_interview_form'),
    path('feedback_form/',views.feedback_form,name="feedback_form"),
    path('book/',views.book,name="book"),
    path('logout/',views.logout,name="logout"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)