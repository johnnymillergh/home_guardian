import os
from typing import Any, List, Tuple

import cv2.cv2 as cv2
import numpy as np
from loguru import logger
from PIL import Image

from home_guardian.common.time import elapsed_time
from home_guardian.function_collection import get_data_dir, get_training_datasets_dir
from home_guardian.opencv.detector_recognizer import face_detector
from home_guardian.repository.model.trained_face import TrainedFace
from home_guardian.repository.trained_face_repository import save_or_update


def _get_face_features_and_labels() -> Tuple[List[np.ndarray], list]:
    datasets_path: str = get_training_datasets_dir()
    image_paths: List[str] = [
        os.path.join(datasets_path, f) for f in os.listdir(datasets_path)
    ]
    logger.info(
        f"Face training datasets path: {datasets_path}, image_paths: {image_paths}"
    )
    face_features: List[np.ndarray] = []
    labels: List[Any] = []
    for image_path in image_paths:
        logger.debug(f"Image path: {image_path}")
        for root, dirs, files in os.walk(image_path):
            for file in files:
                path: str = os.path.join(root, file)
                logger.info(f"Path: {path}")
                # convert it to grayscale
                img: Image = Image.open(path).convert("L")
                img_numpy: np.ndarray = np.array(img, "uint8")
                username: str = os.path.split(image_path)[-1]
                trained_face: TrainedFace = save_or_update(username)
                logger.info(
                    f"Getting face features with the username: {username}, id: {trained_face}"
                )
                face_array = face_detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in face_array:
                    face_features.append(img_numpy[y : y + h, x : x + w])
                    labels.append(trained_face.get_id())
    return face_features, labels


@elapsed_time
def train_data() -> None:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    logger.warning("Training faces. It will take a few seconds. Wait...")
    face_features, labels = _get_face_features_and_labels()
    recognizer.train(face_features, np.array(labels))
    recognizer.save(f"{get_data_dir()}/trainer.yml")
    unique_labels: np.ndarray = np.unique(labels)
    logger.warning(f"{len(unique_labels)} faces trained. Labels: {unique_labels}")
