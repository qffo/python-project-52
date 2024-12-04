from task_manager.tasks.models import Task
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from task_manager.tasks.forms import TaskCreationForm
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label
from task_manager.tasks.filters import TaskFilter


def tasks_list(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect('login')

    filter = TaskFilter(
        request.GET, queryset=Task.objects.all(), request=request)
    tasks = filter.qs

    statuses = Status.objects.all()
    users = User.objects.all()
    labels = Label.objects.all()

    return render(request, 'tasks/tasks_list.html', {
        'tasks': tasks,
        'statuses': statuses,
        'users': users,
        'labels': labels,
        'filter': filter
    })


def task_info(request, pk):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect('login')
    task = Task.objects.get(pk=pk)
    return render(request, 'tasks/task_info.html', {'task': task})


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
        labels = Label.objects.all()
        return render(request, 'tasks/task_create.html', {
            'form': form,
            'statuses': statuses,
            'users': users,
            'labels': labels
        })

    def post(self, request):
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            labels = form.cleaned_data.get('labels')
            task.labels.set(labels)
            messages.success(request, "Задача успешно создана")
            return redirect('tasks_list')
        return render(request, 'tasks/task_create.html', {'form': form})


def task_update(request, pk):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect('login')
    task = Task.objects.get(pk=pk)

    if request.method == 'POST':
        form = TaskCreationForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            labels = form.cleaned_data.get('labels')
            task.labels.set(labels)
            messages.success(request, "Задача успешно изменена")
            return redirect('tasks_list')
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
