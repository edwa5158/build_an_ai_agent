import contextvars
from dataclasses import dataclass
from functools import wraps
from typing import Callable


@dataclass(frozen=True)
class LogOptions:
    verbose: bool = False


_LOG_OPTIONS: contextvars.ContextVar[LogOptions] = contextvars.ContextVar(
    "LOG_OPTIONS", default=LogOptions()
)


def set_log_options(*, verbose: bool = False) -> None:
    _LOG_OPTIONS.set(LogOptions( verbose))


def get_log_options() -> LogOptions:
    return _LOG_OPTIONS.get()


def logger(verbose: bool = False):
    """
    If verbose is None, they are read from the current context at CALL TIME.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            opts = get_log_options()
            effective_verbose = opts.verbose if not verbose else verbose

            if effective_verbose:
                print("\n" + "-" * 20 + f"Calling: {func.__name__}" + "-" * 20)
                print(f"Args:{args}")
                print(f"Kwargs:{kwargs}")
                print("-" * 50 + "\n")
            return func(*args, **kwargs)

        return wrapper

    return decorator
