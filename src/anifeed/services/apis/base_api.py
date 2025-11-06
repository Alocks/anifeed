import requests
from typing import Optional

from anifeed.utils.http_client import HttpClient


class BaseApi(HttpClient):
    def __init__(self,
                 base_url: Optional[str] = None,
                 session: Optional[requests.Session] = None,
                 logger=None
                 ):
        super().__init__(base_url=base_url, session=session, logger=logger)
