from django.urls import path
from . import views

app_name = 'site_diary'

urlpatterns = [
    # Main site diary views
    path('diary/', views.diary, name='diary'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('newproject/', views.newproject, name='newproject'),
    path('history/', views.history, name='history'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
    path('sitedraft/', views.sitedraft, name='sitedraft'),
    
    # Entry management views
    path('entry/<int:entry_id>/', views.entry_detail, name='entry_detail'),
    path('entry/<int:entry_id>/edit/', views.entry_edit, name='entry_edit'),
    path('entry/<int:entry_id>/delete/', views.entry_delete, name='entry_delete'),
    
    # Export functionality
    path('export/reports/', views.export_reports, name='export_reports'),
    
    # Admin views
    path('admin/clientproject/', views.adminclientproject, name='adminclientproject'),
    path('admin/clientdiary/', views.adminclientdiary, name='adminclientdiary'),
    path('admin/reports/', views.adminreports, name='adminreports'),
    
    # API endpoints
    path('api/approve-entry/<int:entry_id>/', views.approve_entry, name='approve_entry'),
    path('api/project-details/<int:project_id>/', views.get_project_details, name='get_project_details'),
    
    # External app views (keeping for compatibility)
    path('chatbot/', views.chatbot, name='chatbot'),
    path('createblog/', views.createblog, name='createblog'),
    path('drafts/', views.drafts, name='drafts'),
]