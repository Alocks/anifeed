__all__ = ["MalAdapter"]
import os
from typing import Dict, Optional
from enum import EnumType

from anifeed.adapters.base_api import BaseApi
from anifeed.adapters.parsers.mal_parser import MalParser
from anifeed.constants.anime_status_enum import AnimeStatus

MAL_STATUS_MAP = {
    AnimeStatus.WATCHING: "watching",
    AnimeStatus.PLANNING: "plan_to_watch",
    AnimeStatus.COMPLETED: "completed",
    AnimeStatus.DROPPED: "dropped",
    AnimeStatus.PAUSED: "on_hold",
    AnimeStatus.REPEATING: "watching",
}


class MalAdapter(BaseApi):
    def __init__(self,
                 session=None,
                 query_path: Optional[str] = None,
                 logger=None,
                 ):
        super().__init__(
            base_url="https://api.myanimelist.net/v2",
            api_parser=MalParser,
            session=session, logger=logger
            )
        self.session.headers = {"X-MAL-CLIENT-ID": os.getenv("MAL_CLIENT_ID")}

    def get_user_anime_list(
            self,
            username: str,
            status: EnumType,
            ) -> Dict:
        self.logger.debug(f"Fetching data from {username} in {status}")
        status = self._translate_status(internal_status=status)
        payload_dict = {
            "status": status.value,
            "fields": "id,title,alternative_titles,status,num_episodes"
            }
        r = self.get(f"/users/{username}/animelist", params=payload_dict)
        r.raise_for_status()
        self.logger.debug("Fetched data successfuly")
        return r.json()
