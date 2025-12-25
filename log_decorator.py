from dataclasses import dataclass
import contextvars
from functools import wraps

@dataclass(frozen=True)
class LogOptions:
    debug_mode: bool = False
    verbose: bool = False


_LOG_OPTIONS: contextvars.ContextVar[LogOptions] = contextvars.ContextVar(
    "LOG_OPTIONS", default=LogOptions()
)

def set_log_options(*, debug_mode: bool = False, verbose: bool = False)-> None:
    _LOG_OPTIONS.set(LogOptions(debug_mode, verbose))

def get_log_options() -> LogOptions:
    return _LOG_OPTIONS.get()

def logger(debug_mode: bool = False, verbose: bool = False):
    """
    If debug_mode/verbose are None, they are read from the current context at CALL TIME.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            opts = get_log_options()
            effective_debug = opts.debug_mode if not debug_mode else debug_mode
            effective_verbose = opts.verbose if not verbose else verbose
            
            if effective_debug or effective_verbose:
                print("\n" + "-" * 20 + f"Calling: {func.__name__}"+ "-" * 20)
                print(f"Args:{args}")
                print(f"Kwargs:{kwargs}")
                print("-"*50 + "\n")
            return func(*args, **kwargs)
        return wrapper

    return decorator
