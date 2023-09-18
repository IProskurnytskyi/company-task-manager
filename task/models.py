from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager import settings


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


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

    class Meta:
        ordering = ["deadline"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position", on_delete=models.CASCADE, related_name="workers"
    )

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name
