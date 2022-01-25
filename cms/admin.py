from catalogue.models import Component
from django.contrib import admin

from .models import BlogPage, Menu, StaticMenuPage


@admin.register(StaticMenuPage)
class CMSAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published", "slug", "menu", "parent", "root")
    list_display_links = ("title",)
    list_editable = ("published",)
    fields = (
        "created",
        "author",
        "title",
        "parent",
        "menu",
        "root",
        "published",
        "slug",
        "template",
        "content",
    )
    readonly_fields = ("created", "author")
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.author:
            # save author on newly created objects
            obj.author = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ("/static/admin/js/cms_admin.js",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "published",
        "slug",
        "created",
    )
    list_display_links = ("title",)
    list_editable = ("published",)
    fields = (
        "created",
        "author",
        "published",
        "title",
        "title_image",
        "slug",
        "content",
        "components",
    )
    readonly_fields = ("created", "author")
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.author:
            # save author on newly created objects
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "components":
            kwargs["queryset"] = Component.public_objects
        return super().formfield_for_manytomany(db_field, request, **kwargs)
