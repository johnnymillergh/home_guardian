from __future__ import annotations

from enum import Enum, unique


@unique
class StartupMode(Enum):
    """
    StartupMode is an enumeration of possible startup modes.
    """

    # Detect and inspect
    DETECT = "detect"
    # Collect data
    COLLECT = "collect"
    # Train data
    TRAIN = "train"

    @staticmethod
    def value_of(value: str) -> StartupMode:
        for member in StartupMode:
            if member.value == value:
                return member
        raise ValueError(f"Unknown startup mode: {value}")
