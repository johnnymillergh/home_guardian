import datetime
import os

import cv2.cv2 as cv2
from cv2.cv2 import CascadeClassifier
from loguru import logger

from home_guardian.common.debounce_throttle import throttle
from home_guardian.configuration.thread_pool_configuration import executor
from home_guardian.function_collection import get_data_dir, get_resources_dir
from home_guardian.message.email import send_email
from home_guardian.opencv.threading import VideoCaptureThreading
from home_guardian.repository.detected_face_repository import save
from home_guardian.repository.model.detected_face import DetectedFace
from home_guardian.repository.model.trained_face import TrainedFace
from home_guardian.repository.trained_face_repository import get_by_id

_detected_face_dir = f"{get_data_dir()}/detection"
os.makedirs(_detected_face_dir, exist_ok=True)
logger.warning(f"Made the directory, _detected_face_dir: {_detected_face_dir}")


def detect_and_take_photo() -> None:
    """
    Detect and take photo.
    :return: when exception is raised, return None.
    """
    face = CascadeClassifier(f"{get_resources_dir()}/haarcascade_frontalface_alt2.xml")
    try:
        vid_cap: VideoCaptureThreading = VideoCaptureThreading(0).start()
    except Exception as e:
        logger.error("Exception raised while starting video capture thread!", e)
        return
    while True:
        grabbed, frame = vid_cap.read()
        cv2.imshow("Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if not grabbed:
            break
        process_frame(face, frame)
    vid_cap.stop()
    cv2.destroyAllWindows()


@throttle(3)
def process_frame(cascade_classifier: CascadeClassifier, frame) -> None:
    executor.submit(async_process_frame, cascade_classifier, frame)


@logger.catch
def async_process_frame(cascade_classifier: CascadeClassifier, frame) -> None:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade_classifier.detectMultiScale(
        gray_frame, scaleFactor=1.5, minNeighbors=5
    )
    for (x, y, w, h) in faces:
        logger.info(
            "Detected face, axis(x,y) = ({},{}), width = {} px, h = {} px", x, y, w, h
        )
        _recognizer = cv2.face.LBPHFaceRecognizer_create()
        _recognizer.read(f"{get_data_dir()}/trainer.yml")
        # recognize? deep learned model predict keras tensorflow pytorch scikit learn
        label, confidence = _recognizer.predict(gray_frame)
        if 4 <= confidence <= 85:
            trained_face: TrainedFace = get_by_id(_id=label)
            if trained_face is not None:
                text: str = trained_face.username
            else:
                text: str = "Unknown"
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
