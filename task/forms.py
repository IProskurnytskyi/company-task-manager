from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from task.models import Worker, Task


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "position",
        )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Worker
        fields = UserCreationForm.Meta.fields


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

    deadline = forms.DateTimeField(
        error_messages={
            "invalid": "Enter a valid date/time in the format: YYYY-MM-DD HH:MM:SS"
        }
    )

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.now():
            raise ValidationError("The deadline cannot be set in the past")

        max_deadline = timezone.now() + timezone.timedelta(days=365 * 20)

        if deadline > max_deadline:
            raise ValidationError("The deadline cannot be set more than 20 years into the future")

        return deadline


class NameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name.."})
    )


class WorkerUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username.."})
    )
