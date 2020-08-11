# Generated by Django 3.0.8 on 2020-08-08 04:23

from django.conf import settings
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions_answer', '0018_auto_20200802_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Give the tags to the question', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]