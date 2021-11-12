import datetime
import os
from time import sleep

# noinspection PyPackageRequirements
import cv2.cv2 as cv2
from loguru import logger

from home_guardian.common.debounce_throttle import throttle
from home_guardian.configuration.thread_pool_configuration import executor
from home_guardian.function_collection import get_data_dir, get_resources_dir
from home_guardian.message.email import send_email
from home_guardian.repository.detected_face_repository import save
from home_guardian.repository.model.detected_face import DetectedFace

_detected_face_dir = f"{get_data_dir()}/detection"
os.makedirs(_detected_face_dir, exist_ok=True)
logger.warning(f"Made the directory, _detected_face_dir: {_detected_face_dir}")


def detect_and_take_photo() -> None:
    """
    Detect and take photo.
    :return: when exception is raised, return None.
    """
    face = cv2.CascadeClassifier(
        f"{get_resources_dir()}/haarcascade_frontalface_alt2.xml"
    )
    try:
        capture = cv2.VideoCapture(0)
    except Exception as e:
        logger.error("Exception raised while capturing video!", e)
        return
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


@throttle(3)
def save_capture(frame) -> None:
    logger.debug(f"type of frame: {type(frame)}")
    executor.submit(async_save_capture, frame)


@logger.catch
def async_save_capture(frame) -> None:
    picture_path = (
        f"{_detected_face_dir}"
        f"/detected_face_{datetime.datetime.now().__str__().replace(':', '_')}.jpeg"
    )
    cv2.imwrite(picture_path, frame)
    detected_face: DetectedFace = save(picture_path)
    logger.info(
        "Saved picture, picture_path: {}, detected_face: {}",
        picture_path,
        detected_face,
    )
    render_dict: dict = {
        "subject": "Detected face",
        "content": "Attention, detected face, please take actions if necessary.",
        "warning_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content_id": f"detected_face_{detected_face}",
    }
    send_email(
        render_dict["subject"],
        "security_warning.html",
        render_dict,
        detected_face.picture_path,
    )
