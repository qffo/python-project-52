from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path('', views.index, name='tasks_list'),
]
