from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/',
         views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.user_delete, name='user_delete'),
]
