from django.urls import path

from task.views import (
    index,
    TaskTypeListView,
    TaskListView,
    PositionListView,
    WorkerListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
]

app_name = "task"
