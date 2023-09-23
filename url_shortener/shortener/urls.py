from django.urls import path

from .views import create_url, delete_url, index, go_to_full_url


urlpatterns = [
    path('', index, name='index'),
    path('create/', create_url, name='create_url'),
    path('delete/<slug:slug>/', delete_url, name='delete_url'),
    path('go/<slug:slug>/', go_to_full_url, name='goto')
]
