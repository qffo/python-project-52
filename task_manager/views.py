from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LoginView


def index(request):
    return render(request, 'index.html')


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')


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
            user = self.get_object()
        except Http404:
            return redirect('user_list')
        return super().get(request, *args, **kwargs)


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        messages.error(
            request, "У вас нет прав для изменения другого пользователя.")
        return redirect('user_list')

    user.delete()
    return redirect('user_list')


def user_list(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')
