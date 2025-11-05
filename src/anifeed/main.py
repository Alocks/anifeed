from dataclasses import dataclass
import logging

from anifeed.utils.log_utils import configure_root_logger, get_logger
from anifeed.models.apis.anilist_api import AniListApi
from anifeed.models.apis.nyaa_api import NyaaApi, NyaaParameters
from anifeed.services.similarity_service import SimilarityService  # optional
from anifeed.services.parser_service import ParserService  # optional
from anifeed.config.app_config import ApplicationConfig
from anifeed.constants.api_enum import AniListStatus, MalStatus
from anifeed.models.apis.mal_api import MalApi

@dataclass
class Application:
    logger: logging.Logger
    ani_api: AniListApi
    nyaa_api: NyaaApi
    mal_api: MalApi
    parser_service: ParserService = None  # optional
    similarity_service: SimilarityService = None  # optional


def build_app():
    configure_root_logger(level=logging.DEBUG)
    logger = get_logger(__name__)
    ani_api = AniListApi(logger=logger)
    nyaa_api = NyaaApi(logger=logger)
    mal_api = MalApi(logger=logger)
    parser_service = ParserService(ani_api=ani_api, nyaa_api=nyaa_api, mal_api=mal_api, logger=logger)  # optional
    similarity_service = SimilarityService(logger=logger)  # optional
    return Application(
        logger=logger,
        ani_api=ani_api,
        nyaa_api=nyaa_api,
        mal_api=mal_api,
        parser_service=parser_service,
        similarity_service=similarity_service,
    )


def main():
    app = build_app()
#    anilist_parsed = app.parser_service.parse_user_anime_list(username=ApplicationConfig.user, status=AniListStatus.WATCHING)
#    nyaa_parsed = app.parser_service.search_and_parse_nyaa(params=NyaaParameters(q="Yofukashi no Uta"))
#    app.logger.debug(anilist_parsed[0])
#    app.logger.debug(nyaa_parsed[0])
    mal_parsed = app.parser_service.parse_user_anime_list(username="xopazaru0343", status=MalStatus.WATCHING)
    app.logger.debug(mal_parsed[1])
#    print(app.mal_api.get_user_ongoing_anime(username="xopazaru0343", status=MalStatus.WATCHING))
#    print(app.mal_api.get_anime_data("21"))
if __name__ == "__main__":
    main()
