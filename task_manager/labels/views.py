from django.shortcuts import render


def index(request):
    return render(request, 'labels/labels_list.html')
