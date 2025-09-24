from django.urls import path
from . import views

urlpatterns = [
    path('adminside/clientproject/', views.adminclientproject, name='adminclientproject'),
    path('adminside/diary/', views.admindiary, name='admindiary'),
    path('adminside/diaryreviewer/', views.admindiaryreviewer, name='admindiaryreviewer'),
    path('adminside/history/', views.adminhistory, name='adminhistory'),
    path('adminside/reports/', views.adminreports, name='adminreports'),
    path('', views.diary, name='diary'),
    path('sitedraft/', views.sitedraft, name='sitedraft'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('newproject/', views.newproject, name='newproject'),
    path('createblog/', views.createblog, name='createblog'),
    path('drafts/', views.drafts, name='drafts'),
    path('history/', views.history, name='history'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
]