from django.contrib import admin
from django.urls import include, path
from task_manager import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomLogoutView, UserCreateView, UserUpdateView, user_delete, CustomLoginView


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', user_delete, name='user_delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('statuses/', include('task_manager.statuses.urls')),
]
