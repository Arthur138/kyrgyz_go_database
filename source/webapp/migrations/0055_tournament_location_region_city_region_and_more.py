# Generated by Django 4.1.7 on 2023-04-09 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0054_game_black_gor_change_game_white_gor_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Место проведения'),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Регион')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.country')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='webapp.region'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.region'),
        ),
    ]
