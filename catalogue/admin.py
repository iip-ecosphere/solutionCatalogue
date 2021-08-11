from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.urls import reverse

from .models import (
    Component,
    BaseData,
    ApplicationProfile,
    TechnicalSpecification,
    Use,
    Source,
    Requirements,
    Task,
    BranchProven,
    BranchApplicable,
    TechnicalSpecification,
    DataAnalysisProcess,
    CorporateDivision,
    HierarchyLevel,
    Process,
    AIMethod,
    Licenses,
    KPI,
)
from .models.users import Profile
from .models.messages import Inquiry, Feedback


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


# BaseData
class TaskInline(SubNestedBase, admin.StackedInline):
    model = Task


# ApplicationProfile
class BranchProvenInline(SubNestedBase, admin.StackedInline):
    model = BranchProven


class BranchApplicableInline(SubNestedBase, admin.StackedInline):
    model = BranchApplicable


class CorporateDivisionInline(SubNestedBase, admin.StackedInline):
    model = CorporateDivision


class HierarchyLevelInline(SubNestedBase, admin.StackedInline):
    model = HierarchyLevel


class ProcessInline(SubNestedBase, admin.StackedInline):
    model = Process


# Use
class KPIInline(SubNestedBase, admin.StackedInline):
    model = KPI


# TechnicalSpecification
class AIMethodInline(SubNestedBase, admin.StackedInline):
    model = AIMethod


class DAProcessInline(SubNestedBase, admin.StackedInline):
    model = DataAnalysisProcess


class LicensesInline(SubNestedBase, admin.StackedInline):
    model = Licenses


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    exclude = ("created_by",)
    list_display = (
        "id",
        "get_name",
        "published",
        "allow_email",
        "get_created_by",
        "created",
        "lastmodified_at",
    )
    list_editable = ("published", "allow_email")
    fieldsets = (
        (None, {"fields": ("published",)}),
        (None, {"fields": ("allow_email",)}),
        # Base
        (
            BaseData._meta.verbose_name,
            {
                "fields": (
                    "name",
                    "trl",
                    "description",
                )
            },
        ),
        (None, {"classes": ("placeholder", "task_set-group"), "fields": ()}),
        # Application Profile
        (ApplicationProfile._meta.verbose_name, {"fields": ("product",)}),
        (None, {"classes": ("placeholder", "branchproven_set-group"), "fields": ()}),
        (
            None,
            {"classes": ("placeholder", "branchapplicable_set-group"), "fields": ()},
        ),
        (
            None,
            {"classes": ("placeholder", "corporatedivision_set-group"), "fields": ()},
        ),
        (None, {"classes": ("placeholder", "hierarchylevel_set-group"), "fields": ()}),
        (None, {"classes": ("placeholder", "process_set-group"), "fields": ()}),
        # Use
        (Use._meta.verbose_name, {"fields": ("scenarios",)}),
        (None, {"classes": ("placeholder", "kpi_set-group"), "fields": ()}),
        # Technical Spec
        (
            TechnicalSpecification._meta.verbose_name,
            {
                "fields": (
                    "realtime_processing",
                    "data_formats",
                )
            },
        ),
        (None, {"classes": ("placeholder", "aimethod_set-group"), "fields": ()}),
        (
            None,
            {"classes": ("placeholder", "dataanalysisprocess_set-group"), "fields": ()},
        ),
        (None, {"classes": ("placeholder", "licenses_set-group"), "fields": ()}),
        # Requirements
        (
            Requirements._meta.verbose_name,
            {
                "fields": (
                    "protocols",
                    "it_environment",
                    "hardware_requirements",
                    "devices",
                )
            },
        ),
        # Source
        (
            Source._meta.verbose_name,
            {
                "fields": (
                    "manufacturer",
                    "contact",
                    "additional_info",
                )
            },
        ),
    )

    inlines = [
        # BaseData
        TaskInline,
        # ApplicationProfile
        BranchProvenInline,
        BranchApplicableInline,
        CorporateDivisionInline,
        HierarchyLevelInline,
        ProcessInline,
        # Use
        KPIInline,
        # TechnicalSpecification
        AIMethodInline,
        DAProcessInline,
        LicensesInline,
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

    def get_name(self, obj):
        return mark_safe(
            f"""
            <a href='{reverse('admin:catalogue_component_change', args=(obj.id,))}'>
            {obj.name}
            </a>
        """
        )

    get_name.short_description = "Name"
    get_name.admin_order_field = "name"

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "created_by"):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


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


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "name",
        "mail",
        "message_short",
        "sentiment",
        "get_search_url",
    )
    readonly_fields = (
        "created",
        "name",
        "mail",
        "message",
        "sentiment",
        "search_url",
    )

    def message_short(self, obj):
        return Truncator(obj.message).chars(40)

    def get_search_url(self, obj):
        return mark_safe(f"""<a href='{obj.search_url}'>{obj.search_url}</a>""")

    get_search_url.short_description = Feedback._meta.get_field(
        "search_url"
    ).verbose_name

    message_short.short_description = Feedback._meta.get_field("message").verbose_name


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
