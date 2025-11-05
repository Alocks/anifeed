__all__ = ["MalApi"]

import os
from typing import Dict, Optional
from enum import EnumType

from anifeed.models.apis.base_api import BaseApi
from anifeed.utils.commons import UniversalPath


class MalApi(BaseApi):
    def __init__(self,
                 session=None,
                 query_path: Optional[str] = None,
                 logger=None
                 ):
        super().__init__(base_url="https://api.myanimelist.net/v2", session=session, logger=logger)
        
#        qpath = query_path or UniversalPath("models/apis/anilist_queries/fetch_userlist.graphql")
#        with open(qpath, mode="r", encoding="utf-8") as fh:
#            self._query_fetch_userlist = fh.read()

    def get_user_ongoing_anime(
            self,
            username: str   ,
            status: EnumType,
            ) -> Dict:
        self.logger.debug(f"Fetching data from {username} in {status}")
        payload_dict = {
            "status": status.value
            }
        header = {
            "X-MAL-CLIENT-ID": os.getenv("CLIENT_ID")
        }
        r = self.get(f"/users/{username}/animelist", params=payload_dict, headers=header)
        r.raise_for_status()
        self.logger.debug("Fetched data successfuly")
        return r.json()