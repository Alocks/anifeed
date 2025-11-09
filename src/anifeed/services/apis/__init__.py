"""
External APIs for the AniFeed Library.
"""
from anifeed.services.apis.base_api import BaseApi
from anifeed.services.apis.anilist_api import AniListApi
from anifeed.services.apis.mal_api import MalApi
from anifeed.services.apis.nyaa_api import NyaaApi


__all__ = ["BaseApi", "AniListApi", "MalApi", "NyaaApi"]
