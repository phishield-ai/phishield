from datetime import timedelta


def time(*args, **kwargs):
    return int(timedelta(*args, **kwargs).total_seconds() * 1000)