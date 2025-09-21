from django.urls import path
from . import views

urlpatterns = [
    path('blogmanagement/', views.blog_list, name='blogmanagement'),  # points to blog_list for now
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>/', views.blog_individual, name='blog_individual'),
]