from types import MappingProxyType

from anifeed.models.config_model import ApplicationConfig, NyaaConfig
from anifeed.utils.commons import TomlParser


def load_application_config() -> ApplicationConfig:
    """Factory function to load config"""
    app_config = MappingProxyType(TomlParser.get_config("application"))
    nyaa_config = MappingProxyType(TomlParser.get_config("nyaa"))
    status_dict = app_config.get("status", {})
    enabled_statuses = [k for k, v in status_dict.items() if v]
    nyaa_config = NyaaConfig(
        batch=nyaa_config.get("batch"),
        fansub=nyaa_config.get("fansub"),
        resolution=nyaa_config.get("resolution")
        )
    return ApplicationConfig(
        user=app_config.get("user"),
        api=app_config.get("api"),
        status=enabled_statuses,
        nyaa_config=nyaa_config

    )
