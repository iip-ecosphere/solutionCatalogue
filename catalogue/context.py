from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from django.http import request


def base_context_processor(r: "request") -> Dict[str, str]:
    return {"BASE_URL": r.build_absolute_uri("/").rstrip("/")}
