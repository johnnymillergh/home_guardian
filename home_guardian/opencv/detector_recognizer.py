import os

import cv2.cv2 as cv2
from cv2 import CascadeClassifier, face_LBPHFaceRecognizer
from cv2.data import haarcascades
from loguru import logger

from home_guardian.function_collection import get_data_dir

_haarcascade_frontalface_default = os.path.join(
    haarcascades, "haarcascade_frontalface_alt2.xml"
)

face_detector: CascadeClassifier = CascadeClassifier(_haarcascade_frontalface_default)
logger.warning(
    f"Initialized global face_detector: {face_detector}, "
    f"_haarcascade_frontalface_default: {_haarcascade_frontalface_default}"
)

face_recognizer: face_LBPHFaceRecognizer = cv2.face.LBPHFaceRecognizer_create()
try:
    face_recognizer.read(f"{get_data_dir()}/trainer.yml")
    logger.warning(f"Initialized global face_recognizer: {face_recognizer}")
except Exception:
    logger.exception("Cannot read trainer.yml!")
