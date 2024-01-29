"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='create_task'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.UserSignupView.as_view(), name='signuo'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/<int:task_id>/', views.edit, name='edit'),
    path('detail/<int:task_id>/', views.task_detail, name='task_detail'),
    path('delete_photo/<int:photo_id>/',
         views.DeleteTaskPhotoView.as_view(), name='delete_photo'),
    path('delete_task/<int:task_id>/',
         views.DeleteTaskView.as_view(), name='delete_task'),
]
