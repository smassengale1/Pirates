"""pirates_inv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views import View

from .views import views_pirate as pirate_views
from .views import views_manage as manage_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pirate_views.dashboard, name='dashboard'),
    path('dashboard/', pirate_views.dashboard, name = 'dashboard'),
    path('dashboard/assets', manage_views.assets.as_view(), name = 'assets'),
    path('dashboard/vendors', manage_views.vendors.as_view(), name = 'vendors'),
    path('dashboard/locations', manage_views.locations.as_view(), name = 'locations'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('ajax/validate_building', manage_views.validate_building),
    path('ajax/remove_building', manage_views.remove_building),
    path('ajax/update_building', manage_views.update_building),

]
