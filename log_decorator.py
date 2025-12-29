from functools import wraps
from typing import Callable


def logger(verbose: bool = False):
    """
    If verbose is None, they are read from the current context at CALL TIME.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if verbose:
                print("\n" + "-" * 20 + f"Calling: {func.__name__}" + "-" * 20)
                print(f"Args:{args}")
                print(f"Kwargs:{kwargs}")
                print("-" * 50 + "\n")
            return func(*args, **kwargs)

        return wrapper

    return decorator
