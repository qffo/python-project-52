from django.contrib import admin
from django.urls import include, path

from task_manager import views

from .views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
]
