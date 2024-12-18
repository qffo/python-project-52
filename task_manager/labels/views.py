from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views import View

from task_manager.labels.forms import LabelCreationForm
from task_manager.labels.models import Label


class LabelsListView(LoginRequiredMixin, View):
    def handle_no_permission(self):
        messages.warning(
            self.request,
            _("You are not logged in! Please log in."))
        return redirect('login')

    def get(self, request):
        labels = Label.objects.all()
        return render(request, 'labels/labels_list.html', {'labels': labels})


class LabelsCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = LabelCreationForm()
        return render(request, 'labels/labels_create.html', {'form': form})

    def post(self, request):
        form = LabelCreationForm(request.POST)

        if not form.is_valid():
            return render(request, 'labels/labels_create.html', {'form': form})

        name = form.cleaned_data['name']

        if Label.objects.filter(name=name).exists():
            form.add_error('name', _('Label with this Name already exists.'))
            return render(request, 'labels/labels_create.html', {'form': form})

        form.save()
        messages.success(request, _("The label was created successfully"))
        return redirect('labels_list')


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
            messages.success(request, _("Label has been successfully changed"))
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
            messages.success(
                request,
                _("The label was successfully deleted"))
        except ProtectedError:
            messages.error(
                request,
                _("Cannot delete this label because it is being used"))
        return redirect('labels_list')
