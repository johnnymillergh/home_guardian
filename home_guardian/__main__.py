from home_guardian.configuration.thread_pool_configuration import (
    cleanup as thread_pool_cleanup,
)
from home_guardian.configuration.thread_pool_configuration import simulate_multi_thread


def cleanup() -> None:
    thread_pool_cleanup()


def main() -> None:
    """
    Main function.
    """
    try:
        simulate_multi_thread()
    finally:
        cleanup()


if __name__ == "__main__":
    main()
