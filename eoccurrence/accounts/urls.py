from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import loginForm

from . import views

app_name = 'accounts'

urlpatterns = [
    path('create-user/', views.create_user, name='create_user'),
    path('login/', 
         auth_views.LoginView.as_view(
             template_name='accounts/login.html', 
             authentication_form=loginForm
        ), 
        name='login'),
    path('logout/', views.logout_view, name='logout'),
]