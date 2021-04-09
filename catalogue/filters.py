from django import forms
from django.db.models import Q, Count
import django_filters

from .models import (
    Component,
    TRLChoices,
    TaskChoices,
    ProcessChoices,
    BaseData,
    Task,
    Process,
    BranchChoices,
    BranchProven,
    BranchApplicable,
    HierarchyLevel,
    HierarchyLevelChoices,
    CorporateDivision,
    CorporateDivisionChoices,
    DataAnalysisProcess,
    DAProcessChoices,
    Licenses,
    LicenseChoices,
    RealtimeChoices,
    TechnicalSpecification,
)


class ComponentFilterBase(django_filters.FilterSet):
    combined = django_filters.CharFilter(
        field_name=["basedata__name", "basedata__description"],
        label="Name / Beschreibung",
        method="combined_filter",
    )
    # basedata__name = django_filters.CharFilter(lookup_expr="icontains", label="Name")
    # basedata__description = django_filters.CharFilter(lookup_expr="icontains", label="Beschreibung")
    basedata__task__name = django_filters.MultipleChoiceFilter(
        label=Task._meta.verbose_name,
        choices=TaskChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    applicationprofile__branchproven__name = django_filters.MultipleChoiceFilter(
        label=BranchProven._meta.verbose_name,
        choices=BranchChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    applicationprofile__branchapplicable__name = django_filters.MultipleChoiceFilter(
        label=BranchApplicable._meta.verbose_name,
        choices=BranchChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Component
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.add_count_to_facet("basedata__trl")

    def get_facet_counts(self, field):
        qs = self.filter_queryset(self.queryset) if self.is_valid() else self.queryset
        facet_counts = qs.values(field).annotate(count=Count(field))
        return {x[field]: x["count"] for x in facet_counts}

    def add_count_to_facet(self, field):
        counts = self.get_facet_counts(field)
        self.form.fields[field].choices = [
            (x, f"{y} ({counts.get(x, 0)})") for x, y in self.form.fields[field].choices
        ]

    @property
    def qs(self):
        return super().qs.filter(published=True)

    @staticmethod
    def combined_filter(queryset, name, value):
        # TODO: use postgres full text search
        q = Q()
        for n in name:
            q |= Q(**{f"{n}__icontains": value})
        return queryset.filter(q)


class ComponentFilter(ComponentFilterBase):
    basedata__trl = django_filters.MultipleChoiceFilter(
        label=BaseData._meta.get_field("trl").verbose_name,
        choices=TRLChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    applicationprofile__process__name = django_filters.MultipleChoiceFilter(
        label=Process._meta.verbose_name,
        choices=ProcessChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    applicationprofile__hierarchylevel__name = django_filters.MultipleChoiceFilter(
        label=HierarchyLevel._meta.verbose_name,
        choices=HierarchyLevelChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    applicationprofile__corporatedivision__name = django_filters.MultipleChoiceFilter(
        label=CorporateDivision._meta.verbose_name,
        choices=CorporateDivisionChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    technicalspecification__dataanalysisprocess__name = (
        django_filters.MultipleChoiceFilter(
            label=DataAnalysisProcess._meta.verbose_name,
            choices=DAProcessChoices.choices[1:],
            widget=forms.CheckboxSelectMultiple,
        )
    )
    technicalspecification__realtime_processing = django_filters.MultipleChoiceFilter(
        label=TechnicalSpecification._meta.get_field(
            "realtime_processing"
        ).verbose_name,
        choices=RealtimeChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    technicalspecification__licenses__name = django_filters.MultipleChoiceFilter(
        label=Licenses._meta.verbose_name,
        choices=LicenseChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
