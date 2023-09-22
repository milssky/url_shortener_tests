# Generated by Django 4.2.5 on 2023-09-22 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_url', models.URLField(max_length=2000, verbose_name='Сокращаемая ссылка')),
                ('shorted_url', models.SlugField(unique=True, verbose_name='Короткий вариант ссылки')),
                ('visited_times', models.PositiveIntegerField(default=0, verbose_name='Количество посещений ссылки')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to=settings.AUTH_USER_MODEL, verbose_name='Владелец ссылки')),
            ],
        ),
    ]