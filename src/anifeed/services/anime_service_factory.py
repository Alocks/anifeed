from typing import Dict, Callable, Tuple
from anifeed.services.apis.base_api import BaseApi
from anifeed.services.parsers.base_parser import BaseParser
from anifeed.services.apis.anilist_api import AniListApi
from anifeed.services.apis.mal_api import MalApi
from anifeed.services.parsers.anilist_parser import AniListParser
from anifeed.services.parsers.mal_parser import MalParser
from anifeed.exceptions import AnimeSourceError


ApiParserFactory = Callable[[object, object], Tuple[BaseApi, BaseParser]]


_ANIME_SOURCE_REGISTRY: Dict[str, ApiParserFactory] = {
    "anilist": lambda session, logger: (
        AniListApi(session=session, logger=logger),
        AniListParser(logger=logger)
    ),
    "mal": lambda session, logger: (
        MalApi(session=session, logger=logger),
        MalParser(logger=logger)
    ),
}


def register_anime_source(name: str, factory: ApiParserFactory) -> None:
    """Register a new anime source (extension point)"""
    _ANIME_SOURCE_REGISTRY[name.lower()] = factory


def create_anime_api_service(source: str, session=None, logger=None) -> Tuple[BaseApi, BaseParser]:
    factory = _ANIME_SOURCE_REGISTRY.get(source.lower())
    if factory is None:
        available = ", ".join(_ANIME_SOURCE_REGISTRY.keys())
        raise AnimeSourceError(
            f"Unknown anime source: '{source}'. Available: {available}"
        )
    return factory(session, logger)
