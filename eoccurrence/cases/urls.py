from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('complainant/new/', views.complainant_entry, name='complainant_entry'),
    path('case/new/<uuid:uuid>/', views.case_entry, name='case_entry'),
    path('cases-list/', views.view_cases, name='view_cases'),
    path('case-details/<uuid:uuid>/', views.case_details, name='case_details'),
    path('case/edit/<uuid:uuid>/', views.edit_case, name='edit_case'),
    path('search/', views.search_cases, name='search_cases'),
    path('case/witness/new/<uuid:uuid>/', views.witness_entry, name='witness_entry'),
]
