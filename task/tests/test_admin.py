from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task.models import Position, TaskType, Task


class TaskAdminTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(name="DevOps")

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="qwerty",
            position=position,
        )
        self.client.force_login(self.admin_user)

        worker = get_user_model().objects.create_user(
            username="worker",
            password="asdf",
            position=position,
        )
        task_type = TaskType.objects.create(
            name="QA",
        )
        self.task = Task.objects.create(
            name="Fix Dashboard",
            description="Fix Dashboard for Vacancies",
            deadline="2024-10-05 03:26:35",
            is_completed=False,
            priority="low",
            task_type=task_type)
        self.task.assignees.set([worker])

    def test_task_additional_fields_listed(self):
        url = reverse("admin:task_task_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.is_completed)
        self.assertContains(response, self.task.priority)
        self.assertContains(response, self.task.task_type)

    def test_filter_fields(self):
        url = reverse("admin:task_task_changelist")
        response = self.client.get(url)

        self.assertContains(response, "is_completed")
        self.assertContains(response, "priority")
        self.assertContains(response, "task_type")

    def test_search_fields(self):
        url = reverse("admin:task_task_changelist")
        response = self.client.get(url)

        self.assertContains(response, "name")

    def test_task_add_has_required_field(self):
        url = reverse("admin:task_task_add")
        response = self.client.get(url)

        self.assertContains(response, "name")
        self.assertContains(response, "description")
        self.assertContains(response, "deadline")
        self.assertContains(response, "is_completed")
        self.assertContains(response, "priority")
        self.assertContains(response, "task_type")
        self.assertContains(response, "assignees")


class WorkerAdminTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(name="DevOps")

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="qwerty",
            position=position,
        )
        self.client.force_login(self.admin_user)
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="asdf",
            position=position,
        )

    def test_worker_position_listed(self):
        url = reverse("admin:task_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_worker_detailed_position_listed(self):
        url = reverse("admin:task_worker_change", args=[self.worker.id])
        response = self.client.get(url)

        self.assertContains(response, self.worker.position)

    def test_worker_add_position_listed(self):
        url = reverse("admin:task_worker_add")
        response = self.client.get(url)

        self.assertContains(response, "position")
