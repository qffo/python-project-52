from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.views import View

from task_manager.labels.forms import LabelCreationForm
from task_manager.labels.models import Label


def labels_list(request):
    if not request.user.is_authenticated:
        messages.warning(
            request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect('login')
    labels = Label.objects.all()
    return render(request, 'labels/labels_list.html', {'labels': labels})


class LabelsCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = LabelCreationForm()
        return render(request, 'labels/labels_create.html', {'form': form})

    def post(self, request):
        form = LabelCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if Label.objects.filter(name=name).exists():
                form.add_error('name', 'Label с таким Имя уже существует.')
                return render(request, 'labels/labels_create.html', {'form': form})
            form.save()
            messages.success(request, "Метка успешно создана")
            return redirect('labels_list')
        return render(request, 'labels/labels_create.html', {'form': form})


class LabelsUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        label = Label.objects.get(pk=pk)
        form = LabelCreationForm(instance=label)
        return render(request, 'labels/labels_update.html', {'form': form})

    def post(self, request, pk):
        label = Label.objects.get(pk=pk)
        form = LabelCreationForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, "Метка успешно изменена")
            return redirect('labels_list')
        return render(request, 'labels/labels_update.html', {'form': form})


class LabelDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        label = Label.objects.get(pk=pk)
        return render(request, 'labels/labels_delete.html', {'label': label})

    def post(self, request, pk):
        label = Label.objects.get(pk=pk)
        try:
            label.delete()
            messages.success(request, "Метка успешно удалена")
        except ProtectedError:
            messages.error(
                request, "Невозможно удалить метку, потому что она используется")
        return redirect('labels_list')
