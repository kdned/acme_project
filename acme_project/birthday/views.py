from typing import Any
from datetime import date, datetime

from .forms import BirthdayForm
from .models import Birthday
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.urls import reverse_lazy


def calculate_birthday_countdown(birthday_str: str) -> int:
    birthday = datetime.strptime(str(birthday_str), "%Y-%m-%d").date()
    today = date.today()
    
    next_birthday = birthday.replace(year=today.year)
    
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)
    
    return (next_birthday - today).days


class BirthdayMixin:
    model = Birthday


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = "birthday/birthday.html"


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayListView(ListView):
    model = Birthday
    ordering = "id"
    paginate_by = 10


class BirthdayDetailView(DetailView):
    model = Birthday
    template_name_suffix = "_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["birthday_countdown"] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass
