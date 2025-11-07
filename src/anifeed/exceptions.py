"""
Domain-specific exceptions for better error handling and testability.
"""


class AnifeedError(Exception):
    pass


class ConfigurationError(AnifeedError):
    pass


class AnimeSourceError(AnifeedError):
    pass


class TorrentSearchError(AnifeedError):
    pass


class ParsingError(AnifeedError):
    pass


class NetworkError(AnifeedError):
    pass
