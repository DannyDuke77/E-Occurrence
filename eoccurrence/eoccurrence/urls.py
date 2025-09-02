"""
URL configuration for eoccurrence project.

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
from django.urls import path, include

from django.contrib.auth import views as auth_views
from accounts.forms import loginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Include the core app's URLs
    path('accounts/', include('accounts.urls')),  # Include the accounts app's URLs
    path('cases/', include('cases.urls')),  # Include the cases app's URLs

    path("", include("pwa.urls")), # PWA support
]
