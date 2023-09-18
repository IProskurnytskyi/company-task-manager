from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

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


class TaskTypeListView(generic.ListView):
    model = TaskType
    template_name = "task/task_type_list.html"
    context_object_name = "task_type_list"


class TaskListView(generic.ListView):
    model = Task


class PositionListView(generic.ListView):
    model = Position


class WorkerListView(generic.ListView):
    model = Worker
