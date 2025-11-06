from typing import List

from anifeed.models.torrent_model import Torrent
from anifeed.models.nyaa_search_model import NyaaParameters
from anifeed.services.apis.nyaa_api import NyaaApi
from anifeed.services.parsers.nyaa_parser import NyaaParser
from anifeed.utils.log_utils import get_logger


class TorrentService:
    def __init__(self, session=None, logger=None):
        self._api = NyaaApi(session=session, logger=logger)
        self._parser = NyaaParser(logger=logger)
        self.logger = logger or get_logger(__name__)

    def search(self, query: str, **kwargs) -> List[Torrent]:
        params = NyaaParameters(q=query, **kwargs)
        self.logger.debug("Searching torrents: %s", query)
        raw_html = self._api.fetch_search_result(params=params)
        torrents = self._parser.parse_api_metadata(metadata=raw_html)
        self.logger.info("Found %d torrents", len(torrents))
        return torrents
