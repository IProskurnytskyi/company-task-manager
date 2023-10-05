from django.contrib.auth import get_user_model
from django.test import TestCase

from task.models import TaskType, Position, Task


class TaskTypeModelTest(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="Bug")

    def test_name_label(self):
        field_label = self.task_type._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_task_type_str(self):
        expected_object_name = self.task_type.name
        self.assertEqual(str(self.task_type), expected_object_name)


class PositionModelTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")

    def test_name_label(self):
        field_label = self.position._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_position_str(self):
        expected_object_name = self.position.name
        self.assertEqual(str(self.position), expected_object_name)


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        task_type = TaskType.objects.create(
            name="QA",
        )
        position = Position.objects.create(name="Developer")
        worker = get_user_model().objects.create_user(
            username="Carl",
            password="qwerty",
            position=position,
        )
        task = Task.objects.create(
            name="Fix Dashboard",
            description="Fix Dashboard for Vacancies",
            deadline="2024-10-05T03:26:35Z",
            is_completed=False,
            priority="low",
            task_type=task_type)
        task.assignees.set([worker])

    def setUp(self) -> None:
        self.task = Task.objects.get(id=1)

    def test_task_str(self):
        expected_object_name = self.task.name
        self.assertEqual(str(self.task), expected_object_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.task.get_absolute_url(), "/tasks/1/")


class WorkerModelTest(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="user",
            password="qwerty",
            position=self.position,
            first_name="Carl",
            last_name="Derek"
        )

    def test_create_worker_with_position(self):
        self.assertEqual(self.worker.username, "user")
        self.assertTrue(self.worker.check_password("qwerty"))
        self.assertEqual(self.worker.position, self.position)

    def test_worker_str(self):
        expected_object_name = (
            f"{self.worker.username} "
            f"({self.worker.first_name} "
            f"{self.worker.last_name})"
        )
        self.assertEqual(str(self.worker), expected_object_name)

    def test_get_absolute_url(self):
        self.assertEqual(self.worker.get_absolute_url(), "/workers/1/")

    def tearDown(self) -> None:
        self.worker.delete()
