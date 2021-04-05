from dataclasses import dataclass
from typing import Dict, Optional, Tuple


def read_bytes(data: bytes, count: int, pos: int = 0) -> Tuple[bytes, int]:
    return data[pos : pos + count], pos + count


def read_uint32(data: bytes, pos: int = 0) -> Tuple[int, int]:
    _bytes, pos = read_bytes(data, count=4, pos=pos)
    return int.from_bytes(_bytes, byteorder="little", signed=False), pos


_FIELD_APP_ID = b"\x02appid\x00"
_FIELD_CLIENT_ICON = b"\x01clienticon\x00"
_FIELD_NAME = b"\x01name\x00"


@dataclass
class App:
    id: int
    name: Optional[str] = None
    icon_hash: Optional[str] = None


def read_key_value(data: bytes, key: bytes, pos: int) -> str:
    key = key
    idx = data.index(key, pos)
    start = idx + len(key)
    end = data.index(b"\0", start)
    return data[start:end].decode("utf-8")


def read(data: bytes) -> Dict[str, App]:
    res: Dict[str, App] = {}
    idx = data.find(_FIELD_APP_ID)
    while idx != -1:
        # Skip 'appid' and null terminator
        pos = idx + len(_FIELD_APP_ID)
        # Read app id
        id, _ = read_uint32(data, pos)
        app = App(id=id)

        try:
            app.name = read_key_value(data, key=_FIELD_NAME, pos=idx + 1)
        except ValueError:
            pass

        try:
            app.icon_hash = read_key_value(data, key=_FIELD_CLIENT_ICON, pos=idx + 1)
        except ValueError:
            pass

        if str(id) not in res:
            res[str(id)] = app

        idx = data.find(_FIELD_APP_ID, idx + 1)
    return res


if __name__ == "__main__":
    from .files import get_app_info

    p = get_app_info()
    b = p.read_bytes()
    a = read(b)
    print(a["730"], a["255710"], a["346010"])
