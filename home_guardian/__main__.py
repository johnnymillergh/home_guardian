from loguru import logger

from home_guardian.configuration.thread_pool_configuration import (
    cleanup as thread_pool_cleanup,
)
from home_guardian.opencv.face_detection import detect_and_take_photo


def _main() -> None:
    """
    Main function.
    """
    try:
        detect_and_take_photo()
    finally:
        # Cleanup procedures
        logger.warning("Cleaning up…")
        thread_pool_cleanup()


if __name__ == "__main__":
    _main()
