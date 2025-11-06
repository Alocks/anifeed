from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class NyaaConfig:
    batch: List[str]
    fansub: List[str]
    resolution: List[str]


@dataclass(frozen=True)
class ApplicationConfig:
    user: str
    api: str
    status: List[str]
    nyaa_config: NyaaConfig
