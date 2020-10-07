from django.contrib import admin

from .models import Component, Task, ApplicationProfile, BranchProven, BranchApplicable

import nested_admin

from django import forms

# class ComponentForm(forms.ModelForm):
#    task = forms.ModelMultipleChoiceField(queryset=Task.objects, widget=forms.CheckboxSelectMultiple(), required=False)


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
    inlines = [BranchProvenInline, BranchApplicableInline]
    can_delete = False
    inline_classes = ("grp-collapse grp-open",)
    # classes = ['collapse']


@admin.register(Component)
class ComponentAdmin(nested_admin.NestedModelAdmin):
    class TaskInline(nested_admin.NestedStackedInline):
        model = Task
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    # form = ComponentForm
    inlines = [TaskInline, ApplicationProfileInline]
    # exclude = ("task",)
    # filter_horizontal = ("task",)


# admin.site.register(Task)
# admin.site.register(ApplicationProfile)
