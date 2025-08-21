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
    path("case/<uuid:case_uuid>/witness/<uuid:witness_uuid>/", views.witness_page, name="witness_page"),
    path('case/suspect/new/<uuid:uuid>/', views.suspect_entry, name='suspect_entry'),
    path('case/republic-court-decision/<uuid:uuid>/', views.court_case_final , name='court_case_final'),
    path("case/<uuid:case_uuid>/suspect/<uuid:suspect_uuid>/", views.suspect_page, name="suspect_page"),
    path("case/<uuid:case_uuid>/complainant/<uuid:complainant_uuid>/", views.complainant_page, name="complainant_page"),
    path('case/suspect/<uuid:uuid>/court-ruling/', views.suspect_court_ruling_entry, name='suspect_court_ruling_entry'),
    path('case/suspect/<uuid:suspect_uuid>/court-ruling/<uuid:ruling_uuid>/edit/', views.edit_suspect_court_ruling, name='edit_suspect_court_ruling'),
    path("suspects/", views.suspect_list, name="suspect_list"),
    path("witnesses/", views.witness_list, name="witness_list"),
    path("statistics/", views.statistics, name="statistics"),
]
