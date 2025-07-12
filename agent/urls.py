from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.agent_login, name='login'),
    path('candidate_login.html', views.candidate_login, name='candidate_login'),
    path('logout.html', views.user_logout, name='logout'),
    
    
    # Candidate URLs
    path('candidate_dashboard.html', views.candidate_dashboard, name='candidate_dashboard'),
    path('reported_incidents.html', views.reported_incidents, name='reported_incident'),
    path('results.html', views.results_summary, name='results_summary'),
    path('reports.html', views.reports, name='reports'),
    path('report_detail/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/<int:report_id>/download-dr-form/', views.download_dr_form, name='download_dr_form'),
    
    
    # Agent URLs
    path('agent_dashboard.html', views.agent_dashboard, name='agent_dashboard'),
    path('incident.html', views.report_incident, name='incident'),
]