# Generated by Django 4.1.7 on 2023-03-05 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_merge_0008_calendar_0008_tournament_tournament_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_avatar', verbose_name='Аватар'),
        ),
    ]
