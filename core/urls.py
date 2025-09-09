from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health'),
    path('tasks/', views.create_task, name='create_task'),
    path('tasks/<str:task_id>/', views.task_status, name='task_status'),
]