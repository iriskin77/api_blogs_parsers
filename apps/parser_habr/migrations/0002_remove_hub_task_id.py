# Generated by Django 5.0 on 2024-01-12 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("parser_habr", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hub",
            name="task_id",
        ),
    ]
