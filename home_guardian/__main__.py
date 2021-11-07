import logging.config
from os import path
import sys

from home_guardian.home_guardian import fib

# Set up logging
logging_conf_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
print(f"logging_conf_path = {logging_conf_path}, __file__ = {__file__}")
logging.config.fileConfig(logging_conf_path)

if __name__ == "__main__":
    n = int(sys.argv[1])
    print(fib(n))
