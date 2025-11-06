from dataclasses import dataclass

from anifeed.constants.nyaa_search_enum import (
    NyaaCategory,
    NyaaColumnToOrder,
    NyaaFilter,
    NyaaOrder
)


@dataclass
class NyaaParameters:
    q: str
    f: NyaaFilter = NyaaFilter.NO_FILTER.value
    s: NyaaColumnToOrder = NyaaColumnToOrder.SEEDS.value
    o: NyaaOrder = NyaaOrder.DESCENDING.value
    c: NyaaCategory = NyaaCategory.DEFAULT.value
