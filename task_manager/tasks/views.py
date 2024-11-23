from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from task_manager.tasks.forms import TaskCreationForm
from task_manager.statuses.models import Status
from task_manager.users.models import User


def index(request):
    return render(request, 'tasks/tasks_list.html')


def task_info(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'tasks/task_info.html', {'task': task})


def tasks_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks})


class TaskCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = TaskCreationForm()
        statuses = Status.objects.all()
        users = User.objects.all()
        return render(request, 'tasks/task_create.html', {
            'form': form,
            'statuses': statuses,
            'users': users
        })

    def post(self, request):
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.success(request, "Задача успешно создана")
            return redirect('tasks_list')
        messages.error(request, "Ошибка при создании задачи")
        return render(request, 'tasks/task_create.html', {'form': form})
