from io import BytesIO
from sys import stderr

import PIL.Image

from .files import get_icon_dir


def store_icon(app_id: str, data: bytes) -> None:
    data_io = BytesIO(data)
    image = PIL.Image.open(data_io)
    width, height = image.size
    image.format
    icon_dir = get_icon_dir()
    for dir in icon_dir.iterdir():
        if not dir.is_dir():
            continue
        try:
            width, height = (int(x) for x in dir.name.split("x"))
            icon_path = dir / f"apps/steam_icon_{app_id}.png"
            image.resize((width, height)).save(icon_path)
            print(f"stored icon for {app_id} at {icon_path}", file=stderr)
        except Exception:
            print(
                f"error: failed to store icon for appid={app_id}, size={width}x{height}",
                file=stderr,
            )
