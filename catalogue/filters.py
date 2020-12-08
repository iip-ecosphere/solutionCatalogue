import django_filters

from .models import Component, TRLChoices, TaskChoices


class ComponentFilter(django_filters.FilterSet):
    basedata__name = django_filters.CharFilter(lookup_expr="icontains", label="Name")
    basedata__trl = django_filters.ChoiceFilter(label="TRL", choices=TRLChoices.choices)
    basedata__description = django_filters.CharFilter(lookup_expr="icontains", label="Beschreibung")
    basedata__task__name = django_filters.ChoiceFilter(label="Task", choices=TaskChoices.choices)

    class Meta:
        model = Component
        fields = []

    @property
    def qs(self):
        return super().qs.filter(published=True)