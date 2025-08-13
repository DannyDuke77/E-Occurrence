from django.contrib import admin
from django.urls import path

from .views import index, terms

app_name = 'core'

urlpatterns = [
    path('', index, name='home'),
    path('terms-of-use/', terms, name='terms_of_use'),
]
