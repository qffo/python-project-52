from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


def index(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect('login')  # Перенаправление на страницу входа
    statuses = Status.objects.all()
    return render(request, 'statuses/list.html', {'statuses': statuses})


class StatusCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

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
    login_url = '/login/'

    def get(self, request, pk):
        status = Status.objects.get(pk=pk)
        form = StatusForm(instance=status)
        return render(request, 'statuses/create.html', {'form': form})

    def post(self, request, pk):
        status = Status.objects.get(pk=pk)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('status_list')
        return render(request, 'statuses/create.html', {'form': form})


class StatusDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        status = Status.objects.get(pk=pk)
        return render(request, 'statuses/status_delete.html', {'status': status})

    def post(self, request, pk):
        status = Status.objects.get(pk=pk)
        status.delete()
        return redirect('status_list')
