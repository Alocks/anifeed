from unittest.mock import patch
from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.constants.nyaa_search_enum import (
    NyaaCategory, NyaaFilter, NyaaColumnToOrder, NyaaOrder
)
from anifeed.constants.app_config import load_application_config
from anifeed.models.config_model import ApplicationConfig


class TestAnimeStatusEnum:
    def test_enum_members(self):
        assert hasattr(AnimeStatus, 'WATCHING')
        assert hasattr(AnimeStatus, 'PLANNING')
        assert hasattr(AnimeStatus, 'COMPLETED')
        assert hasattr(AnimeStatus, 'DROPPED')
        assert hasattr(AnimeStatus, 'PAUSED')
        assert hasattr(AnimeStatus, 'REPEATING')


class TestNyaaSearchEnums:
    def test_nyaa_category_values(self):
        assert NyaaCategory.DEFAULT.value == "1_0"
        assert NyaaCategory.ENGLISH_TRANSLATED.value == "1_2"
        assert NyaaCategory.NON_ENGLISH_TRANSLATED.value == "1_3"
        assert NyaaCategory.RAW.value == "1_4"

    def test_nyaa_filter_values(self):
        assert NyaaFilter.NO_FILTER.value == "0"
        assert NyaaFilter.NO_REMAKES.value == "1"
        assert NyaaFilter.TRUSTED_ONLY.value == "2"

    def test_nyaa_column_order_values(self):
        assert NyaaColumnToOrder.SEEDS.value == "seeders"
        assert NyaaColumnToOrder.SIZE.value == "size"
        assert NyaaColumnToOrder.DOWNLOADS.value == "download"
        assert NyaaColumnToOrder.LEECHERS.value == "leechers"

    def test_nyaa_order_values(self):
        assert NyaaOrder.ASCENDING.value == "asc"
        assert NyaaOrder.DESCENDING.value == "desc"


class TestAppConfig:
    @patch('anifeed.constants.app_config.TomlParser')
    def test_load_application_config(self, mock_toml_parser):
        mock_toml_parser.get_config.side_effect = [
            {
                "user": "testuser",
                "api": "anilist",
                "status": {"WATCHING": True, "COMPLETED": False}
            },
            {
                "batch": ["[batch]"],
                "fansub": ["[SubsPlease]"],
                "resolution": ["1080p"]
            }
        ]

        config = load_application_config()

        assert isinstance(config, ApplicationConfig)
        assert config.user == "testuser"
        assert config.api == "anilist"
        assert config.status == ["WATCHING"]
        assert config.nyaa_config.batch == ["[batch]"]

    @patch('anifeed.constants.app_config.TomlParser')
    def test_load_config_with_all_statuses_enabled(self, mock_toml_parser):
        mock_toml_parser.get_config.side_effect = [
            {
                "user": "user",
                "api": "mal",
                "status": {
                    "WATCHING": True,
                    "COMPLETED": True,
                    "PLANNING": True,
                    "PAUSE": True,
                    "DROPPED": True,
                }
            },
            {"batch": [], "fansub": [], "resolution": []}
        ]

        config = load_application_config()
        assert len(config.status) == 5
        assert "WATCHING" in config.status
        assert "COMPLETED" in config.status
        assert "PLANNING" in config.status
        assert "PAUSE" in config.status
        assert "DROPPED" in config.status
