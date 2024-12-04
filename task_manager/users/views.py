from django.contrib import messages
from django.db.models import ProtectedError
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
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
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return response


class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user_list')

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user != self.request.user:
            messages.error(
                self.request, "У вас нет прав для изменения другого пользователя.")
            raise Http404("Вы не можете редактировать чужие данные.")
        return user

    def get(self, request, *args, **kwargs):
        try:
            self.get_object()
        except Http404:
            return redirect('user_list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Пользователь успешно изменен")
        return response


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        messages.error(
            request, "У вас нет прав для изменения другого пользователя.")
        return redirect('user_list')

    if request.method == 'POST':
        try:
            user.delete()
            messages.success(request, "Пользователь успешно удален.")
        except ProtectedError:
            messages.error(
                request, "Невозможно удалить пользователя, потому что он используется.")
        return redirect('user_list')

    return render(request, 'users/user_delete.html', {'user': user})


def user_list(request):
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})
