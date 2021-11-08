import random

from home_guardian.repository.user_repository import create_user

if __name__ == "__main__":
    create_user(f"user{random.random()}")
