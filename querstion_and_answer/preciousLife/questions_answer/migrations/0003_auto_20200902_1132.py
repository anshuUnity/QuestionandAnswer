# Generated by Django 3.0.8 on 2020-09-02 06:02

from django.db import migrations, models
import questions_answer.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions_answer', '0002_auto_20200831_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image_first',
            field=models.ImageField(blank=True, null=True, upload_to=questions_answer.models.path_and_rename, validators=[questions_answer.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='question',
            name='image_second',
            field=models.ImageField(blank=True, null=True, upload_to=questions_answer.models.path_and_rename, validators=[questions_answer.models.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='question',
            name='image_third',
            field=models.ImageField(blank=True, null=True, upload_to=questions_answer.models.path_and_rename, validators=[questions_answer.models.validate_file_size]),
        ),
    ]
