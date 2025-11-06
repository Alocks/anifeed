from enum import Enum, auto


class AnimeStatus(Enum):
    # These are the keys you will use in your internal code
    WATCHING = auto()
    PLANNING = auto()
    COMPLETED = auto()
    DROPPED = auto()
    PAUSED = auto()
    REPEATING = auto()
