# Generated by Django 5.0 on 2024-03-07 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name_cat",
                    models.CharField(
                        max_length=255, unique=True, verbose_name="Категория"
                    ),
                ),
                (
                    "link_cat",
                    models.URLField(
                        max_length=10000,
                        unique=True,
                        verbose_name="Ссылка на категорию",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "celery_task_id",
                    models.CharField(max_length=1001, verbose_name="id celery"),
                ),
                (
                    "is_success",
                    models.BooleanField(default=False, verbose_name="Статус задачи"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Задачи",
                "verbose_name_plural": "Задачи",
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                ("body", models.TextField(verbose_name="Содержание статьи")),
                (
                    "date_published",
                    models.CharField(max_length=255, verbose_name="Дата публикации"),
                ),
                (
                    "link",
                    models.URLField(max_length=10000, verbose_name="Ссылка на статью"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="parser_mel.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Статьи",
                "verbose_name_plural": "Статьи",
            },
        ),
    ]
