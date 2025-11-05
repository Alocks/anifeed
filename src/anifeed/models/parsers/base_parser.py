__all__ = ["BaseParser"]
from anifeed.utils import log_utils
from dataclasses import dataclass

@dataclass
class AnimeMetadata:
    title_romaji: str
    title_english: str
    episodes: int
    status: str

class BaseParser:
    def __init__(self, api_metadata, session=None, logger=None):
        self._api_metadata = api_metadata
        self.session = session
        self.logger = logger or log_utils.get_logger(__name__)

    def parse_api_metadata(self):
        raise NotImplementedError("parse_api_metadata must be implemented in subclasses")
