# Generated by Django 4.0.1 on 2022-01-17 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_rest_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useradmin',
            name='is_staff',
            field=models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
