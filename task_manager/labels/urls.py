from django.urls import path

from task_manager.labels import views

urlpatterns = [
    path('', views.labels_list, name='labels_list'),
    path('create/', views.LabelsCreateView.as_view(), name='labels_create'),
    path('<int:pk>/update/', views.LabelsUpdateView.as_view(), name='labels_update'),
    path('<int:pk>/delete/', views.LabelDeleteView.as_view(), name='labels_delete'),
]
