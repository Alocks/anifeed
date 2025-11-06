from typing import Dict
from dataclasses import asdict

from anifeed.services.apis.base_api import BaseApi
from anifeed.models.nyaa_search_model import NyaaParameters


class NyaaApi(BaseApi):
    def __init__(
                self,
                session=None,
                logger=None):
        super().__init__(
            base_url="https://nyaa.si",
            session=session,
            logger=logger)

    def fetch_search_result(
            self,
            params: NyaaParameters,
            ) -> Dict:
        r = self.get(params=asdict(params))
        r.raise_for_status()
        return r.text
