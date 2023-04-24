import sys

def err_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)