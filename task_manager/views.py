from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy


def index(request):
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, """Пожалуйста, введите правильные имя пользователя и пароль.
             Оба поля могут быть чувствительны к регистру.""")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
