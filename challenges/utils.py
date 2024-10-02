from typing import Any


def obj_to_dict(obj: Any) -> dict:
    return {field.name: getattr(obj, field.name) for field in obj._meta.fields}
