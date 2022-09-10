import time


def timer(function_description=None):
    """Decorator that prints the runtime of the decorated function"""
    def inner_function(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            time_taken_in_secs = round(end - start, 5)
            message = "Executed `{func_name}` in {time_taken_in_secs} seconds".format(
                func_name=func.__name__,
                time_taken_in_secs=time_taken_in_secs,
            )
            if function_description is not None:
                message += " (Function description - {})".format(str(function_description))
            print(message)
            return result
        return wrapper
    return inner_function


def repeat(num_times: int):
    """Decorator that executes the decorated function `num_times` times"""
    def inner_function(func):
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return inner_function