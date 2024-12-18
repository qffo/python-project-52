from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _(
            "User has been successfully registered"))
        return response


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user != self.request.user:
            messages.error(self.request, _(
                "You do not have the rights to change another user."))
            raise Http404(_("You cannot edit other people's data."))
        return user

    def get(self, request, *args, **kwargs):
        try:
            self.get_object()
        except Http404:
            return redirect('user_list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _("User has been successfully changed"))
        return response


class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            messages.error(request, _(
                "You do not have the rights to delete another user."))
            return redirect('user_list')
        return render(request, 'users/user_delete.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            messages.error(request, _(
                "You do not have the rights to delete another user."))
            return redirect('user_list')

        try:
            user.delete()
            messages.success(request, _("User has been successfully deleted."))
        except ProtectedError:
            messages.error(request, _(
                "It is not possible to delete a user because it is in use."))
        return redirect('user_list')


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users/users_list.html', {'users': users})
