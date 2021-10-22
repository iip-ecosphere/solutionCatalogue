from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Count

from .models import (
    Component,
    BaseData,
    ApplicationProfile,
    Use,
    Contact,
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
from .models.logging import SearchLog, ComponentLog
from .utils import is_admin, is_admin_or_mod, get_mod_emails


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
    raw_id_fields = ("created_by",)
    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"

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
        return Component.objects.filter(created_by=request.user).filter(
            is_deleted=False
        )

    def save_model(self, request, obj, form, change):
        # add component owner on creation
        if not change:
            obj.created_by = request.user
        if not is_admin_or_mod(request):
            if not change or obj.approved:
                # send notification on new or previously approved components
                self.send_approve_notification_mods(obj, request)
            # reset approval on change by user
            obj.approved = False
        elif change and obj.approved and not Component.objects.get(id=obj.id).approved:
            # send notification to user that a component was newly approved
            self.send_approve_notification_user(obj, request)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if is_admin_or_mod(request):
            super().delete_model(request, obj)
            return
        obj.is_deleted = True
        super().save_model(request, obj, None, True)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)

    def view_on_site(self, obj):
        return f'{reverse("catalogue:detail", kwargs={"pk": obj.pk})}?preview=True'

    def get_readonly_fields(self, request, obj=None):
        if is_admin_or_mod(request):
            return ()
        else:
            return ("approved",)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (
                "Optionen",
                {"fields": ("approved", "published", "allow_email")},
            ),
            # Base
            (
                BaseData._meta.verbose_name,
                {
                    "fields": (
                        "name",
                        "trl",
                        "description",
                        "url",
                    )
                },
            ),
            (None, {"classes": ("placeholder", "task_set-group"), "fields": ()}),
            # Application Profile
            (ApplicationProfile._meta.verbose_name, {"fields": ("product",)}),
            (
                None,
                {"classes": ("placeholder", "branchproven_set-group"), "fields": ()},
            ),
            (
                None,
                {
                    "classes": ("placeholder", "branchapplicable_set-group"),
                    "fields": (),
                },
            ),
            (
                None,
                {
                    "classes": ("placeholder", "corporatedivision_set-group"),
                    "fields": (),
                },
            ),
            (
                None,
                {"classes": ("placeholder", "hierarchylevel_set-group"), "fields": ()},
            ),
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
                {
                    "classes": ("placeholder", "dataanalysisprocess_set-group"),
                    "fields": (),
                },
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
            # Contact
            (
                Contact._meta.verbose_name,
                {
                    "fields": (
                        "contact_manufacturer",
                        "contact_person_name",
                        "contact_email",
                        "contact_phone",
                        "contact_address_street",
                        "contact_address_city",
                        "contact_address_zip",
                        "contact_address_country",
                        "contact_additional_info",
                    )
                },
            ),
        )
        # display certain fields for admins/mods only
        admin_only = (
            "is_deleted",
            "created_by",
        )
        if is_admin_or_mod(request):
            fieldsets[0][1]["fields"] += admin_only
        return fieldsets

    def changelist_view(self, request, extra_context=None):
        self.list_display = [
            "name",
            "approved",
            "published",
            "allow_email",
            "trl",
            "description_short",
            "get_created_by",
            "created",
            "lastmodified_at",
        ]
        self.list_display_links = ("name",)
        self.list_editable = (
            "published",
            "allow_email",
        )
        self.list_filter = ()
        # moderators can choose components for frontpage
        if is_admin_or_mod(request):
            self.list_display.insert(2, "frontpage")
            self.list_display.insert(1, "is_deleted")
            self.list_editable += ("frontpage",)
            self.list_filter += ("is_deleted",)

        return super().changelist_view(request, extra_context)

    def send_approve_notification_mods(self, instance, request):
        """Send email notification to mods for component requiring approval."""
        context = {"comp": instance, "link": request.build_absolute_uri()}
        content = render_to_string("catalogue/emails/email_approve_admin.txt", context)
        send_mail(
            subject="KI-Lösungskatalog: Lösung muss moderiert werden",
            message=content,
            from_email=settings.SENDER_EMAIL_APPROVE,
            recipient_list=get_mod_emails(),
        )

    def send_approve_notification_user(self, instance, request):
        """Send email notification to user that a component was approved."""
        context = {"comp": instance, "link": request.build_absolute_uri()}
        content = render_to_string("catalogue/emails/email_approve_user.txt", context)
        send_mail(
            subject="KI-Lösungskatalog: Lösung wurde freigegeben",
            message=content,
            from_email=settings.SENDER_EMAIL_APPROVE,
            recipient_list=[instance.created_by.email],
        )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "component_link",
        "name",
        "mail",
        "message_short",
    )
    readonly_fields = (
        "created",
        "component",
        "name",
        "mail",
        "message",
    )

    def get_queryset(self, request):
        if is_admin_or_mod(request):
            return Inquiry.objects.all()
        return Inquiry.objects.filter(component__created_by=request.user)

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


class ComponentLogInline(admin.TabularInline):
    model = ComponentLog
    ordering = ("-accessed",)
    can_delete = False
    fields = (
        "accessed",
        "component",
    )
    readonly_fields = fields
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = (
        "identifier",
        "created",
        "get_query",
        "query_result_count",
        "get_comp_count",
    )
    search_fields = (
        "query",
        "created",
        "identifier",
    )
    readonly_fields = (
        "query",
        "created",
        "identifier",
        "query_result_count",
    )
    list_filter = [
        "created",
        "query_result_count",
    ]
    inlines = [ComponentLogInline]

    @admin.display(description=SearchLog._meta.get_field("query").verbose_name)
    def get_query(self, obj):
        return mark_safe(f"<a href='{obj.query}'>{obj.query}</a>")

    def get_queryset(self, request):
        qs = super(SearchLogAdmin, self).get_queryset(request)
        return qs.annotate(comp_count=Count("componentlog"))

    @admin.display(description=ComponentLog._meta.verbose_name, ordering="comp_count")
    def get_comp_count(self, obj):
        return obj.comp_count


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
        return mark_safe(f"<nobr>{', '.join(r)}</nobr>")

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
