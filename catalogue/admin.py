from django.contrib import admin

from .models import (
    BaseData,
    Component,
    Task,
    ApplicationProfile,
    BranchProven,
    BranchApplicable,
    Use,
    Requirements,
    TechnicalSpecification,
    DataAnalysisProcess,
    Source,
)

import nested_admin


class SourceInline(nested_admin.NestedStackedInline):
    model = Source
    verbose_name = ""
    verbose_name_plural = "Quelle"
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class TechnicalSpecificationInline(nested_admin.NestedStackedInline):
    class DAProcessInline(nested_admin.NestedStackedInline):
        model = DataAnalysisProcess
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    model = TechnicalSpecification
    verbose_name = ""
    verbose_name_plural = "Technische Spezifikation"
    inlines = [DAProcessInline]
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class RequirementsInline(nested_admin.NestedStackedInline):
    model = Requirements
    verbose_name = ""
    verbose_name_plural = "Vorraussetzungen"
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class UseInline(nested_admin.NestedStackedInline):
    model = Use
    verbose_name = ""
    verbose_name_plural = "Nutzen"
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class ApplicationProfileInline(nested_admin.NestedStackedInline):
    class BranchProvenInline(nested_admin.NestedStackedInline):
        model = BranchProven
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    class BranchApplicableInline(nested_admin.NestedStackedInline):
        model = BranchApplicable
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    model = ApplicationProfile
    verbose_name = ""
    verbose_name_plural = "Anwendungsprofil"
    inlines = [BranchProvenInline, BranchApplicableInline]
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class BaseDataInline(nested_admin.NestedStackedInline):
    class TaskInline(nested_admin.NestedStackedInline):
        model = Task
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    model = BaseData
    verbose_name = ""
    verbose_name_plural = "Grunddaten"
    inlines = [TaskInline]
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


@admin.register(Component)
class ComponentAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        BaseDataInline,
        ApplicationProfileInline,
        UseInline,
        RequirementsInline,
        TechnicalSpecificationInline,
        SourceInline,
    ]


# admin.site.register(Task)
# admin.site.register(ApplicationProfile)
