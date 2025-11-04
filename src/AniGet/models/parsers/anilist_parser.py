__all__ = ["AniListParser"]

from typing import List
from dataclasses import dataclass

from anifeed.models.parsers.base_parser import BaseParser
from anifeed.utils.commons import DictWrangler


@dataclass
class AnimeMetadata:
    title_romaji: str
    title_english: str
    episodes: int
    status: str


class AniListParser(BaseParser):
    def parse_api_metadata(self) -> List[AnimeMetadata]:
        metadata = DictWrangler.find_value_recursively(
            data=self._api_metadata, target_key="entries")
        res = [
            AnimeMetadata(
                title_romaji=DictWrangler.find_value_recursively(x, "romaji"),
                title_english=DictWrangler.find_value_recursively(x, "english"),
                episodes=DictWrangler.find_value_recursively(x, "episodes"),
                status=DictWrangler.find_value_recursively(x, "status"),
                )
            for x in metadata]

        return res
