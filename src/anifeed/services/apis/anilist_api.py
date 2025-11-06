from typing import Dict, Optional
from enum import EnumType

from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.services.apis.base_api import BaseApi
from anifeed.utils.commons import UniversalPath

ANILIST_STATUS_MAP = {
    AnimeStatus.WATCHING: "CURRENT",
    AnimeStatus.PLANNING: "PLANNING",
    AnimeStatus.COMPLETED: "COMPLETED",
    AnimeStatus.DROPPED: "DROPPED",
    AnimeStatus.PAUSED: "PAUSED",
    AnimeStatus.REPEATING: "REPEATING",
}


class AniListApi(BaseApi):
    def __init__(self,
                 session=None,
                 query_path: Optional[str] = None,
                 logger=None
                 ):
        super().__init__(
            base_url="https://graphql.anilist.co",
            session=session,
            logger=logger)

        qpath = UniversalPath("services/apis/anilist_api/fetch_userlist.graphql")
        with open(qpath, mode="r", encoding="utf-8") as fh:
            self._query_fetch_userlist = fh.read()

    def get_user_anime_list(
            self,
            username: str,
            status: EnumType,
            ) -> Dict:
        status = self._translate_status(internal_status=status)
        payload_dict = {
            "query": self._query_fetch_userlist,
            "variables": {"userName": username,
                          "status": status}
            }
        r = self.post(json=payload_dict)
        r.raise_for_status()
        return r.json()

    def _translate_status(self, internal_status: AnimeStatus) -> Optional[str]:
        """Translates the internal MediaStatus to the MAL API string."""
        return ANILIST_STATUS_MAP.get(internal_status)
