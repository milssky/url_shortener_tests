from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse

from .forms import UrlForm


def index(request):
    return render(request, 'index.html', {'form': UrlForm()})


@login_required
def create_url(request):
    return HttpResponse(b"123")
