from typing import List, Literal

from anifeed.models.anime_model import Anime
from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.services.anime_service_factory import create_anime_api_service
from anifeed.utils.log_utils import get_logger


class AnimeService:
    def __init__(
            self,
            source: Literal["anilist", "mal"] = "anilist",
            session=None,
            logger=None
    ):
        self.source = source
        self.logger = logger or get_logger(f"anifeed.services.{self.__class__.__name__}")
        self._api, self._parser = create_anime_api_service(
            source=source,
            session=session,
            logger=logger
        )

    def get_user_anime_list(self, username: str, status: AnimeStatus) -> List[Anime]:
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        self.logger.debug("Fetching anime for %s from %s", username, self.source)
        raw_data = self._api.get_user_anime_list(username=username, status=status)
        animes = self._parser.parse_api_metadata(metadata=raw_data)
        self.logger.info("Fetched %d anime entries", len(animes))
        return animes
