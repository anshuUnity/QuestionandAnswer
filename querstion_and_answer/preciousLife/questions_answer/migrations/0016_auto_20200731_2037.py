# Generated by Django 3.0.8 on 2020-07-31 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions_answer', '0015_answer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='Question',
            new_name='question',
        ),
    ]
