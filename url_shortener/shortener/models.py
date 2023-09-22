from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Url(models.Model):
    full_url = models.URLField(
        max_length=2000,
        verbose_name='Сокращаемая ссылка'
    )
    shorted_url = models.SlugField(
        unique=True,
        verbose_name='Короткий вариант ссылки'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='urls',
        verbose_name='Владелец ссылки'
    )
    visited_times = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество посещений ссылки'
    )
