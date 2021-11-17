from datetime import datetime

from loguru import logger

from home_guardian.repository.model.trained_face import TrainedFace


@logger.catch
def save_or_update(username: str) -> TrainedFace:
    """
    Save or update a trained face.
    :param username: The username of the trained face.
    :return: a new trained face.
    """
    trained_face: TrainedFace = TrainedFace(username=username)
    try:
        trained_face.save()
    except Exception as e:
        logger.warning(f"Exception occurred while saving trained face. {e}")
        trained_face.update({TrainedFace.modified_time: datetime.now()}).where(
            TrainedFace.username == username
        ).execute()
        trained_face = TrainedFace.get_or_none(TrainedFace.username == username)
    return trained_face


def get_by_id(_id: int) -> TrainedFace:
    """
    Get a trained face by id.
    :param _id: The id of the trained face.
    :return: a trained face.
    """
    return TrainedFace.get_by_id(_id)
