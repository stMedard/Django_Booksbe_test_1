# Generated by Django 4.0.1 on 2022-01-22 14:13

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_rest_app', '0004_alter_chapter_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Content'),
        ),
    ]