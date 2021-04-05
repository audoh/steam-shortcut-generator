from os import makedirs
from pathlib import Path
from sys import stderr

from .app_list import get_app_name
from .desktop import DesktopFile, DesktopParser, EntryType
from .files import iter_game_ids
from .slug import slugify

if __name__ == "__main__":
    outputdir = Path("./test")

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
            with open(path, "w") as fp:
                parser.write(fp)
        except Exception as exc:
            print(
                f"warning: failed to generate shortcut for appid={game_id}: {exc}",
                file=stderr,
            )
