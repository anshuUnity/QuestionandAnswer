# Generated by Django 3.0.8 on 2020-07-16 09:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255)),
                ('title', models.CharField(max_length=264)),
                ('description', markdownx.models.MarkdownxField()),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-published_date'],
            },
        ),
    ]
