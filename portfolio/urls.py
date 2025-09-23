from django.urls import path
from . import views, api

urlpatterns = [
    path('projectmanagement/', views.projectmanagement, name='projectmanagement'),
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    
    # API endpoints
    path('api/projects/', api.project_list_api, name='project_list_api'),
    path('api/projects/<int:project_id>/', api.project_detail_api, name='project_detail_api'),
    path('api/categories/', api.categories_api, name='categories_api'),
]