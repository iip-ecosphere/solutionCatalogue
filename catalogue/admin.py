from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

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
from .models.users import Profile

from nested_admin import nested


class SourceInline(nested.NestedStackedInline):
    model = Source
    verbose_name = ""
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class TechnicalSpecificationInline(nested.NestedStackedInline):
    class DAProcessInline(nested.NestedStackedInline):
        model = DataAnalysisProcess
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    model = TechnicalSpecification
    verbose_name = ""
    inlines = [DAProcessInline]
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class RequirementsInline(nested.NestedStackedInline):
    model = Requirements
    verbose_name = ""
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class UseInline(nested.NestedStackedInline):
    model = Use
    verbose_name = ""
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class ApplicationProfileInline(nested.NestedStackedInline):
    class BranchProvenInline(nested.NestedStackedInline):
        model = BranchProven
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    class BranchApplicableInline(nested.NestedStackedInline):
        model = BranchApplicable
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    model = ApplicationProfile
    verbose_name = ""
    inlines = [BranchProvenInline, BranchApplicableInline]
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class BaseDataInline(nested.NestedStackedInline):
    class TaskInline(nested.NestedStackedInline):
        model = Task
        extra = 0
        min_num = 1
        inline_classes = ("grp-open",)

    model = BaseData
    extra = 0
    min_num = 1
    verbose_name = ""
    inlines = [TaskInline]
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


@admin.register(Component)
class ComponentAdmin(nested.NestedModelAdmin):
    exclude = ("created_by",)
    list_display = (
        "id",
        "basedata_name",
        "published",
        "created",
        "created_by",
        "lastmodified_at",
    )
    # list_editable = ("published",)
    inlines = [
        BaseDataInline,
        ApplicationProfileInline,
        UseInline,
        RequirementsInline,
        TechnicalSpecificationInline,
        SourceInline,
    ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Component.objects.all()
        return Component.objects.filter(created_by=request.user)

    def basedata_name(self, obj):
        return obj.basedata.name

    basedata_name.short_description = "Name"


# @admin.register(User)
# class ModeratorUserAdmin(UserAdmin):
#     def get_readonly_fields(self, request, obj=None):
#         if not request.user.is_superuser:
#             return ["username", "date_joined", "last_login", "is_superuser", "is_staff", "user_permissions"]
#         return []
#
#     def get_queryset(self, request):
#         if request.user.is_superuser:
#             return User.objects.all()
#         return User.objects.filter(groups__name__in=['Autoren'])


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profil"
    fk_name = "user"
    inline_classes = ("grp-collapse grp-open",)


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(groups__name__in=["Autoren"])

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return [
                "username",
                "date_joined",
                "last_login",
                "is_superuser",
                "is_staff",
                "user_permissions",
                "groups",
            ]
        return []


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
