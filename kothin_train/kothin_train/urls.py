"""
URL configuration for kothin_train project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import rs.views as rs_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',rs_views.homepage,name= 'home'),
    path('registration',rs_views.registration,name= 'register'),
    path('login',rs_views.login,name= 'login'),
    path('about',rs_views.about,name="about"),
    path('homepage',rs_views.homepage,name='homepage'),
    path('test',rs_views.test,name='test'),
    path('logout',rs_views.log_out,name='logout'),
    path('train_show',rs_views.train_show,name='train_show'),
    path('booked_seats',rs_views.booked_seats,name='booked_seats'),
]
