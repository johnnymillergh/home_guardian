import random

from home_guardian.configuration.thread_pool_configuration import simulate_multi_thread
from home_guardian.repository.user_repository import create_user

if __name__ == "__main__":
    create_user(f"user{random.random()}")
    simulate_multi_thread()
