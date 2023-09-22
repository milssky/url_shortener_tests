from django.urls import path

from .views import create_url, index


urlpatterns = [
    path('', index, name='index'),
    path('create/', create_url, name='create_url'),
]
