from django import views
from django.urls import path
from . import views

urlpatterns = [
   path('countries', views.CountryCreateView.as_view(), name='country-create'),
    path('countries/list', views.CountryListView.as_view(), name='country-list'),
    path('jobs', views.JobCreateView.as_view(), name='job-create'),
    path('jobs/list', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:job_id>/apply/', views.JobApplicationView.as_view(), name='apply-job'),
]
