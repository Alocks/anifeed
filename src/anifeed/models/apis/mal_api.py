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
                 logger=None,        
                 header = {"X-MAL-CLIENT-ID": os.getenv("CLIENT_ID")}
                 ):
        super().__init__(base_url="https://api.myanimelist.net/v2", session=session, logger=logger)
        self.session.headers = header

    def get_user_ongoing_anime(
            self,
            username: str   ,
            status: EnumType,
            ) -> Dict:
        self.logger.debug(f"Fetching data from {username} in {status}")
        payload_dict = {
            "status": status.value,
            "fields": "id,title,alternative_titles,status,num_episodes"
            }
        r = self.get(f"/users/{username}/animelist", params=payload_dict)
        r.raise_for_status()
        self.logger.debug("Fetched data successfuly")
        return r.json() 