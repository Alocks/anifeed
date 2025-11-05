__all__ = ["AniListStatus"]
from enum import Enum


class AniListStatus(Enum):
    WATCHING = "CURRENT"
    PLANNING = "PLANNING"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"
    PAUSED = "PAUSED"
    REPEATING = "REPEATING"

class MalStatus(Enum):
    WATCHING = "watching"
    PLANNING = "plan_to_watch"
    COMPLETED = "completed"
    DROPPED = "dropped"
    PAUSED = "on_hold"