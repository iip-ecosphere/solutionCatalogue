from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.urls import reverse

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
    CorporateDivision,
    HierarchyLevel,
    Process,
    AIMethod,
    Licenses,
    KPI,
)
from .models.users import Profile
from .models.messages import Inquiry

from nested_admin import nested


def is_admin(request):
    return request.user.is_superuser


def is_mod(request):
    return request.user.groups.filter(name="Moderatoren").exists()


def is_admin_or_mod(request):
    return is_admin(request) or is_mod(request)


class TopNestedBase:
    extra = 0
    min_num = 1
    verbose_name = ""
    inline_classes = ("grp-collapse grp-open",)
    can_delete = False


class SubNestedBase:
    extra = 0
    min_num = 1
    inline_classes = ("grp-open",)


class SourceInline(TopNestedBase, nested.NestedStackedInline):
    model = Source


class TechnicalSpecificationInline(TopNestedBase, nested.NestedStackedInline):
    class AIMethodInline(SubNestedBase, nested.NestedStackedInline):
        model = AIMethod

    class DAProcessInline(SubNestedBase, nested.NestedStackedInline):
        model = DataAnalysisProcess

    class LicensesInline(SubNestedBase, nested.NestedStackedInline):
        model = Licenses

    model = TechnicalSpecification
    inlines = [LicensesInline, AIMethodInline, DAProcessInline]


class RequirementsInline(TopNestedBase, nested.NestedStackedInline):
    model = Requirements


class UseInline(TopNestedBase, nested.NestedStackedInline):
    class KPIInline(SubNestedBase, nested.NestedStackedInline):
        model = KPI

    model = Use
    inlines = [KPIInline]


class ApplicationProfileInline(TopNestedBase, nested.NestedStackedInline):
    class BranchProvenInline(SubNestedBase, nested.NestedStackedInline):
        model = BranchProven

    class BranchApplicableInline(SubNestedBase, nested.NestedStackedInline):
        model = BranchApplicable

    class CorporateDivisionInline(SubNestedBase, nested.NestedStackedInline):
        model = CorporateDivision

    class HierarchyLevelInline(SubNestedBase, nested.NestedStackedInline):
        model = HierarchyLevel

    class ProcessInline(SubNestedBase, nested.NestedStackedInline):
        model = Process

    model = ApplicationProfile
    inlines = [
        BranchProvenInline,
        BranchApplicableInline,
        CorporateDivisionInline,
        HierarchyLevelInline,
        ProcessInline,
    ]


class BaseDataInline(TopNestedBase, nested.NestedStackedInline):
    class TaskInline(SubNestedBase, nested.NestedStackedInline):
        model = Task

    model = BaseData
    inlines = [TaskInline]


@admin.register(Component)
class ComponentAdmin(nested.NestedModelAdmin):
    exclude = ("created_by",)
    list_display = (
        "id",
        "basedata_name",
        "published",
        "get_created_by",
        "created",
        "lastmodified_at",
    )
    list_editable = ("published",)
    inlines = [
        BaseDataInline,
        ApplicationProfileInline,
        UseInline,
        RequirementsInline,
        TechnicalSpecificationInline,
        SourceInline,
    ]

    def get_created_by(self, obj):
        return mark_safe(
            f"""
            <a href='{reverse('admin:auth_user_change', args=(obj.created_by.id,))}'>
            {obj.created_by}
            </a>
        """
        )

    get_created_by.short_description = Component._meta.get_field(
        "created_by"
    ).verbose_name
    get_created_by.admin_order_field = "created_by"

    def get_queryset(self, request):
        if is_admin_or_mod(request):
            return Component.objects.all()
        return Component.objects.filter(created_by=request.user)

    def basedata_name(self, obj):
        return mark_safe(
            f"""
            <a href='{reverse('admin:catalogue_component_change', args=(obj.id,))}'>
            {obj.basedata.name}
            </a>
        """
        )

    basedata_name.short_description = "Name"
    basedata_name.admin_order_field = "basedata__name"


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "recipient",
        "component",
        "name",
        "mail",
        "message_short",
    )
    readonly_fields = (
        "created",
        "recipient",
        "component",
        "name",
        "mail",
        "message",
    )

    def get_queryset(self, request):
        if is_admin_or_mod(request):
            return Inquiry.objects.all()
        return Inquiry.objects.filter(recipient=request.user)

    def message_short(self, obj):
        return Truncator(obj.message).chars(40)

    message_short.short_description = Inquiry._meta.get_field("message").verbose_name


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
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "get_company",
        "get_groups",
        "get_component_count",
    ]
    list_select_related = ("profile",)
    inlines = (ProfileInline,)

    def get_groups(self, obj):
        r = sorted([str(g) for g in obj.groups.all()])
        if obj.user_permissions.count():
            r += ["+"]
        return mark_safe("<nobr>{}</nobr>".format(", ".join(r)))

    get_groups.short_description = "Gruppen"

    def get_company(self, obj):
        return obj.profile.company

    get_company.short_description = Profile._meta.get_field("company").verbose_name
    get_company.admin_order_field = "profile__company"

    def get_component_count(self, obj):
        return obj.profile.component_count

    get_component_count.short_description = "Komponenten"

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def get_queryset(self, request):
        if is_admin(request):
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
