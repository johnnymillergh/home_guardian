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
    data_dir = f"{get_root_path()}/data"
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_resources_dir() -> str:
    """
    Get the resources directory of the project.
    """
    return f"{get_root_path()}/resources"


def get_training_datasets_dir() -> str:
    """
    Get the training datasets directory of the project.
    """
    return f"{get_data_dir()}/training_datasets"


def get_cpu_count() -> int:
    """
    Get CPU count, default is 4
    """
    cpu_count = os.cpu_count()
    if cpu_count is not None:
        return cpu_count
    else:
        return 4
