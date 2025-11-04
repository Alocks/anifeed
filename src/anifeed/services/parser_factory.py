from typing import Type, Dict
from anifeed.models.parsers.base_parser import BaseParser
from anifeed.models.parsers.anilist_parser import AniListParser
from anifeed.models.parsers.nyaa_parser import NyaaParser

_PARSER_REGISTRY: Dict[str, Type[BaseParser]] = {
    "anilist": AniListParser,
    "nyaa": NyaaParser,
}


def register_parser(name: str, parser_cls: Type[BaseParser]) -> None:
    _PARSER_REGISTRY[name.lower()] = parser_cls


def create_parser(name: str, api_metadata, session=None, logger=None, **kwargs) -> BaseParser:
    cls = _PARSER_REGISTRY.get(name.lower())
    if cls is None:
        raise ValueError(f"No parser registered for {name}")
    return cls(api_metadata=api_metadata, session=session, logger=logger, **kwargs)
