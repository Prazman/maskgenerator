import os
import cProfile


def do_cprofile(func):
    """ Decorator function for performance profiling
    """
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
    """ Get the number of lines in a file
    """
    if not os.path.isfile(filepath):
        return 0
    with open(filepath) as f:
        for i, n in enumerate(f):
            pass
        return i + 1


def clear_file(fName):
    """ Remove the content of a file 
    """
    with open(fName, "w"):
        pass
