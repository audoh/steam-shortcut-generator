from dataclasses import dataclass
from typing import Dict, Optional, Tuple

_FIELD_APP_ID = b"\x02appid\x00"
_FIELD_CLIENT_ICON = b"\x01clienticon\x00"
_FIELD_NAME = b"\x01name\x00"


def _read_bytes(data: bytes, count: int, pos: int = 0) -> Tuple[bytes, int]:
    return data[pos : pos + count], pos + count


def _read_uint32(data: bytes, pos: int = 0) -> Tuple[int, int]:
    _bytes, pos = _read_bytes(data, count=4, pos=pos)
    return int.from_bytes(_bytes, byteorder="little", signed=False), pos


def _read_key_uint32(data: bytes, key: bytes, pos: int = 0) -> Tuple[int, int]:
    idx = data.index(key, pos)
    pos = idx + len(key)
    return _read_uint32(data, pos)


def _read_key_utf8(data: bytes, key: bytes, pos: int = 0) -> Tuple[str, int]:
    idx = data.index(key, pos)
    start = idx + len(key)
    end = data.index(b"\0", start)
    return data[start:end].decode("utf-8"), end


@dataclass
class App:
    id: int
    name: Optional[str] = None
    icon_hash: Optional[str] = None


def read(data: bytes) -> Dict[str, App]:
    res: Dict[str, App] = {}
    pos = 0
    while True:
        try:
            id, pos = _read_key_uint32(data, _FIELD_APP_ID, pos=pos)
        except ValueError:
            break

        app = App(id=id)

        try:
            app.name, _ = _read_key_utf8(data, key=_FIELD_NAME, pos=pos)
        except ValueError:
            pass

        try:
            app.icon_hash, _ = _read_key_utf8(data, key=_FIELD_CLIENT_ICON, pos=pos)
        except ValueError:
            pass

        if str(id) not in res:
            res[str(id)] = app
    return res


if __name__ == "__main__":
    from .files import get_app_info

    p = get_app_info()
    b = p.read_bytes()
    a = read(b)
    print(a["730"], a["255710"], a["346010"])
