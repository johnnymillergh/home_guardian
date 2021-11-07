import os

_current_file = os.path.abspath(__file__)


def get_root_path() -> str: return os.path.dirname(_current_file)
