# Generated by Django 4.0.1 on 2022-01-17 21:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('title', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=70)),
                ('first_name', models.CharField(blank=True, max_length=70)),
                ('last_name', models.CharField(blank=True, max_length=70)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_chapter', models.CharField(blank=True, max_length=200)),
                ('content', models.TextField(blank=True)),
                ('book', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='django_rest_app.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='django_rest_app.useradmin'),
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ForeignKey(help_text='Select a genre for this book', null=True, on_delete=django.db.models.deletion.CASCADE, to='django_rest_app.genre'),
        ),
    ]