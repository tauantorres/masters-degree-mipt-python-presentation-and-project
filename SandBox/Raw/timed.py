import time
import functools
from typing import Callable, Any, TypeVar, Tuple


T = TypeVar("T")


def timed(func: Callable[..., T]) -> Callable[..., Tuple[T, float]]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Tuple[T, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed
    return wrapper

