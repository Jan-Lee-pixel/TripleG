from django.urls import path
from . import views

urlpatterns = [
    path('', views.diary, name='diary'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('newproject/', views.newproject, name='newproject'),
    path('createblog/', views.createblog, name='createblog'),
    path('drafts/', views.drafts, name='drafts'),
    path('history/', views.history, name='history'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),
 ]