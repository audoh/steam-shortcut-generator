import json
from os import makedirs
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, TypedDict

import appdirs
import requests

_APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
_CACHE_DIR = Path(
    appdirs.user_cache_dir(appname="steam-shortcut-generator", appauthor="audoh")
)
_CACHE_PATH = _CACHE_DIR / "applist.json"
_MEM_MAP: Optional[Dict[str, str]] = None
_fetched = False


class _App(TypedDict):
    appid: str
    name: str


class NoKnownAppError(Exception):
    pass


def _read_applist(_json: Dict[str, Any]) -> Iterable[_App]:
    return _json["applist"]["apps"]


def _refetch() -> Dict[str, str]:
    # Fetch from Steam API
    res = requests.get(_APP_LIST_URL)
    res.raise_for_status()
    _json = res.json()

    # Convert to mapping
    _list = _read_applist(_json)
    _dict = {str(app["appid"]): app["name"] for app in _list}

    # Cache in memory and FS
    makedirs(_CACHE_PATH.parent.absolute(), exist_ok=True)
    with _CACHE_PATH.open("w") as fp:
        json.dump(_dict, fp)
    return _dict


def _read_cache() -> Dict[str, str]:
    with _CACHE_PATH.open("r") as fp:
        return json.load(fp)


def _ensure_cache_read() -> None:
    global _MEM_MAP
    if _MEM_MAP is None:
        try:
            _MEM_MAP = _read_cache()
        except Exception:
            pass


def _ensure_latest_fetched() -> None:
    global _MEM_MAP
    # Don't fetch more than once per session
    if _fetched:
        return
    try:
        _MEM_MAP = _refetch()
    except Exception:
        pass


def get_app_name(id: str) -> str:
    id = str(id)
    _ensure_cache_read()

    if _MEM_MAP is None or id not in _MEM_MAP:
        _ensure_latest_fetched()

    if _MEM_MAP is None:
        raise FileNotFoundError(f"no mem map")
    if id not in _MEM_MAP:
        raise NoKnownAppError(f"no known app with {id=}")

    return _MEM_MAP[id]
