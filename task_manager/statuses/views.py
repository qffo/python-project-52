from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.views import View

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


def index(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect('login')
    statuses = Status.objects.all()
    return render(request, 'statuses/list.html', {'statuses': statuses})


class StatusCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = StatusForm()
        return render(request, 'statuses/create.html', {'form': form})

    def post(self, request):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно создан")
            return redirect('status_list')
        return render(request, 'statuses/create.html', {'form': form})


class StatusUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        status = Status.objects.get(pk=pk)
        form = StatusForm(instance=status)
        return render(request, 'statuses/status_update.html', {'form': form})

    def post(self, request, pk):
        status = Status.objects.get(pk=pk)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, "Статус успешно изменен")
            return redirect('status_list')
        return render(request, 'statuses/status_update.html', {'form': form})


class StatusDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        status = Status.objects.get(pk=pk)
        return render(request, 'statuses/status_delete.html', {'status': status})

    def post(self, request, pk):
        status = Status.objects.get(pk=pk)
        try:
            status.delete()
            messages.success(request, "Статус успешно удален.")
        except ProtectedError:
            messages.error(
                request, "Невозможно удалить статус, потому что он используется")
        return redirect('status_list')
