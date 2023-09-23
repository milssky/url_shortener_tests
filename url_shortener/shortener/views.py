from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


from .forms import UrlForm
from .models import Url


def index(request):
    form = UrlForm()
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'form': form})
    user_urls = request.user.urls.all()
    return render(
        request,
        'index.html',
        {
            'form': form,
            'user_urls': user_urls
        }
    )


@login_required
def create_url(request):
    if request.method != 'POST':
        return redirect('index')
    form = UrlForm(request.POST or None)
    if not form.is_valid():
        return JsonResponse(
            form.errors,
            json_dumps_params={'ensure_ascii': False},
            content_type='application/json; charset=utf-8'
        )
    url_obj = form.save(commit=False)
    url_obj.author = request.user
    url_obj.save()
    return redirect('index')


@login_required
def delete_url(request, slug):
    get_object_or_404(Url, shorted_url=slug, author=request.user).delete()
    return redirect('index')


def go_to_full_url(request, slug):
    url_obj = get_object_or_404(Url, shorted_url=slug)
    url_obj.visited_times += 1
    url_obj.save()
    return redirect(url_obj.full_url)
