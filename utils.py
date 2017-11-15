# -*- coding: utf-8 -*-

from functools import wraps


def call_once(func):
    ret = None
    has_run = False

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal has_run
        nonlocal ret
        if not has_run:
            has_run = True
            ret = func(*args, **kwargs)
        return ret
    return wrapper
