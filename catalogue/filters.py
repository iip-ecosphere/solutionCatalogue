from django import forms
from django.db.models import Q, Count

import django_filters

from . import COMPONENT_RELATED_FIELDS
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
    class Meta:
        model = Component
        fields = []

    q = django_filters.CharFilter(
        field_name=["name", "description"],
        label="Name / Beschreibung",
        method="combined_filter",
    )
    # basedata__name = django_filters.CharFilter(lookup_expr="icontains", label="Name")
    # basedata__description = django_filters.CharFilter(lookup_expr="icontains", label="Beschreibung")
    task__name = django_filters.MultipleChoiceFilter(
        label=Task._meta.verbose_name,
        choices=TaskChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    branchproven__name = django_filters.MultipleChoiceFilter(
        label=BranchProven._meta.verbose_name,
        choices=BranchChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    branchapplicable__name = django_filters.MultipleChoiceFilter(
        label=BranchApplicable._meta.verbose_name,
        choices=BranchChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )

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
        return (
            super()
                .qs.filter(published=True)
                .prefetch_related(
                "task_set",
                "process_set",
            )
        )

    @staticmethod
    def combined_filter(queryset, name, value):
        # TODO: use postgres full text search
        q = Q()
        for n in name:
            q |= Q(**{f"{n}__icontains": value})
        return queryset.filter(q)


class ComponentFilterFrontPage(ComponentFilterBase):
    @property
    def qs(self):
        return super().qs[:3]


class ComponentFilter(ComponentFilterBase):
    trl = django_filters.MultipleChoiceFilter(
        label=BaseData._meta.get_field("trl").verbose_name,
        choices=TRLChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    process__name = django_filters.MultipleChoiceFilter(
        label=Process._meta.verbose_name,
        choices=ProcessChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    hierarchylevel__name = django_filters.MultipleChoiceFilter(
        label=HierarchyLevel._meta.verbose_name,
        choices=HierarchyLevelChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    name = django_filters.MultipleChoiceFilter(
        label=CorporateDivision._meta.verbose_name,
        choices=CorporateDivisionChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    dataanalysisprocess__name = (
        django_filters.MultipleChoiceFilter(
            label=DataAnalysisProcess._meta.verbose_name,
            choices=DAProcessChoices.choices[1:],
            widget=forms.CheckboxSelectMultiple,
        )
    )
    realtime_processing = django_filters.MultipleChoiceFilter(
        label=TechnicalSpecification._meta.get_field(
            "realtime_processing"
        ).verbose_name,
        choices=RealtimeChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )
    licenses__name = django_filters.MultipleChoiceFilter(
        label=Licenses._meta.verbose_name,
        choices=LicenseChoices.choices[1:],
        widget=forms.CheckboxSelectMultiple,
    )


class ComponentComparisonFilter(django_filters.FilterSet):
    class Meta:
        model = Component
        fields = []

    id = django_filters.ModelMultipleChoiceFilter(
        to_field_name="id",
        queryset=Component.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    @property
    def qs(self):
        return (
            super()
            .qs.filter(published=True)
            #.select_related(*COMPONENT_RELATED_FIELDS)
            # .prefetch_related(
            #     "basedata__task_set",
            #     "applicationprofile__corporatedivision_set",
            #     "applicationprofile__hierarchylevel_set",
            #     "applicationprofile__process_set",
            #     "applicationprofile__branchproven_set",
            #     "applicationprofile__branchapplicable_set",
            #     "use__kpi_set",
            #     "technicalspecification__aimethod_set",
            #     "technicalspecification__dataanalysisprocess_set",
            #     "technicalspecification__licenses_set",
            # )
        )
