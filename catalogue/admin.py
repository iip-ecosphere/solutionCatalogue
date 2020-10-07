from django.contrib import admin

from .models import Component, Task

from django import forms

#class ComponentForm(forms.ModelForm):
#    task = forms.ModelMultipleChoiceField(queryset=Task.objects, widget=forms.CheckboxSelectMultiple(), required=False)


class TaskInline(admin.StackedInline):
    model = Task
    extra = 1

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    #form = ComponentForm
    inlines = [TaskInline]
    #exclude = ("task",)
    #filter_horizontal = ("task",)

admin.site.register(Task)
#@admin.register(Task)
#class TaskAdmin(admin.ModelAdmin):
#    inlines = [TaskInline]
