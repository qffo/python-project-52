from django.shortcuts import render
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


def task_update(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'tasks/task_update.html', {'task': task})


def task_delete(request, pk):
    task = Task.objects.get(pk=pk)

    if task.author != request.user:
        messages.error(request, "Задачу может удалить только ее автор")
        return redirect('tasks_list')

    if request.method == 'POST':
        task.delete()
        messages.success(request, "Задача успешно удалена")
        return redirect('tasks_list')

    return render(request, 'tasks/task_delete.html', {'task': task})


class TaskCreateView(LoginRequiredMixin, View):
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


def task_update(request, pk):
    task = Task.objects.get(pk=pk)

    if request.method == 'POST':
        form = TaskCreationForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Задача успешно изменена")
            return redirect('task_info', pk=task.pk)
        else:
            messages.error(request, "Ошибка при обновлении задачи")
    else:
        form = TaskCreationForm(instance=task)

    statuses = Status.objects.all()
    users = User.objects.all()

    return render(request, 'tasks/task_update.html', {
        'form': form,
        'task': task,
        'statuses': statuses,
        'users': users
    })
