# Generated by Django 3.0.8 on 2020-07-19 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofileinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='full_name',
            field=models.CharField(blank=True, max_length=230, null=True),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]