import logging

from socketify import App

from anifeed.api.routers import register_health_route
from anifeed.utils.log_utils import configure_root_logger, get_logger

configure_root_logger(level=logging.INFO)
logger = get_logger(f"anifeed.api.{__name__}")


def create_app() -> App:
    """
    Assemble the Socketify application with all routes and dependencies.
    """
    app = App()
    register_health_route(app)
    return app


app = create_app()


def run(port: int = 8000) -> None:
    """
    Entrypoint for running the API with Socketify.
    """
    def _on_listen(config) -> None:
        port_value = getattr(config, "port", None)
        if callable(port_value):
            try:
                port_value = port_value()
            except TypeError:
                port_value = None
        if port_value is None and hasattr(config, "get_local_port"):
            try:
                port_value = config.get_local_port()
            except TypeError:
                port_value = None
        logger.info("AniFeed API listening on port %s", port_value or port)

    app.listen(port, _on_listen)
    app.run()
