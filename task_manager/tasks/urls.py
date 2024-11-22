from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
]
