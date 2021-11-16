import os
from pathlib import Path
from typing import Optional, List, Union

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=BASE_DIR / ".env")


def ENV_BOOL(name: str, default: bool = False) -> bool:
    val = os.getenv(name, str(default)).lower()
    if val in ["true", "yes", "1"]:
        return True
    elif val in ["false", "no", "0"]:
        return False
    else:
        return default


def ENV_STR(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name, default)


def ENV_INT(name: str, default: Optional[Union[int, str]] = None) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def ENV_LIST(
    name: str, separator: str = ",", default: Optional[List[str]] = None
) -> List[str]:
    if default is None:
        default = []

    if name not in os.environ:
        return default
    return os.environ[name].split(separator)
