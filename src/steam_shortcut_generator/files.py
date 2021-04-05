import os
from itertools import count
from pathlib import Path
from typing import Iterable

import vdf


def get_steam_root() -> Path:
    if "STEAMPATH" in os.environ:
        return Path(os.environ["STEAMPATH"])
    if os.name == "posix":
        return Path.home() / ".steam/steam"
    raise FileNotFoundError(
        "failed to resolve steam root; please set STEAMPATH to the root steam directory"
    )


def get_steam_user_id() -> str:
    if "STEAMUSER" in os.environ:
        return os.environ["STEAMUSER"]
    userdata = get_steam_root() / "userdata"
    user = next(userdata.iterdir(), None)
    if not user:
        raise FileNotFoundError("failed to resolve steam user")
    return user.name


def get_app_info() -> Path:
    return get_steam_root() / "appcache/appinfo.vdf"


def get_share_dir() -> Path:
    return Path.home() / ".local/share"


def get_library_folders() -> Path:
    return get_steam_root() / "steamapps/libraryfolders.vdf"


def iter_library_folders() -> Iterable[Path]:
    with open(get_library_folders(), "r") as fp:
        data = vdf.parse(fp)
        library_folders = data["LibraryFolders"]
        for i in count(start=1):
            key = str(i)
            if key not in library_folders:
                break
            yield Path(library_folders[key])


_MANIFEST_SUFFIX = "appmanifest_"


def iter_game_ids() -> Iterable[str]:
    for library_folder in iter_library_folders():
        app_folder = library_folder / "steamapps"
        for file in app_folder.iterdir():
            if not file.name.startswith(_MANIFEST_SUFFIX):
                continue
            yield file.with_suffix("").name[len(_MANIFEST_SUFFIX) :]


def get_shortcut_dir() -> Path:
    return get_share_dir() / "applications/steam"


if __name__ == "__main__":
    print(list(iter_game_ids()))
