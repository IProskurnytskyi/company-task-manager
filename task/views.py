from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task.forms import WorkerForm
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


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    template_name = "task/task_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task:task-type-list")


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    template_name = "task/task_type_form.html"
    fields = "__all__"
    success_url = reverse_lazy("task:task-type-list")


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("task:task-type-list")
    template_name = "task/task_type_confirm_delete.html"


class TaskListView(generic.ListView):
    model = Task


class TaskDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("")

    def get_success_url(self):
        return reverse_lazy("task:task-detail", args=[self.object.pk])


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")


class PositionListView(generic.ListView):
    model = Position


class PositionCreateView(generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:position-list")


class PositionUpdateView(generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("task:position-list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("task:position-list")


class WorkerListView(generic.ListView):
    model = Worker
    queryset = Worker.objects.select_related("position")


class WorkerDetailView(generic.DetailView):
    model = Worker


class WorkerCreateView(generic.CreateView):
    model = Worker
    form_class = WorkerForm
    success_url = reverse_lazy("task:worker-list")


class WorkerUpdateView(generic.UpdateView):
    model = Worker
    form_class = WorkerForm

    def get_success_url(self):
        return reverse_lazy("task:worker-detail", args=[self.object.pk])


class WorkerDeleteView(generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("task:worker-list")
