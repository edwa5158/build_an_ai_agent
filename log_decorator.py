
def logger(debug_mode: bool = False, verbose: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if debug_mode or verbose:
                print(f"Calling: {func.__name__}")
                print(f"Args: {args}")
                print(f"Kwargs: {kwargs}")
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator