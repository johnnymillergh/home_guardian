import logging.config
import random

from home_guardian.repository.user_repository import create_user

log = logging.getLogger("rotatingFileLogger")
if __name__ == "__main__":
    create_user(f"user{random.random()}")
