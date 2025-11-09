from dataclasses import dataclass
import logging

from anifeed.models import ApplicationConfig
from anifeed.services import AnimeService
from anifeed.services import TorrentService
from anifeed.services import SimilarityService
from anifeed.constants import AnimeStatus
from anifeed.constants import load_application_config
from anifeed.utils.log_utils import configure_root_logger, get_logger
from anifeed.exceptions import AnifeedError


@dataclass
class Application:
    logger: logging.Logger
    anime_service: AnimeService
    torrent_service: TorrentService
    similarity_service: SimilarityService
    config: ApplicationConfig


def build_app() -> Application:
    configure_root_logger(level=logging.INFO)
    logger = get_logger(__name__)
    config = load_application_config()

    return Application(
        logger=logger,
        anime_service=AnimeService(source=config.api),
        torrent_service=TorrentService(),
        similarity_service=SimilarityService(),
        config=config,
    )


def main():
    try:
        app = build_app()
        animes = app.anime_service.get_user_anime_list(
            username=app.config.user,
            status=AnimeStatus.WATCHING
        )

        if animes:
            app.logger.info("%s", animes[0])

            torrents = app.torrent_service.search(
                query=animes[0].title_english or animes[0].title_romaji
            )

            if torrents:
                app.logger.info("%s", torrents[0])

    except AnifeedError as e:
        app.logger.error("Application error: %s", e)
        raise
    except ValueError as e:
        app.logger.error("Validation error: %s", e)
        raise
    except Exception as e:
        app.logger.exception("Unexpected error occurred: %s", e)
        raise


if __name__ == "__main__":
    main()
