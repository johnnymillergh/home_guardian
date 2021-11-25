import os
import pickle
from typing import Any, List, Tuple

import face_recognition
import numpy as np
from PIL import Image
from loguru import logger

from home_guardian.common.time import elapsed_time
from home_guardian.function_collection import get_training_datasets_dir, get_data_dir
from home_guardian.repository.model.trained_face import TrainedFace
from home_guardian.repository.trained_face_repository import save_or_update


def _get_face_encodings_and_names() -> Tuple[List[Any], List[str]]:
    datasets_path: str = get_training_datasets_dir()
    image_paths: List[str] = [
        os.path.join(datasets_path, f) for f in os.listdir(datasets_path)
    ]
    logger.info(
        f"Face training datasets path: {datasets_path}, image_paths: {image_paths}"
    )
    # initialize the list of known encodings and known names
    known_encodings: List[Any] = []
    known_names: List[str] = []
    for image_path in image_paths:
        logger.debug(f"Image path: {image_path}")
        for root, dirs, files in os.walk(image_path):
            for file in files:
                path: str = os.path.join(root, file)
                logger.info(f"Path: {path}")
                # convert it to RGB
                rgb_image: Image = Image.open(path).convert("RGB")
                rgb_image_numpy_array: np.ndarray = np.array(rgb_image, "uint8")
                # detect the (x, y)-coordinates of the bounding face_locations
                # corresponding to each face in the input image
                face_locations = face_recognition.face_locations(
                    rgb_image_numpy_array, model="hog"
                )
                # compute the facial embedding for the face
                face_encodings = face_recognition.face_encodings(
                    rgb_image_numpy_array, face_locations
                )
                username: str = os.path.split(image_path)[-1]
                trained_face: TrainedFace = save_or_update(username)
                logger.info(
                    f"Appending face features with the username: {username}, id: {trained_face}"
                )
                # loop over the encodings
                for encoding in face_encodings:
                    # add each encoding + name to our set of known names and encodings
                    known_encodings.append(encoding)
                    known_names.append(username)
    return known_encodings, known_names


@elapsed_time
def train_data() -> None:
    logger.warning("Training face model. It will take a few minutes…")
    face_encodings, names = _get_face_encodings_and_names()
    trained_model_data: dict = {"face_encodings": face_encodings, "names": names}
    with open(f"{get_data_dir()}/trained_model.pickle", "wb") as file:
        file.write(pickle.dumps(trained_model_data))
    unique_names: np.ndarray = np.unique(names)
    logger.warning(f"{len(unique_names)} face model trained. Names: {unique_names}")
