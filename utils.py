# -*- coding: utf-8 -*-

from functools import wraps


def call_once(func):
    store = {
        "has_run": False,
        "return": None,
    }

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not store["has_run"]:
            store["has_run"] = True
            store["return"] = func(*args, **kwargs)
        return store["return"]
    return wrapper
