# Generated by Django 3.0.8 on 2020-09-06 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200831_1355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='tags',
            new_name='blog_tags',
        ),
    ]
