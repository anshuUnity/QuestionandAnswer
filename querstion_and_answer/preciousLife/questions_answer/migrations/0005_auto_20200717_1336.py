# Generated by Django 3.0.8 on 2020-07-17 08:06

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions_answer', '0004_auto_20200717_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]