__all__ = ["AniListAdapter"]
from anifeed.constants.anime_status_enum import AnimeStatus
from typing import Dict, Optional
from enum import EnumType

from anifeed.adapters.base_api import BaseApi
from anifeed.adapters.parsers.anilist_parser import AniListParser
from anifeed.utils.commons import UniversalPath

ANILIST_STATUS_MAP = {
    AnimeStatus.WATCHING: "CURRENT",
    AnimeStatus.PLANNING: "PLANNING",
    AnimeStatus.COMPLETED: "COMPLETED",
    AnimeStatus.DROPPED: "DROPPED",
    AnimeStatus.PAUSED: "PAUSED",
    AnimeStatus.REPEATING: "REPEATING",
}


class AniListAdapter(BaseApi):
    def __init__(self,
                 session=None,
                 query_path: Optional[str] = None,
                 logger=None
                 ):
        super().__init__(
            base_url="https://graphql.anilist.co",
            session=session,
            api_parser=AniListParser,
            logger=logger)

        qpath = query_path or UniversalPath("adapters/anilist_adapter/fetch_userlist.graphql")
        with open(qpath, mode="r", encoding="utf-8") as fh:
            self._query_fetch_userlist = fh.read()

    def get_user_anime_list(
            self,
            username: str,
            status: EnumType,
            ) -> Dict:
        self.logger.debug(f"Fetching data from {username} in {status}")
        status = self._translate_status(internal_status=status)
        payload_dict = {
            "query": self._query_fetch_userlist,
            "variables": {"userName": username,
                          "status": status}
            }
        r = self.post(json=payload_dict)
        r.raise_for_status()
        self.logger.debug("Fetched data successfuly")
        return r.json()

    def _translate_status(self, internal_status: AnimeStatus) -> Optional[str]:
        """Translates the internal MediaStatus to the MAL API string."""
        return ANILIST_STATUS_MAP.get(internal_status)
