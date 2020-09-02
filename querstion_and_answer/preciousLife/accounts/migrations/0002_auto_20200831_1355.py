# Generated by Django 3.0.8 on 2020-08-31 08:25

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='profile_pic_user',
            field=models.ImageField(blank=True, upload_to='profile_pics', validators=[accounts.models.validate_file_size]),
        ),
    ]
