from django.shortcuts import render

from .forms import UrlForm


def index(request):
    return render(request, 'index.html', {'form': UrlForm()})
