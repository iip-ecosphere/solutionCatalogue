from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings

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
from .models.messages import Inquiry, Feedback, Report


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
        "name",
        "approved",
        "published",
        "allow_email",
        "trl",
        "description_short",
        "get_created_by",
        "created",
        "lastmodified_at",
    )
    list_display_links = ("name",)
    list_editable = ("published", "allow_email")
    fieldsets = (
        (
            "Optionen",
            {
                "fields": (
                    "approved",
                    "published",
                    "allow_email",
                )
            },
        ),
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

    @admin.display(
        description=Component._meta.get_field("created_by").verbose_name,
        ordering="created_by",
    )
    def get_created_by(self, obj):
        return mark_safe(
            f"""
            <a href='{reverse('admin:auth_user_change', args=(obj.created_by.id,))}'>
            {obj.created_by}
            </a>
        """
        )

    @admin.display(description=Component._meta.get_field("description").verbose_name)
    def description_short(self, obj):
        return Truncator(obj.description).chars(40)

    def get_queryset(self, request):
        if is_admin_or_mod(request):
            return Component.objects.all()
        return Component.objects.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        if not hasattr(obj, "created_by"):
            obj.created_by = request.user
        if not is_admin_or_mod(request):
            if not change or obj.approved:
                self.send_approve_notification_admin(obj, request)
            obj.approved = False
        elif obj.approved:
            self.send_approve_notification_user(obj, request)
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if is_admin_or_mod(request):
            return ()
        else:
            return ("approved",)

    def send_approve_notification_admin(self, instance, request):
        context = {
            "comp": instance,
            "link": request.build_absolute_uri()
        }
        content = render_to_string("catalogue/emails/email_approve_admin.txt", context)
        mod_emails = (
            get_user_model()
            .objects.filter(groups__name__in=["Moderatoren"])
            .values_list("email", flat=True)
        )
        send_mail(
            subject="IIP Ecosphere Lösungskatalog: Komponente muss moderiert werden",
            message=content,
            from_email=settings.SENDER_EMAIL_APPROVE,
            recipient_list=mod_emails,
        )

    def send_approve_notification_user(self, instance, request):
        context = {
            "comp": instance,
            "link": request.build_absolute_uri()
        }
        content = render_to_string("catalogue/emails/email_approve_user.txt", context)
        send_mail(
            subject="IIP Ecosphere Lösungskatalog: Komponente wurde freigegeben",
            message=content,
            from_email=settings.SENDER_EMAIL_APPROVE,
            recipient_list=[instance.created_by.email],
        )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "component_link",
        "recipient",
        "name",
        "mail",
        "message_short",
    )
    readonly_fields = (
        "created",
        "component",
        "recipient",
        "name",
        "mail",
        "message",
    )

    def get_queryset(self, request):
        if is_admin_or_mod(request):
            return Inquiry.objects.all()
        return Inquiry.objects.filter(recipient=request.user)

    @admin.display(description=Inquiry._meta.get_field("message").verbose_name)
    def message_short(self, obj):
        return Truncator(obj.message).chars(40)

    @admin.display(description=Component._meta.verbose_name, ordering="component__name")
    def component_link(self, obj):
        return mark_safe(
            f"""
            <a href='{reverse('admin:catalogue_component_change', args=(obj.component.id,))}'>
            {obj.component.name}
            </a>
        """
        )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "name",
        "mail",
        "sentiment",
        "message_short",
        "get_search_url",
    )
    readonly_fields = (
        "created",
        "name",
        "mail",
        "sentiment",
        "message",
        "search_url",
    )

    @admin.display(description=Feedback._meta.get_field("message").verbose_name)
    def message_short(self, obj):
        return Truncator(obj.message).chars(40)

    @admin.display(description=Feedback._meta.get_field("search_url").verbose_name)
    def get_search_url(self, obj):
        return mark_safe(f"""<a href='{obj.search_url}'>{obj.search_url}</a>""")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "component_link",
        "name",
        "mail",
        "message_short",
    )
    readonly_fields = (
        "created",
        "name",
        "mail",
        "message",
        "component",
    )

    @admin.display(description=Report._meta.get_field("message").verbose_name)
    def message_short(self, obj):
        return Truncator(obj.message).chars(40)

    @admin.display(description=Component._meta.verbose_name, ordering="component__name")
    def component_link(self, obj):
        return mark_safe(
            f"""
            <a href='{reverse('admin:catalogue_component_change', args=(obj.component.id,))}'>
            {obj.component.name}
            </a>
        """
        )


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

    @admin.display(description="Gruppen")
    def get_groups(self, obj):
        r = sorted([str(g) for g in obj.groups.all()])
        if obj.user_permissions.count():
            r += ["+"]
        return mark_safe("<nobr>{}</nobr>".format(", ".join(r)))

    @admin.display(
        description=Profile._meta.get_field("company").verbose_name,
        ordering="profile__company",
    )
    def get_company(self, obj):
        return obj.profile.company

    @admin.display(description=Component._meta.verbose_name_plural)
    def get_component_count(self, obj):
        return obj.profile.component_count

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
