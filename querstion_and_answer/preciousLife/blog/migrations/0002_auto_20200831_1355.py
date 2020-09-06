# Generated by Django 3.0.8 on 2020-08-31 08:25

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_images/', validators=[blog.models.validate_file_size]),
        ),
    ]