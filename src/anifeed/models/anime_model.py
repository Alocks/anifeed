from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Anime:
    title_romaji: str
    title_english: str
    status: str
    episodes: Optional[int] = None
