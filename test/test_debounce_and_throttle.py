from time import sleep

from loguru import logger

from home_guardian.common.debounce_throttle import debounce, throttle


def test_debounce() -> None:
    call_count: int = 3
    try:
        while call_count > 0:
            debounce_function()
            call_count -= 1
    except Exception:
        assert False, "Failed to test debounce_function()"
    sleep(2)


def test_throttle() -> None:
    call_count: int = 5
    try:
        while call_count > 0:
            throttle_function()
            call_count -= 1
            sleep(0.24)
    except Exception:
        assert False, "Failed to test throttle_function()"


@debounce(1)
def debounce_function() -> None:
    logger.warning("'debounce_function' was called")


@throttle(0.25)
def throttle_function() -> None:
    logger.warning("'throttle_function' was called")
