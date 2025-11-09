"""
Parsers to use with external APIs in AniFeed library.
"""
from anifeed.services.parsers.base_parser import BaseParser
from anifeed.services.parsers.anilist_parser import AniListParser
from anifeed.services.parsers.mal_parser import MalParser
from anifeed.services.parsers.nyaa_parser import NyaaParser

__all__ = ["BaseParser", "AniListParser", "MalParser", "NyaaParser"]
