import time

from loguru import logger


def elapsed_time(fn):
    def decorator(*arg, **kwarg):
        start_time = time.time()
        return_value = fn(*arg, **kwarg)
        end_time = time.time()
        logger.info(f"Elapsed time of function {fn}：{round(end_time - start_time, 4)}s")
        return return_value

    return decorator
