from configparser import ConfigParser, RawConfigParser
from dataclasses import dataclass, field
from enum import Enum
from io import FileIO
from sys import stderr
from typing import List, Optional

_SECTION_NAME = "Desktop Entry"


class EntryType(str, Enum):
    APPLICATION = "Application"


@dataclass
class DesktopFile:
    name: str
    exec: str
    icon: str
    terminal: bool
    type: EntryType
    categories: List[str] = field(default_factory=lambda: [])
    comment: Optional[str] = None

    def set_config(self, config: ConfigParser):
        if not config.has_section(_SECTION_NAME):
            config.add_section(_SECTION_NAME)
        config.set(_SECTION_NAME, "Name", self.name)
        config.set(_SECTION_NAME, "Exec", self.exec)
        config.set(_SECTION_NAME, "Icon", self.icon)
        config.set(_SECTION_NAME, "Terminal", "true" if self.terminal else "false")
        config.set(_SECTION_NAME, "Type", self.type.value)
        config.set(_SECTION_NAME, "Categories", ";".join(self.categories) + ";")
        if self.comment is not None:
            config.set(_SECTION_NAME, "Comment", self.comment)


class DesktopParser(ConfigParser):
    def optionxform(self, optionstr: str) -> str:
        return optionstr

    def write(self, fp, space_around_delimiters=False) -> None:
        return super().write(fp, space_around_delimiters=space_around_delimiters)


if __name__ == "__main__":
    f = DesktopFile(
        name="Airport Madness 3D",
        comment="Play this game on Steam",
        exec="steam steam://rungameid/445770",
        icon="steam_icon_445770",
        terminal=False,
        type=EntryType.APPLICATION,
        categories=["Game"],
    )
    parser = DesktopParser()
    f.set_config(parser)
    parser.write(stderr)
