import datetime
import os
import pickle
from time import sleep
from typing import List, Tuple

import cv2.cv2 as cv2
import face_recognition
from loguru import logger

from home_guardian.common.debounce_throttle import throttle
from home_guardian.configuration.application_configuration import application_conf
from home_guardian.configuration.thread_pool_configuration import executor
from home_guardian.function_collection import get_data_dir
from home_guardian.message.email import send_email
from home_guardian.opencv.threading import VideoCaptureThreading
from home_guardian.repository.detected_face_repository import save
from home_guardian.repository.model.detected_face import DetectedFace

_detected_face_dir = f"{get_data_dir()}/detection"
os.makedirs(_detected_face_dir, exist_ok=True)
logger.warning(f"Made the directory, _detected_face_dir: {_detected_face_dir}")

_headless: bool = application_conf.get_bool("headless")

try:
    with open(f"{get_data_dir()}/trained_model.pickle", "rb") as trained_model:
        trained_model_data = pickle.loads(trained_model.read())
except FileNotFoundError as e:
    logger.exception(f"Failed to load trained_model.pickle!")
    raise e


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
            cv2.imshow("Detect and Take Photo", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        if not grabbed:
            break
        process_frame(frame)
        sleep(0.04)
    vid_cap.stop()
    cv2.destroyAllWindows()


@throttle(3)
def process_frame(frame) -> None:
    executor.submit(async_process_frame, frame)


@logger.catch
def async_process_frame(frame) -> None:
    # Detect the face_locations
    face_locations: List[Tuple] = face_recognition.face_locations(frame)
    if len(face_locations) == 0:
        logger.debug("No face detected")
        return
    # compute the facial embeddings for each face bounding box
    face_encodings: list = face_recognition.face_encodings(frame, face_locations)
    names = []
    # loop over the facial embeddings
    for face_encoding in face_encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(
            trained_model_data["face_encodings"], face_encoding
        )
        # if face is not recognized, then print Unknown
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matched_idxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matched_idxs:
                name = trained_model_data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)
            logger.debug(f"Determined name: {name}, counts: {counts.get}")
        # update the list of names
        names.append(name)
    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(face_locations, names):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(
            frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
        )
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
