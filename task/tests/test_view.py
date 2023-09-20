from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task.models import Task, Position, TaskType


class TaskViewTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="DevOps")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="qwerty",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(
            name="Bug",
        )

        for number in range(10):
            task = Task.objects.create(
                name=f"{number}Fix Dashboard",
                description=f"{number}Fix Dashboard for Vacancies",
                deadline="2024-10-05T03:26:35Z",
                is_completed=False,
                priority="low",
                task_type=self.task_type)
            task.assignees.set([self.worker])

    def test_login_required_for_unauthorized_users(self):
        response = self.client.get(reverse("task:task-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/tasks/")

    def test_retrieve_tasks(self):
        self.client.force_login(self.worker)
        response = self.client.get(reverse("task:task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all()[:4])
        )
        self.assertTemplateUsed(response, "task/task_list.html")

    def test_search_field_tasks(self):
        self.client.force_login(self.worker)
        response = self.client.get(
            reverse("task:task-list"), {"name": "1Fix Dashboard"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            [Task.objects.get(name="1Fix Dashboard")]
        )

    def test_pagination(self):
        self.client.force_login(self.worker)
        response = self.client.get(reverse("task:task-list"))

        self.assertEqual(len(response.context["task_list"]), 4)

    def test_tasks_when_there_is_no_search(self):
        self.client.force_login(self.worker)
        response = self.client.get(
            reverse("task:task-list"), {"name": ""}
        )

        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.all()[:4])
        )

    def test_invalid_search(self):
        self.client.force_login(self.worker)
        response = self.client.get(
            reverse("task:task-list"),
            {"name": "NonExistentTask"}
        )

        self.assertEqual(list(response.context["task_list"]), [])

    def test_task_detail_view(self):
        self.client.force_login(self.worker)

        self.task = Task.objects.get(id=1)

        response = self.client.get(
            reverse("task:task-detail", args=[self.task.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)
        self.assertEqual(response.context["task"], self.task)

    def test_create_task(self):
        self.client.force_login(self.worker)

        data = {
            "name": "Bug",
            "description": "Fix",
            "deadline": "2024-10-05T03:26:35Z",
            "is_completed": False,
            "priority": "high",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }

        response = self.client.post(
            reverse("task:task-create"), data=data
        )

        self.assertRedirects(response, reverse("task:task-list"))
        self.assertTrue(Task.objects.filter(name="Bug").exists())

    def test_create_task_without_login(self):
        data = {
            "name": "Bug",
            "description": "Fix",
            "deadline": "2024-10-05T03:26:35Z",
            "is_completed": False,
            "priority": "high",
            "task_type": self.task_type,
            "assignees": [self.worker],
        }

        response = self.client.post(
            reverse("task:task-create"), data=data
        )

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, "/accounts/login/?next=/tasks/create/"
        )
        self.assertFalse(Task.objects.filter(name="Bug").exists())

    def test_update_task(self):
        self.client.force_login(self.worker)

        data = {
            "name": "Bug2",
            "description": "Fix",
            "deadline": "2024-10-05T03:26:35Z",
            "is_completed": False,
            "priority": "high",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
        }
        self.task = Task.objects.get(id=1)

        response = self.client.post(
            reverse("task:task-update", args=[self.task.id]),
            data=data
        )

        self.assertRedirects(
            response, reverse("task:task-detail", args=[self.task.id])
        )

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Bug2")
        self.assertEqual(self.task.description, "Fix")

    def test_delete_task(self):
        self.client.force_login(self.worker)

        self.task = Task.objects.get(id=1)

        response = self.client.post(
            reverse("task:task-delete", args=[self.task.id]),
        )

        self.assertRedirects(response, reverse("task:task-list"))

        self.assertFalse(Task.objects.filter(name="0Fix Dashboard").exists())


class AssignDeleteTaskTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="DevOps")

        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="qwerty",
            position=self.position,
        )
        self.client.force_login(self.worker)

        self.task_type = TaskType.objects.create(
            name="Bug",
        )

        self.task = Task.objects.create(
            name="Fix Dashboard",
            description="Fix Dashboard for Vacancies",
            deadline="2024-10-05T03:26:35Z",
            is_completed=False,
            priority="low",
            task_type=self.task_type)
        self.task.assignees.set([self.worker])

    def test_assign_task_to_worker(self):
        self.assertTrue(self.worker.tasks.filter(id=self.task.id).exists())

        response = self.client.post(
            reverse("task:assign-delete", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 302)

        self.worker.refresh_from_db()

        self.assertFalse(self.worker.tasks.filter(id=self.task.id).exists())

    def test_unassign_task_from_worker(self):
        self.worker.tasks.remove(self.task)
        self.worker.save()

        self.assertFalse(self.worker.tasks.filter(id=self.task.id).exists())

        response = self.client.post(
            reverse("task:assign-delete", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 302)

        self.worker.refresh_from_db()

        self.assertTrue(self.worker.tasks.filter(id=self.task.id).exists())


class MarkUnmarkAsDoneViewTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="DevOps")

        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="qwerty",
            position=self.position,
        )
        self.client.force_login(self.worker)

        self.task_type = TaskType.objects.create(
            name="Bug",
        )

        self.task = Task.objects.create(
            name="Fix Dashboard",
            description="Fix Dashboard for Vacancies",
            deadline="2024-10-05T03:26:35Z",
            is_completed=False,
            priority="low",
            task_type=self.task_type)
        self.task.assignees.set([self.worker])

    def test_mark_task_as_done(self):
        self.assertFalse(self.task.is_completed)

        response = self.client.post(
            reverse("task:mark-unmark", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()

        self.assertTrue(self.task.is_completed)

    def test_unmark_task_as_done(self):
        self.task.is_completed = True
        self.task.save()

        response = self.client.post(
            reverse("task:mark-unmark", args=[self.task.id])
        )

        self.assertEqual(response.status_code, 302)

        self.task.refresh_from_db()

        self.assertFalse(self.task.is_completed)
