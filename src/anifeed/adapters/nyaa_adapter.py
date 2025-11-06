__all__ = ["NyaaAdapter"]
from typing import Dict
from dataclasses import dataclass, asdict

from anifeed.adapters.base_api import BaseApi
from anifeed.adapters.parsers.nyaa_parser import NyaaParser
from anifeed.constants.nyaa_search_enum import (
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


class NyaaAdapter(BaseApi):
    def __init__(
                self,
                session=None,
                logger=None):
        super().__init__(
            base_url="https://nyaa.si",
            session=session,
            api_parser=NyaaParser,
            logger=logger)

    def fetch_search_result(
            self,
            params: NyaaParameters,
            ) -> Dict:
        self.logger.debug(f"Fetching data from Nyaa using {params}")
        r = self.get(params=asdict(params))
        r.raise_for_status()
        self.logger.debug("Fetched data successfuly")
        return r.text
