from anifeed.utils.commons import TomlParser
from types import MappingProxyType

APPLICATION_CONFIG = MappingProxyType(TomlParser.get_config("application"))
NYAA_CONFIG = MappingProxyType(TomlParser.get_config("nyaa"))
RSS_CONFIG = MappingProxyType(TomlParser.get_config("rss"))
