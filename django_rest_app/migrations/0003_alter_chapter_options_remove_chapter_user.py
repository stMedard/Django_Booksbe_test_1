# Generated by Django 4.0.1 on 2022-01-20 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_rest_app', '0002_alter_chapter_options_chapter_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['title_chapter', 'content', 'book']},
        ),
        migrations.RemoveField(
            model_name='chapter',
            name='user',
        ),
    ]