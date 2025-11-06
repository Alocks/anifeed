"""
Unified anime service - simpler than separate adapters.
Combines API + Parser into one convenient service.
"""
from typing import List, Literal

from anifeed.models.anime_model import Anime
from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.services.apis.anilist_api import AniListApi
from anifeed.services.apis.mal_api import MalApi
from anifeed.services.parsers.anilist_parser import AniListParser
from anifeed.services.parsers.mal_parser import MalParser
from anifeed.utils.log_utils import get_logger


class AnimeService:
    def __init__(
            self,
            source: Literal["anilist", "mal"] = "anilist",
            session=None,
            logger=None
    ):
        self.source = source
        self.logger = logger or get_logger(__name__)
        if source == "anilist":
            self._api = AniListApi(session=session, logger=logger)
            self._parser = AniListParser(logger=logger)
        elif source == "mal":
            self._api = MalApi(session=session, logger=logger)
            self._parser = MalParser(logger=logger)
        else:
            raise ValueError(f"Unknown source: {source}")

    def get_user_anime_list(self, username: str, status: AnimeStatus) -> List[Anime]:
        self.logger.debug("Fetching anime for %s from %s", username, self.source)
        raw_data = self._api.get_user_anime_list(username=username, status=status)
        animes = self._parser.parse_api_metadata(metadata=raw_data)
        self.logger.info("Fetched %d anime entries", len(animes))
        return animes
