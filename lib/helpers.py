import sys


def fprint(file, *args, **kwargs):
    print(*args, file=file, **kwargs)


def err_print(*args, **kwargs):
    fprint(sys.stderr, *args, **kwargs)
