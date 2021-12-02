from django.contrib import admin
from .models import StaticMenuPage, Menu


@admin.register(StaticMenuPage)
class CMSAdmin(admin.ModelAdmin):
    list_display = ("published", "title", "slug", "menu", "parent", "root")
    list_display_links = ("title", )
    list_editable = ("published",)
    fields = (
        "title",
        "menu",
        "published",
        "root",
        "slug",
        "template",
        "parent",
        "content",
    )
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = ("/static/admin/js/cms_admin.js",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass
