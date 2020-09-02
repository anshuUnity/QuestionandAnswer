# Generated by Django 3.0.8 on 2020-09-01 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_contactform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactform',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to=settings.AUTH_USER_MODEL),
        ),
    ]
