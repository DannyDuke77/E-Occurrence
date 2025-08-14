from django.contrib.auth import views as auth_views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .forms import loginForm

from . import views

app_name = 'accounts'

urlpatterns = [
    path('create-user/', views.create_user, name='create_user'),
    path('admin-login/', 
         auth_views.LoginView.as_view(
             template_name='accounts/login.html', 
             authentication_form=loginForm
        ), 
        name='admin-login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)