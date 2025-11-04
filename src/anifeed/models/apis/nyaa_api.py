__all__ = ["NyaaApi"]
from typing import Dict, Optional
from dataclasses import dataclass, asdict

from anifeed.models.apis.base_api import BaseApi
from anifeed.constants.nyaa_enum import (
    NyaaFilter,
    NyaaCategory,
    NyaaColumnToOrder,
    NyaaOrder
)


@dataclass
class NyaaParameters:
    q: str
    f: NyaaFilter = NyaaFilter.NO_FILTER.value
    s: NyaaColumnToOrder = NyaaColumnToOrder.SEEDS.value
    o: NyaaOrder = NyaaOrder.DESCENDING.value
    c: NyaaCategory = NyaaCategory.DEFAULT.value


class NyaaApi(BaseApi):
    def __init__(self, base_url: Optional[str] = "https://nyaa.si", session=None, logger=None):
        super().__init__(base_url=base_url, session=session, logger=logger)

    def fetch_search_result(
            self,
            params: NyaaParameters,
            ) -> Dict:
        self.logger.debug(f"Fetching data from Nyaa using {params}")
        r = self.get(params=asdict(params))
        r.raise_for_status()
        self.logger.debug("Fetched data successfuly")
        return r.text
