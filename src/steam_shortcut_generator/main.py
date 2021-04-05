import stat
from os import chmod, makedirs
from sys import stderr

import requests

from .app_info import read as read_app_info
from .app_list import get_app_name
from .desktop import DesktopFile, DesktopParser, EntryType
from .files import get_app_info, get_shortcut_dir, iter_game_ids
from .icons import store_icon
from .slug import slugify

if __name__ == "__main__":
    outputdir = get_shortcut_dir()
    app_info = read_app_info(get_app_info().open("rb").read())

    makedirs(outputdir, exist_ok=True)
    for game_id in iter_game_ids():
        try:
            name = get_app_name(game_id)
            desktop_file = DesktopFile(
                name=name,
                comment="Play this game on Steam",
                exec=f"steam steam://rungameid/{game_id}",
                icon=f"steam_icon_{game_id}",
                terminal=False,
                type=EntryType.APPLICATION,
                categories=["Game"],
            )
            path = outputdir / f"{slugify(name)}.desktop"
            parser = DesktopParser()
            desktop_file.set_config(parser)
            chmod(
                path,
                stat.S_IRWXU
                | stat.S_IRGRP
                | stat.S_IXGRP
                | stat.S_IROTH
                | stat.S_IXOTH,
            )
            with open(path, "w") as fp:
                parser.write(fp)
        except Exception as exc:
            print(
                f"error: failed to generate shortcut for appid={game_id}: {exc}",
                file=stderr,
            )
        else:
            if game_id in app_info:
                try:
                    app = app_info[game_id]
                    if app.icon_hash:
                        icon_url = f"https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/{game_id}/{app.icon_hash}.ico"
                        print(f"downloading icon from {icon_url}", file=stderr)
                        res = requests.get(icon_url)
                        store_icon(game_id, res.content)
                except Exception as exc:
                    print(
                        f"error: failed to store icon for appid={game_id} ({name=}): {exc}",
                        file=stderr,
                    )
