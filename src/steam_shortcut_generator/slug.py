import re


def slugify(name: str) -> str:
    name = name.lower()
    dashed = re.compile(r"[\s\.]")
    name = re.sub(dashed, "-", name)
    excluded = re.compile(r"[^a-z0-9-]")
    name = re.sub(excluded, "", name)
    return name
