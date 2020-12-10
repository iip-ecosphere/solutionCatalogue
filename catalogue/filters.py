from django import forms
from django.db.models import Q, Count
import django_filters

from .models import Component, TRLChoices, TaskChoices


class ComponentFilter(django_filters.FilterSet):
    combined = django_filters.CharFilter(
        field_name=["basedata__name", "basedata__description"],
        label="Name / Beschreibung",
        method="combined_filter",
    )
    # basedata__name = django_filters.CharFilter(lookup_expr="icontains", label="Name")
    # basedata__description = django_filters.CharFilter(lookup_expr="icontains", label="Beschreibung")
    basedata__trl = django_filters.MultipleChoiceFilter(
        label="TRL", choices=TRLChoices.choices[1:], widget=forms.CheckboxSelectMultiple
    )
    basedata__task__name = django_filters.MultipleChoiceFilter(
        label="Task", choices=TaskChoices.choices
    )

    class Meta:
        model = Component
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_count_to_facet("basedata__trl")

    def get_facet_counts(self, field):
        qs = self.filter_queryset(self.queryset) if self.is_valid() else self.queryset
        facet_counts = qs.values(field).annotate(count=Count(field))
        return {x[field]: x["count"] for x in facet_counts}

    def add_count_to_facet(self, field):
        counts = self.get_facet_counts(field)
        self.form.fields[field].choices = [
            (x, y + f" ({counts.get(x, 0)})")
            for x, y in self.form.fields[field].choices
        ]

    @property
    def qs(self):
        return super().qs.filter(published=True)

    def combined_filter(self, queryset, name, value):
        # TODO: use postgres full text search
        q = Q()
        for n in name:
            q |= Q(**{f"{n}__icontains": value})
        return queryset.filter(q)
