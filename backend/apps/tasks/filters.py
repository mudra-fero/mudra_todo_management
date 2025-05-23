import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    priority = django_filters.BaseInFilter(field_name="priority", lookup_expr="in")
    lifecycle_stage = django_filters.BaseInFilter(
        field_name="lifecycle_stage", lookup_expr="in"
    )
    start_date = django_filters.DateFilter(field_name="deadline", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="deadline", lookup_expr="lte")

    class Meta:
        model = Task
        fields = ["priority", "lifecycle_stage", "start_date", "end_date"]
