from django import forms
from django.contrib.auth.forms import UserCreationForm

from task.models import Worker


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )
