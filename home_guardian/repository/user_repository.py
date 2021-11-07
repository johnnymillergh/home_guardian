import logging

from home_guardian.repository.model.user import User

log = logging.getLogger("rotatingFileLogger")


def create_user(username: str) -> User:
    """
    Creates a new user.
    :param username: usernameasdf
    :return: a user
    """
    a_user = User.create(username=username, created_time="2019-01-01 00:00:00")
    log.info(f"Created, a_user = {a_user}")
    return a_user
