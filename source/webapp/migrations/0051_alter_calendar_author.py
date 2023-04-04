# Generated by Django 4.1.7 on 2023-04-04 10:10

from django.conf import settings
from django.db import migrations, models
import webapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0050_remove_participant_patronymic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='author',
            field=models.ForeignKey(default=webapp.models.get_author, on_delete=models.SET(webapp.models.get_author), to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]
