from dataclasses import dataclass, field
from typing import List

from anifeed.utils.commons import TomlParser
from types import MappingProxyType


APPLICATION_CONFIG = MappingProxyType(TomlParser.get_config("application"))
NYAA_CONFIG = MappingProxyType(TomlParser.get_config("nyaa"))
RSS_CONFIG = MappingProxyType(TomlParser.get_config("rss"))


@dataclass
class ApplicationConfig:
    user: str = APPLICATION_CONFIG.get("user")
    api: str = APPLICATION_CONFIG.get("api")
    status: List[str] = field(default_factory=[k for k, v in APPLICATION_CONFIG.get("status").items() if v])
