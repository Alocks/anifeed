import requests
from typing import Optional

from anifeed.utils.http_client import HttpClient
from anifeed.utils.log_utils import get_logger


class BaseApi(HttpClient):
    def __init__(self,
                 base_url: Optional[str] = None,
                 session: Optional[requests.Session] = None,
                 ):
        super().__init__(base_url=base_url, session=session)
        self.logger = get_logger(f"anifeed.services.apis.{self.__class__.__name__}")
