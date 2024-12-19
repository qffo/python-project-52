from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views import View

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TasksListView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        messages.warning(self.request, _(
            "You are not logged in! Please log in."))
        return redirect('login')

    def get(self, request):
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


class TaskInfoView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        messages.warning(self.request, _(
            "You are not logged in! Please log in."))
        return redirect('login')

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        return render(request, 'tasks/task_info.html', {'task': task})


class TaskDeleteView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        messages.warning(self.request, _(
            "You are not logged in! Please log in."))
        return redirect('login')

    def get(self, request, pk):
        task = Task.objects.get(pk=pk)

        if task.author != request.user:
            messages.error(request, _(
                "Only the author of the task can delete it."))
            return redirect('tasks_list')
        return render(request, 'tasks/task_delete.html', {'task': task})

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        if task.author != request.user:
            messages.error(request, _(
                "Only the author of the task can delete it."))
            return redirect('tasks_list')
        task.delete()
        messages.success(request, _("The task was successfully deleted"))
        return redirect('tasks_list')


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
            messages.success(request, _(
                "The task has been successfully created"))
            return redirect('tasks_list')
        return render(request, 'tasks/task_create.html', {'form': form})


class TaskUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        form = TaskCreationForm(instance=task)

        statuses = Status.objects.all()
        users = User.objects.all()

        return render(request, 'tasks/task_update.html', {
            'form': form,
            'task': task,
            'statuses': statuses,
            'users': users
        })

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        form = TaskCreationForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            labels = form.cleaned_data.get('labels')
            task.labels.set(labels)
            messages.success(request, _(
                "The task has been successfully changed"))
            return redirect('tasks_list')
        else:
            messages.error(request, _("Error updating the task"))

        statuses = Status.objects.all()
        users = User.objects.all()

        return render(request, 'tasks/task_update.html', {
            'form': form,
            'task': task,
            'statuses': statuses,
            'users': users
        })
