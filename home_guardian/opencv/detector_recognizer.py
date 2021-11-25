import os

from cv2 import CascadeClassifier
from cv2.data import haarcascades
from loguru import logger

_haarcascade_frontalface_default = os.path.join(
    haarcascades, "haarcascade_frontalface_alt2.xml"
)

face_detector: CascadeClassifier = CascadeClassifier(_haarcascade_frontalface_default)
logger.warning(
    f"Initialized global face_detector: {face_detector}, "
    f"_haarcascade_frontalface_default: {_haarcascade_frontalface_default}"
)
