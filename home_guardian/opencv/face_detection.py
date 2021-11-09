import datetime
import os
from time import sleep

import cv2.cv2 as cv2
from loguru import logger

from home_guardian.common.debounce_throttle import throttle
from home_guardian.configuration.thread_pool_configuration import executor
from home_guardian.function_collection import get_data_dir, get_resources_dir

detected_face_dir = f"{get_data_dir()}/detection"
os.makedirs(detected_face_dir, exist_ok=True)
logger.warning(f"Made the directory, detected_face_dir: {detected_face_dir}")


def detect_and_take_photo() -> None:
    face = cv2.CascadeClassifier(
        f"{get_resources_dir()}/haarcascade_frontalface_alt2.xml"
    )
    capture = cv2.VideoCapture(0)
    while True:
        return_value, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face.detectMultiScale(gray)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            save_capture(frame)
        if return_value:
            cv2.imshow("Capture Window", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        sleep(1)
    capture.release()
    cv2.destroyAllWindows()


@throttle(2)
def save_capture(frame) -> None:
    executor.submit(async_save_capture, frame)


def async_save_capture(frame) -> None:
    file_name = f"{get_data_dir()}/detection/detected_face_{datetime.datetime.now().__str__().replace(':', '_')}.jpeg"
    cv2.imwrite(file_name, frame)
    logger.info("Saved image to: {}", file_name)
