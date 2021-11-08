import asyncio
from time import time


class Setter:
    def __init__(self, initial_value=None) -> None:
        self._value = initial_value

    def get(self):
        return self._value

    def set(self, v):
        self._value = v


def debounce(delay):
    """
    Debounce decorator.

    @see Python 中的防抖与节流 https://www.bilibili.com/read/cv13257868
    """

    # 用于存储 asyncio.Task 实例，这里是闭包
    task = Setter()

    def decorator(fn):
        # Task 协程函数
        async def f(*args, **kwargs):
            # 进行休眠
            await asyncio.sleep(delay)
            # 调用函数
            f1 = fn(*args, **kwargs)
            # 支持回调函数是异步函数的情况
            if asyncio.iscoroutine(f1):
                await f1
            # 清除 task
            task.set(None)

        def wrapper(*args, **kwargs):
            # 如果 task 存在，说明在 delay 秒内调用过一次函数，此次调用应当重置计时器，因此取消先前的 Task
            if task.get() is not None:
                task.get().cancel()
            # 创建 Task 并赋值变量 task
            task.set(asyncio.create_task(f(*args, **kwargs)))

        return wrapper

    return decorator


def throttle(delay):
    """
    Throttle decorator.

    @see Python 中的防抖与节流 https://www.moyu.moe/articles/25/
    """

    # 下一次许可调用的时间，初始化为 0
    next_t = Setter(0)

    def decorator(fn):
        def wrapper(*args, **kwargs):
            # 当前时间
            now = time()
            # 若未到下一次许可调用的时间，直接返回
            if next_t.get() > now:
                return
            # 更新下一次许可调用的时间
            next_t.set(now + delay)
            # 调用函数并返回
            return fn(*args, **kwargs)

        return wrapper

    return decorator
