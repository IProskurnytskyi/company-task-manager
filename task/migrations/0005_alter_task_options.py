# Generated by Django 4.2.5 on 2023-09-22 13:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0004_alter_task_deadline"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={"ordering": ["is_completed", "priority"]},
        ),
    ]