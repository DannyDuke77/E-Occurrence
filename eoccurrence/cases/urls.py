from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('complainant/new/', views.complainant_entry, name='complainant_entry'),
    path('case/new/<int:complainant_id>/', views.case_entry, name='case_entry'),
    path('cases-list/', views.view_cases, name='view_cases'),
    path('case-details/<slug:case_number>/', views.case_details, name='case_details'),
    path('search/', views.search_cases, name='search_cases'),
    path('case/witness/new/<str:case_number>/', views.witness_entry, name='witness_entry'),
]
