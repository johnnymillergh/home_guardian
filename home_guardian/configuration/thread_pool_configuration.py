import time
from concurrent.futures import ThreadPoolExecutor

from loguru import logger

from home_guardian.function_collection import get_cpu_count

_max_workers = get_cpu_count()
executor = ThreadPoolExecutor(
    max_workers=_max_workers, thread_name_prefix="my_thread_pool"
)


def configure() -> None:
    """
    Configure thread pool.
    """
    logger.warning(
        f"Thread pool executor with {_max_workers} workers, executor: {executor}"
    )


def cleanup() -> None:
    """
    Clean up thread pool.
    """
    executor.shutdown()
    logger.warning(f"Thread pool executor has been shutdown: {executor}")


def simulate_get_html(times):
    time.sleep(times)
    logger.info(f"get page {times} finished")
    return times


def simulate_multi_thread() -> None:
    task1 = executor.submit(simulate_get_html, 3)
    task2 = executor.submit(simulate_get_html, 2)
    logger.info(task1.done())
    logger.info(task2.cancel())
    time.sleep(4)
    logger.info(task1.done())
    logger.info(task1.result())
