from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import request


def is_admin(r: "request") -> bool:
    return r.user.is_superuser


def is_mod(r: "request") -> bool:
    return r.user.groups.filter(name="Moderatoren").exists()


def is_admin_or_mod(r: "request") -> bool:
    return is_admin(r) or is_mod(r)
