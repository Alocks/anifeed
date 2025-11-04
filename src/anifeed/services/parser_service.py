from enum import EnumType

from anifeed.models.apis.anilist_api import AniListApi
from anifeed.models.apis.nyaa_api import NyaaApi
from anifeed.services.parser_factory import create_parser
from anifeed.utils.log_utils import get_logger
from anifeed.models.apis.nyaa_api import NyaaParameters


class ParserService:
    def __init__(self, ani_api: AniListApi, nyaa_api: NyaaApi, logger=None):
        self.ani_api = ani_api
        self.nyaa_api = nyaa_api
        self.logger = logger or get_logger(__name__)

    def parse_user_anime_list(self, username: str, status: EnumType):
        dict_data = self.ani_api.get_user_ongoing_anime(username, status)
        parser = create_parser("anilist", api_metadata=dict_data, logger=self.logger)
        return parser.parse_api_metadata()

    def search_and_parse_nyaa(self, params: NyaaParameters):
        html_data = self.nyaa_api.fetch_search_result(params)
        parser = create_parser("nyaa", api_metadata=html_data, logger=self.logger)
        return parser.parse_api_metadata()
