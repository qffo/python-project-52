from django.urls import path
from task_manager.labels import views


urlpatterns = [
    path('', views.index, name='labels_list'),
]
