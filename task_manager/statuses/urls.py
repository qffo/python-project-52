from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('', views.index, name='status_list'),
]
