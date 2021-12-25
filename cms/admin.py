from django.contrib import admin
from .models import StaticMenuPage, Menu, BlogPage
from catalogue.models import Component


@admin.register(StaticMenuPage)
class CMSAdmin(admin.ModelAdmin):
    list_display = ("published", "title", "slug", "menu", "parent", "root")
    list_display_links = ("title",)
    list_editable = ("published",)
    fields = (
        "title",
        "parent",
        "menu",
        "root",
        "published",
        "slug",
        "template",
        "content",
    )
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = ("/static/admin/js/cms_admin.js",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(BlogPage)
class BlogPageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "published",
        "slug",
        "created",
    )
    list_display_links = ("title",)
    list_editable = ("published",)
    fields = (
        "published",
        "title",
        "title_image",
        "slug",
        "template",
        "content",
        "components",
    )
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        # add component owner on creation
        obj.author = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "components":
            kwargs["queryset"] = Component.public_objects
        return super().formfield_for_manytomany(db_field, request, **kwargs)
