import logging.config

from home_guardian.function_collection import get_root_path

# Set up logging
logging_conf_path = f"{get_root_path()}/logging.conf"
print(f"Start loading logging configuration. logging_conf_path = {logging_conf_path}, __file__ = {__file__}")
logging.config.fileConfig(logging_conf_path)
print(f"Done loading logging configuration.")
