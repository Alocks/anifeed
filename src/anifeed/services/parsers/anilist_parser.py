from typing import List, Dict, Any

from anifeed.services.parsers.base_parser import BaseParser
from anifeed.models.anime_model import Anime
from anifeed.utils.commons import DictWrangler


class AniListParser(BaseParser):
    def parse_api_metadata(self, metadata: Dict[Any, Any]) -> List[Anime]:
        metadata = DictWrangler.find_value_recursively(
            data=metadata, target_key="entries")
        res = [
            Anime(
                title_romaji=DictWrangler.find_value_recursively(x, "romaji"),
                title_english=DictWrangler.find_value_recursively(x, "english"),
                episodes=DictWrangler.find_value_recursively(x, "episodes"),
                status=DictWrangler.find_value_recursively(x, "status"),
                )
            for x in metadata]

        return res
