from __future__ import annotations

from enum import Enum, unique


@unique
class StartupMode(Enum):
    """
    StartupMode is an enumeration of possible startup modes.
    """

    # Detect and inspect
    NORMAL = 0
    # Train data
    TRAIN = 1

    @staticmethod
    def value_of(value: int) -> StartupMode:
        for member in StartupMode:
            if member.value == value:
                return member
        raise ValueError(f"Unknown startup mode: {value}")
