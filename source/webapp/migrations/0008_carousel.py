# Generated by Django 4.1.7 on 2023-05-15 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_merge_20230509_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('photo', models.ImageField(upload_to='carousel', verbose_name='Carousel')),
                ('web_link', models.URLField(blank=True, null=True, verbose_name='Web link')),
            ],
            options={
                'verbose_name': 'Карусель',
                'verbose_name_plural': 'Карусели',
                'db_table': 'carousel',
            },
        ),
    ]
