__all__ = ["MalParser"]

from typing import List
from dataclasses import dataclass

from anifeed.models.parsers.base_parser import BaseParser, AnimeMetadata
from anifeed.utils.commons import DictWrangler
class MalParser(BaseParser):
    def parse_api_metadata(self) -> List[AnimeMetadata]:
        metadata = DictWrangler.find_value_recursively(
            data=self._api_metadata, target_key="data")
        res = [
            AnimeMetadata(
                title_romaji=DictWrangler.find_value_recursively(x, "title"),
                title_english=DictWrangler.find_value_recursively(x, "en"),
                episodes=DictWrangler.find_value_recursively(x, "num_episodes"),
                status=DictWrangler.find_value_recursively(x, "status"),
                )
            for x in metadata]

        return res