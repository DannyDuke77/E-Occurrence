from django.contrib import admin
from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('faq/', views.faq, name='faq'),
    path('help-and-support/', views.help_support, name='help_support'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
