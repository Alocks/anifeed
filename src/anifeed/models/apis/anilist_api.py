__all__ = ["AniListApi"]

from typing import Dict, Optional
from enum import EnumType

from anifeed.models.apis.base_api import BaseApi
from anifeed.utils.commons import UniversalPath


class AniListApi(BaseApi):
    def __init__(self,
                 session=None,
                 query_path: Optional[str] = None,
                 logger=None
                 ):
        super().__init__(base_url="https://graphql.anilist.co", session=session, logger=logger)

        qpath = query_path or UniversalPath("models/apis/anilist_queries/fetch_userlist.graphql")
        with open(qpath, mode="r", encoding="utf-8") as fh:
            self._query_fetch_userlist = fh.read()

    def get_user_ongoing_anime(
            self,
            username: str,
            status: EnumType,
            ) -> Dict:
        self.logger.debug(f"Fetching data from {username} in {status}")
        payload_dict = {
            "query": self._query_fetch_userlist,
            "variables": {"userName": username,
                          "status": status.value}
            }
        r = self.post(json=payload_dict)
        r.raise_for_status()
        self.logger.debug("Fetched data successfuly")
        return r.json()
