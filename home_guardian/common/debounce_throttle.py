from threading import Timer
from time import time

from loguru import logger


def debounce(interval: float):
    """
    Decorator that will postpone a functions
    execution until after wait seconds
    have elapsed since the last time it was invoked.
    https://gist.github.com/walkermatt/2871026

    :param interval: interval time in seconds
    """

    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
                logger.debug(f"Called debounced function: {fn}")

            try:
                debounced.t.cancel()
                logger.debug(f"Cancelled calling debounced function: {fn}")
            except AttributeError:
                pass
            debounced.t = Timer(interval, call_it)
            debounced.t.start()

        return debounced

    return decorator


class Wrapper:
    def __init__(self, initial_value=None) -> None:
        self._value = initial_value

    def get(self):
        return self._value

    def set(self, v):
        self._value = v


def throttle(interval: float):
    """
    Throttle decorator.
    Python 中的防抖与节流 https://www.bilibili.com/read/cv13257868/
    Python 中的防抖与节流 https://www.moyu.moe/articles/25/

    :param interval: interval time in seconds
    """

    # 下一次许可调用的时间，初始化为 0
    next_t = Wrapper(0)

    def decorator(fn):
        def throttled(*args, **kwargs):
            # 当前时间
            now = time()
            # 若未到下一次许可调用的时间，直接返回
            if next_t.get() > now:
                logger.debug(f"Skipped throttled call, function: {fn}")
                return
            # 更新下一次许可调用的时间
            next_t.set(now + interval)
            # 调用函数并返回
            logger.debug(f"Called throttled function: {fn}")
            return fn(*args, **kwargs)

        return throttled

    return decorator
