from dataclasses import dataclass
from typing import Optional, List, Literal

from anifeed.models.anime_model import Anime


@dataclass(frozen=True)
class UserAnimeList:
    """Represents a user's anime list"""
    username: str
    source: Literal["anilist", "mal"]
    watching: Optional[List[Anime]] = None
    completed: Optional[List[Anime]] = None
    plan_to_watch: Optional[List[Anime]] = None
