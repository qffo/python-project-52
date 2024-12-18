from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


def index(request):
    return render(request, 'index.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(
            self.request,
            _("You are logged in")
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            _("""Please enter the correct username and password.
            Both fields can be case sensitive.""")
        )
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(
            request,
            _("You are logged out")
        )
        return super().dispatch(request, *args, **kwargs)
