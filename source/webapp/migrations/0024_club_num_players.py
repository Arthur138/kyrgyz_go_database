# Generated by Django 4.1.7 on 2023-03-18 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0023_merge_20230318_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='num_players',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество участников клуба'),
        ),
    ]
