__all__ = ["AniListStatus"]
from enum import Enum


class AniListStatus(Enum):
    WATCHING = "CURRENT"
    PLANNING = "PLANNING"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"
    PAUSED = "PAUSED"
    REPEATING = "REPEATING"
