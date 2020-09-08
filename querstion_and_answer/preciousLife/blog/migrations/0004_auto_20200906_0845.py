# Generated by Django 3.0.8 on 2020-09-06 03:15

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('blog', '0003_auto_20200906_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='blog_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='Give tags to the blog', related_name='blog_tags', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]