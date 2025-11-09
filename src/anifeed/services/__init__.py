"""
Services to communicate between the controllers for the AniFeed API.
"""
from anifeed.services.anime_service import AnimeService
from anifeed.services.similarity_service import SimilarityService
from anifeed.services.torrent_service import TorrentService

__all__ = ["AnimeService", "SimilarityService", "TorrentService"]
