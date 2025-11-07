from dataclasses import dataclass


@dataclass(frozen=True)
class Torrent:
    """Represents torrent metadata"""
    title: str
    download_url: str
    size: str
    seeders: int
    leechers: int
