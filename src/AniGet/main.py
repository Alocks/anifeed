from dataclasses import dataclass
import logging

from anifeed.utils.log_utils import configure_root_logger, get_logger
from anifeed.models.apis.anilist_api import AniListApi
from anifeed.models.apis.nyaa_api import NyaaApi
from anifeed.services.similarity_service import SimilarityService  # optional
from anifeed.services.parser_service import ParserService  # optional


@dataclass
class Application:
    logger: logging.Logger
    ani_api: AniListApi
    nyaa_api: NyaaApi
    parser_service: ParserService = None  # optional
    similarity_service: SimilarityService = None  # optional


def build_app():
    configure_root_logger(level=logging.DEBUG)
    logger = get_logger(__name__)
    ani_api = AniListApi(logger=logger)
    nyaa_api = NyaaApi(logger=logger)
    parser_service = ParserService(ani_api=ani_api, nyaa_api=nyaa_api, logger=logger)  # optional
    similarity_service = SimilarityService(logger=logger)  # optional
    return Application(
        logger=logger,
        ani_api=ani_api,
        nyaa_api=nyaa_api,
        parser_service=parser_service,
        similarity_service=similarity_service,
    )


def main():
    app = build_app()


if __name__ == "__main__":
    main()
