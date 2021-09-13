from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from django.http import request
    from django.db.models import QuerySet


def is_admin(r: "request") -> bool:
    """Check if user is admin"""
    return r.user.is_superuser


def is_mod(r: "request") -> bool:
    """Check if user belongs to moderators group"""
    return r.user.groups.filter(name="Moderatoren").exists()


def is_admin_or_mod(r: "request") -> bool:
    """Check if user is admin or moderator"""
    return is_admin(r) or is_mod(r)


def get_admin_emails() -> "QuerySet":
    """Get all eMail addresses of admins"""
    return (
        get_user_model()
        .objects.filter(is_superuser=True)
        .values_list("email", flat=True)
    )


def get_mod_emails() -> "QuerySet":
    """Get all eMail addresses of moderators"""
    return (
        get_user_model()
        .objects.filter(groups__name__in=["Moderatoren"])
        .values_list("email", flat=True)
    )
