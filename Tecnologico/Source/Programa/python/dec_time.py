import time

def TIME(func):
    '''Decorator para avaliar o tempo de execução da função'''
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__}: {end_time - start_time:.6f}")
        return result
    return wrapper