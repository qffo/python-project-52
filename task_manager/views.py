from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
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


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return HttpResponseRedirect(reverse('user_list'))


def user_list(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')
