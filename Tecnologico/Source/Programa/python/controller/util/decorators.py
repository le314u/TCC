import time
import resource
from functools import wraps


def timed(func):
    '''Decorator para avaliar o tempo de execução da função'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__}: {end_time - start_time:.6f}s")
        return result
    return wrapper


def memory_usage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        before_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result = func(*args, **kwargs)
        after_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(f"{func.__name__}: Memory usage: {(after_memory - before_memory) / 1024.0:.3f} MB")
        return result
    return wrapper