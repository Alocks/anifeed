from dataclasses import dataclass
import logging

from anifeed.adapters.aniilist_adapter import AniListAdapter
from anifeed.adapters.nyaa_adapter import NyaaAdapter
from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.models.nyaa_search_model import NyaaParameters
from anifeed.constants.app_config import ApplicationConfig
from anifeed.services.similarity_service import SimilarityService  # optional
from anifeed.utils.log_utils import configure_root_logger, get_logger


@dataclass
class Application:
    logger: logging.Logger
    anilist: AniListAdapter
    nyaa: NyaaAdapter
    similarity_service: SimilarityService = None  # optional


def build_app():
    configure_root_logger(level=logging.DEBUG)
    logger = get_logger(__name__)
    anilist = AniListAdapter()
    nyaa = NyaaAdapter()
    similarity_service = SimilarityService()  # optional
    return Application(
        logger=logger,
        anilist=anilist,
        nyaa=nyaa,
        similarity_service=similarity_service,
    )


def main():
    app = build_app()
    anilist_retval = app.anilist.get_user_anime_list(username=ApplicationConfig.user, status=AnimeStatus.WATCHING)
    nyaa_retval = app.nyaa.fetch_search_result(params=NyaaParameters(q="Yofukashi no Uta"))

    anilist_res = app.anilist.parser.parse_api_metadata(metadata=anilist_retval)
    nyaa_res = app.nyaa.parser.parse_api_metadata(metadata=nyaa_retval)

    app.logger.info(anilist_res[0])
    app.logger.info(nyaa_res[0])


if __name__ == "__main__":
    main()
