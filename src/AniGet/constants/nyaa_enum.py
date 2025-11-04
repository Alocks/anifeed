__all__ = ["NyaaCategory", "NyaaFilter", "NyaaColumnToOrder", "NyaaOrder"]
from enum import Enum


class NyaaCategory(Enum):
    DEFAULT = "1_0"
    ENGLISH_TRANSLATED = "1_2"
    NON_ENGLISH_TRANSLATED = "1_3"
    RAW = "1_4"


class NyaaFilter(Enum):
    NO_FILTER = "0"
    NO_REMAKES = "1"
    TRUSTED_ONLY = "2"


class NyaaColumnToOrder(Enum):
    SEEDS = "seeders"
    SIZE = "size"
    DOWNLOADS = "download"
    LEECHERS = "leechers"


class NyaaOrder(Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"