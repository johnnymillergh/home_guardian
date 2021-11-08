from datetime import datetime

from loguru import logger

from home_guardian.repository.model.user import User


@logger.catch
def create_user(username: str) -> User:
    """
    Creates a new user.
    :param username: username
    :return: a user
    """
    a_user = User.create(username=username, created_time=datetime.now())
    logger.info(f"Created, a_user = {a_user}")
    return a_user
