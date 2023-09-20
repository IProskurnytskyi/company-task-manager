from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from task.forms import TaskForm
from task.models import Position, TaskType, Task


class TaskFormTest(TestCase):
    def setUp(self) -> None:
        position = Position.objects.create(name="DevOps")
        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="qwerty",
            position=position,
        )
        self.task_type = TaskType.objects.create(
            name="Bug",
        )

    def test_task_creation_form_valid_data(self):
        form_data = {
            "name": "Fix Dashboard",
            "description": "Fix Dashboard for Vacancies",
            "deadline": timezone.now() + timezone.timedelta(days=1),
            "is_completed": False,
            "priority": "low",
            "task_type": self.task_type,
            "assignees": [self.worker],
        }
        form = TaskForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_task_creation_form_deadline_in_the_past(self):
        form_data = {
            "name": "Fix Dashboard",
            "description": "Fix Dashboard for Vacancies",
            "deadline": timezone.now() - timezone.timedelta(days=1),
            "is_completed": False,
            "priority": "low",
            "task_type": self.task_type,
            "assignees": [self.worker],
        }
        form = TaskForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "The deadline cannot be set in the past",
            form.errors["deadline"]
        )

    def test_task_creation_form_deadline_more_than_20_years(self):
        form_data = {
            "name": "Fix Dashboard",
            "description": "Fix Dashboard for Vacancies",
            "deadline": timezone.now() + timezone.timedelta(days=365 * 20 + 1),
            "is_completed": False,
            "priority": "low",
            "task_type": self.task_type,
            "assignees": [self.worker],
        }
        form = TaskForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "The deadline cannot be set more than 20 years into the future",
            form.errors["deadline"]
        )

    def test_task_creation_form_with_invalid_deadline_format(self):
        form_data = {
            "name": "Fix Dashboard",
            "description": "Fix Dashboard for Vacancies",
            "deadline": "2023",
            "is_completed": False,
            "priority": "low",
            "task_type": self.task_type,
            "assignees": [self.worker],
        }
        form = TaskForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Enter a valid date/time in the format: YYYY-MM-DD HH:MM:SS",
            form.errors["deadline"]
        )
