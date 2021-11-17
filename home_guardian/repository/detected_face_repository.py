from loguru import logger

from home_guardian.repository.model.detected_face import DetectedFace


@logger.catch
def save(picture_path: str, detected_username: str = None) -> DetectedFace:
    """
    Save a new detected face.
    :param picture_path: the picture path
    :param detected_username: the detected username
    :return: a DetectedFace object
    """
    detected_face: DetectedFace = DetectedFace(
        picture_path=picture_path, detected_username=detected_username
    )
    detected_face.save()
    return detected_face
