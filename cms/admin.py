from django.contrib import admin
from .models import StaticMenuPage, Menu


@admin.register(StaticMenuPage)
class CMSAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "menu", "parent", "root")
    fields = (
        "title",
        "menu",
        "root",
        "url",
        "template",
        "parent",
        "content",
    )

    class Media:
        js = ("/static/admin/js/cms_admin.js",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass
