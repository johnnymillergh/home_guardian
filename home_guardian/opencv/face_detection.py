import datetime
import os

import cv2.cv2 as cv2
from cv2.cv2 import CascadeClassifier
from cv2.mat_wrapper import Mat
from loguru import logger

from home_guardian.common.debounce_throttle import throttle
from home_guardian.configuration.application_configuration import application_conf
from home_guardian.configuration.thread_pool_configuration import executor
from home_guardian.function_collection import get_data_dir
from home_guardian.message.email import send_email
from home_guardian.opencv.haar_model import haarcascade_frontalface_default
from home_guardian.opencv.threading import VideoCaptureThreading
from home_guardian.repository.detected_face_repository import save
from home_guardian.repository.model.detected_face import DetectedFace
from home_guardian.repository.model.trained_face import TrainedFace
from home_guardian.repository.trained_face_repository import get_by_id

_detected_face_dir = f"{get_data_dir()}/detection"
os.makedirs(_detected_face_dir, exist_ok=True)
logger.warning(f"Made the directory, _detected_face_dir: {_detected_face_dir}")

_headless: bool = application_conf.get_bool("headless")

face = CascadeClassifier(haarcascade_frontalface_default)
_recognizer = cv2.face.LBPHFaceRecognizer_create()
try:
    _recognizer.read(f"{get_data_dir()}/trainer.yml")
except Exception:
    logger.exception("Cannot read trainer.yml!")


def detect_and_take_photo() -> None:
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
            cv2.imshow("Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        if not grabbed:
            break
        process_frame(frame)
    vid_cap.stop()
    cv2.destroyAllWindows()


@throttle(3)
def process_frame(frame: Mat) -> None:
    executor.submit(async_process_frame, frame)


@logger.catch
def async_process_frame(frame: Mat) -> None:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray_frame)
    for (x, y, w, h) in faces:
        logger.info(
            "Detected face, axis(x,y) = ({},{}), width = {} px, h = {} px", x, y, w, h
        )
        # recognize? deep learned model predict keras tensorflow pytorch scikit learn
        label, confidence = _recognizer.predict(gray_frame)
        logger.info(f"Predicted face. Label: {label}, confidence: {confidence}")
        if 2 <= confidence <= 85:
            trained_face: TrainedFace = get_by_id(_id=label)
            text: str
            if trained_face is not None:
                text = trained_face.username
            else:
                text = "Unknown"
            logger.info(
                f"Recognized face. Label: {label}, confidence: {confidence}, text: {text}"
            )
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, text, (x, y), font, 1, color, stroke, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        save_frame(frame)


def save_frame(frame) -> None:
    """
    Save frame.

    :param frame: The frame
    """
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
