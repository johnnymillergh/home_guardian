import sys

from loguru import logger

from home_guardian.common.startup import StartupMode
from home_guardian.configuration.apscheduler_configuration import (
    cleanup as apscheduler_cleanup,
)
from home_guardian.configuration.thread_pool_configuration import (
    cleanup as thread_pool_cleanup,
)
from home_guardian.message.email import cleanup as email_cleanup
from home_guardian.opencv.face_collecting import collect_data
from home_guardian.opencv.face_detection import detect_and_take_photo
from home_guardian.opencv.face_training import train_data


def _main() -> None:
    """
    Main function.
    """
    startup_mode = StartupMode.value_of(sys.argv[1])
    logger.info(f"startup_mode: {startup_mode}")
    try:
        if startup_mode == StartupMode.DETECT:
            logger.info("Detecting and taking photos")
            detect_and_take_photo()
        elif startup_mode == StartupMode.COLLECT:
            logger.info("Collecting data")
            collect_data(sys.argv[2])
        elif startup_mode == StartupMode.TRAIN:
            logger.info("Training data")
            train_data()
    finally:
        logger.warning("Cleaning up…")
        thread_pool_cleanup()
        email_cleanup()
        apscheduler_cleanup()


if __name__ == "__main__":
    _main()
