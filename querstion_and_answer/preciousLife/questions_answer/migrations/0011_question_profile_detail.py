# Generated by Django 3.0.8 on 2020-07-27 07:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200723_1244'),
        ('questions_answer', '0010_auto_20200721_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='profile_detail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfileInfo'),
        ),
    ]