from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from task_manager import settings


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "task type"
        verbose_name_plural = "task types"

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
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(
        choices=PRIORITY_CHOICES, default="medium", max_length=10
    )
    task_type = models.ForeignKey(
        TaskType, on_delete=models.SET_NULL, related_name="tasks", null=True
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="tasks"
    )

    class Meta:
        ordering = ["-deadline"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("task:task-detail", kwargs={"pk": self.pk})


class Worker(AbstractUser):
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        related_name="workers",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["position"]
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("task:worker-detail", kwargs={"pk": self.pk})


class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name
