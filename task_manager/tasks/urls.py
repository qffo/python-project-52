from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/', views.task_info, name='task_info'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
]
