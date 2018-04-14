import os
import cProfile


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func


def file_len(filepath):
    if not os.path.isfile(filepath):
        return 0
    with open(filepath) as f:
        for i, n in enumerate(f):
            pass
        return i + 1
