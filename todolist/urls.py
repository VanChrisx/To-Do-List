"""
URL configuration for todolist project.

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
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.signup, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('create-task/', views.create_task, name='create'),
    path('all-tasks/', views.all_tasks, name='alltasks'),
    path('pending-tasks/', views.pending_tasks, name='pending'),
    path('completed-tasks/', views.completed_tasks, name='complete'),
    path('detail-task/<int:task_id>', views.detail_task, name='details'),
    path('detail-task/<int:task_id>/complete',
         views.complete_task, name='complete_task'),
    path('detail-task/<int:task_id>/delete', views.delete_task, name='delete')
]
