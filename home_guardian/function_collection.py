import os

_current_file = os.path.abspath(__file__)


def get_root_path() -> str:
    """
    Get the root path of the project.
    """
    return os.path.dirname(_current_file)


def get_data_dir() -> str:
    """
    Get the data directory of the project.
    """
    data_dir = f"{get_root_path()}/_data"
    os.makedirs(data_dir, exist_ok=True)
    return data_dir
