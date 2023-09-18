from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from task.models import TaskType, Task, Position, Worker


def index(request: HttpRequest) -> HttpResponse:
    task_types = TaskType.objects.count()
    tasks = Task.objects.count()
    positions = Position.objects.count()
    workers = Worker.objects.count()

    context = {
        "task_types": task_types,
        "tasks": tasks,
        "positions": positions,
        "workers": workers,
    }

    return render(request, "task/index.html", context)
