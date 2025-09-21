from django.urls import path
from . import views

urlpatterns = [
    path('projectmanagement/', views.projectmanagement, name='projectmanagement'),
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
]