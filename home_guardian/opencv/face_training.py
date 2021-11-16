import os
from typing import Any

import cv2.cv2 as cv2
import numpy as np
from loguru import logger
from PIL import Image

from home_guardian.function_collection import (
    get_data_dir,
    get_resources_dir,
    get_training_datasets_dir,
)
from home_guardian.repository.model.trained_face import TrainedFace
from home_guardian.repository.trained_face_repository import save_or_update


def _get_face_features_and_labels() -> tuple[list[np.ndarray], list]:
    detector = cv2.CascadeClassifier(
        f"{get_resources_dir()}/haarcascade_frontalface_alt2.xml"
    )
    datasets_path: str = get_training_datasets_dir()
    logger.info(f"Face training datasets path: {datasets_path}")
    image_paths: list[str] = [
        os.path.join(datasets_path, f) for f in os.listdir(datasets_path)
    ]
    face_features: list[np.ndarray] = []
    labels: list[Any] = []
    for image_path in image_paths:
        for root, dirs, files in os.walk(image_path):
            for file in files:
                path: str = os.path.join(root, file)
                # convert it to grayscale
                img: Image = Image.open(path).convert("L")
                img_numpy: np.ndarray = np.array(img, "uint8")
                username: str = os.path.split(image_paths[0])[-1]
                trained_face: TrainedFace = save_or_update(username)
                logger.info(
                    f"Getting face features with the username: {username}, id: {trained_face}"
                )
                face_array = detector.detectMultiScale(
                    img_numpy, scaleFactor=1.5, minNeighbors=5
                )
                for (x, y, w, h) in face_array:
                    face_features.append(img_numpy[y : y + h, x : x + w])
                    labels.append(trained_face.get_id())
    return face_features, labels


def train_data() -> None:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    logger.info("Training faces. It will take a few seconds. Wait...")
    face_features, labels = _get_face_features_and_labels()
    recognizer.train(face_features, np.array(labels))
    recognizer.save(f"{get_data_dir()}/trainer.yml")
    logger.info(f"{len(np.unique(labels))} faces trained.")
