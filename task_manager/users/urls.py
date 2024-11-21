from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/',
         views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
]
