import datetime
import os
from time import sleep

import cv2.cv2 as cv2
import numpy as np
from loguru import logger

from home_guardian.common.debounce_throttle import throttle
from home_guardian.configuration.application_configuration import application_conf
from home_guardian.configuration.thread_pool_configuration import executor
from home_guardian.function_collection import get_training_datasets_dir
from home_guardian.opencv.detector_recognizer import face_detector
from home_guardian.opencv.threading import VideoCaptureThreading

_training_datasets_dir = f"{get_training_datasets_dir()}"
os.makedirs(_training_datasets_dir, exist_ok=True)
logger.warning(f"Made the directory, _training_datasets_dir: {_training_datasets_dir}")

_headless: bool = application_conf.get_bool("headless")


def collect_data(username: str) -> None:
    """
    Detect and take photo.
    :return: when exception is raised, return None.
    """
    try:
        vid_cap: VideoCaptureThreading = VideoCaptureThreading(0).start()
    except Exception as e:
        logger.error("Exception raised while starting video capture thread!", e)
        return
    while True:
        grabbed, frame = vid_cap.read()
        if not _headless:
            cv2.imshow("Collect Face Photo", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        if not grabbed:
            break
        _process_frame(frame, username)
        sleep(0.04)
    vid_cap.stop()
    cv2.destroyAllWindows()


@throttle(3)
def _process_frame(frame: np.ndarray, username: str) -> None:
    executor.submit(_async_process_frame, frame, username)


@logger.catch
def _async_process_frame(frame: np.ndarray, username: str) -> None:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_frame)
    for (x, y, w, h) in faces:
        logger.info(
            "Detected face, axis(x,y) = ({},{}), width = {} px, h = {} px", x, y, w, h
        )
        _save_frame(frame, username)


def _save_frame(frame, username: str) -> None:
    """
    Save frame.

    :param frame: The frame
    """
    username_path = f"{_training_datasets_dir}/{username}"
    if os.path.exists(username_path) is False:
        os.makedirs(username_path, exist_ok=True)
    picture_path = (
        f"{username_path}"
        f"/detected_face_{datetime.datetime.now().__str__().replace(':', '_')}.jpg"
    )
    cv2.imwrite(picture_path, frame)
    logger.info("Saved picture, picture_path: {}", picture_path)
