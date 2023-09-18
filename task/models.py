from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager import settings


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        choices=PRIORITY_CHOICES, default="medium"
    )
    task_type = models.ForeignKey(
        TaskType, on_delete=models.SET_NULL, related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="tasks"
    )


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position", on_delete=models.CASCADE, related_name="workers"
    )


class Position(models.Model):
    name = models.CharField(max_length=128)
