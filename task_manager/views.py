from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def user_list(request):
    return render(request, 'users.html')
