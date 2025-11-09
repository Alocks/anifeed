"""
DTO models for the AniFeed library.
"""
from anifeed.models.anime_model import Anime
from anifeed.models.config_model import ApplicationConfig, NyaaConfig
from anifeed.models.nyaa_search_model import NyaaParameters
from anifeed.models.torrent_model import Torrent
from anifeed.models.user_model import UserAnimeList

__all__ = [
    "Anime",
    "NyaaConfig",
    "ApplicationConfig",
    "NyaaParameters",
    "Torrent",
    "UserAnimeList",
    ]
