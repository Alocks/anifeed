import pytest
from unittest.mock import Mock, patch
from anifeed.services.anime_service import AnimeService
from anifeed.services.torrent_service import TorrentService
from anifeed.services.similarity_service import SimilarityService
from anifeed.services.anime_service_factory import (
    create_anime_api_service,
    register_anime_source
)
from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.exceptions import AnimeSourceError


class TestAnimeService:
    @patch('anifeed.services.anime_service.create_anime_api_service')
    def test_anime_service_init(self, mock_factory):
        mock_api = Mock()
        mock_parser = Mock()
        mock_factory.return_value = (mock_api, mock_parser)

        service = AnimeService(source="anilist")

        assert service.source == "anilist"
        mock_factory.assert_called_once()

    @patch('anifeed.services.anime_service.create_anime_api_service')
    def test_get_user_anime_list_success(
        self,
        mock_factory,
        sample_anime_list,
        anilist_api_response
    ):
        mock_api = Mock()
        mock_parser = Mock()
        mock_api.get_user_anime_list.return_value = anilist_api_response
        mock_parser.parse_api_metadata.return_value = sample_anime_list
        mock_factory.return_value = (mock_api, mock_parser)

        service = AnimeService(source="anilist")
        result = service.get_user_anime_list("testuser", AnimeStatus.WATCHING)

        assert len(result) == 2
        assert result[0].title_romaji == "Shingeki no Kyojin"
        mock_api.get_user_anime_list.assert_called_once_with(
            username="testuser",
            status=AnimeStatus.WATCHING
        )

    @patch('anifeed.services.anime_service.create_anime_api_service')
    def test_get_user_anime_list_empty_username(self, mock_factory):
        mock_factory.return_value = (Mock(), Mock())
        service = AnimeService()

        with pytest.raises(ValueError, match="Username cannot be empty"):
            service.get_user_anime_list("", AnimeStatus.WATCHING)

        with pytest.raises(ValueError, match="Username cannot be empty"):
            service.get_user_anime_list("   ", AnimeStatus.WATCHING)

    @patch('anifeed.services.anime_service.create_anime_api_service')
    def test_anime_service_with_mal_source(self, mock_factory):
        mock_factory.return_value = (Mock(), Mock())

        service = AnimeService(source="mal")

        assert service.source == "mal"


class TestTorrentService:
    @patch('anifeed.services.torrent_service.NyaaApi')
    @patch('anifeed.services.torrent_service.NyaaParser')
    def test_torrent_service_init(self, mock_parser_class, mock_api_class):
        TorrentService()

        mock_api_class.assert_called_once()
        mock_parser_class.assert_called_once()

    @patch('anifeed.services.torrent_service.NyaaApi')
    @patch('anifeed.services.torrent_service.NyaaParser')
    def test_search_success(
        self,
        mock_parser_class,
        mock_api_class,
        sample_torrent_list,
        nyaa_html_response
    ):
        mock_api = Mock()
        mock_parser = Mock()
        mock_api.fetch_search_result.return_value = nyaa_html_response
        mock_parser.parse_api_metadata.return_value = sample_torrent_list
        mock_api_class.return_value = mock_api
        mock_parser_class.return_value = mock_parser

        service = TorrentService()
        result = service.search("Yofukashi no Uta")

        assert len(result) == 2
        assert result[0].title == "[SubsPlease] Yofukashi no Uta - 01 [1080p].mkv"
        mock_api.fetch_search_result.assert_called_once()

    @patch('anifeed.services.torrent_service.NyaaApi')
    @patch('anifeed.services.torrent_service.NyaaParser')
    def test_search_empty_query(self, mock_parser_class, mock_api_class):
        service = TorrentService()

        with pytest.raises(ValueError, match="Search query cannot be empty"):
            service.search("")

        with pytest.raises(ValueError, match="Search query cannot be empty"):
            service.search("   ")

    @patch('anifeed.services.torrent_service.NyaaApi')
    @patch('anifeed.services.torrent_service.NyaaParser')
    def test_search_strips_whitespace(self, mock_parser_class, mock_api_class):
        mock_api = Mock()
        mock_api.fetch_search_result.return_value = "<html></html>"
        mock_parser = Mock()
        mock_parser.parse_api_metadata.return_value = []
        mock_api_class.return_value = mock_api
        mock_parser_class.return_value = mock_parser

        service = TorrentService()
        service.search("  test query  ")

        call_args = mock_api.fetch_search_result.call_args[1]
        assert call_args['params'].q == "test query"


class TestSimilarityService:
    def test_similarity_service_init_default(self):
        service = SimilarityService()

        assert service._model is None
        assert service._model_factory is not None

    def test_similarity_service_init_custom_factory(self):
        mock_factory = Mock()

        service = SimilarityService(model_factory=mock_factory)

        assert service._model_factory == mock_factory

    def test_load_model(self, mock_embedding_model):
        factory = Mock(return_value=mock_embedding_model)
        service = SimilarityService(model_factory=factory)

        assert service._model is None
        service.load_model()
        assert service._model is not None
        factory.assert_called_once()

        service.load_model()
        factory.assert_called_once()  # Still only called once

    def test_compute_similarity(self, mock_embedding_model):
        factory = Mock(return_value=mock_embedding_model)
        service = SimilarityService(model_factory=factory)

        results = service.compute(
            "Yofukashi no Uta Season 2",
            ["Yofukashi no Uta S2", "Yofukashi no Uta", "Yofukashi no Uta Mini", "Zero no Tsukaima"]
        )

        assert len(results) == 4
        assert all(isinstance(item, tuple) for item in results)
        assert all(isinstance(item[0], str) and isinstance(item[1], float) for item in results)
        assert results[0][1] > results[1][1] > results[2][1]

    def test_compute_empty_candidates(self):
        service = SimilarityService()

        result = service.compute("query", [])

        assert result == []

    def test_cosine_similarity(self):
        import numpy as np

        a = np.array([1.0, 0.0, 0.0])
        b = np.array([1.0, 0.0, 0.0])
        c = np.array([0.0, 1.0, 0.0])

        # Identical vectors should have similarity 1.0
        sim_ab = SimilarityService._cosine_similarity(a, b)
        assert abs(sim_ab - 1.0) < 0.001

        # Orthogonal vectors should have similarity 0.0
        sim_ac = SimilarityService._cosine_similarity(a, c)
        assert abs(sim_ac) < 0.001


class TestAnimeServiceFactory:
    @patch('anifeed.services.anime_service_factory.AniListApi')
    @patch('anifeed.services.anime_service_factory.AniListParser')
    def test_create_anilist_service(self, mock_parser, mock_api):
        api, parser = create_anime_api_service("anilist")

        mock_api.assert_called_once()
        mock_parser.assert_called_once()

    @patch('anifeed.services.anime_service_factory.MalApi')
    @patch('anifeed.services.anime_service_factory.MalParser')
    def test_create_mal_service(self, mock_parser, mock_api):
        api, parser = create_anime_api_service("mal")

        mock_api.assert_called_once()
        mock_parser.assert_called_once()

    def test_create_unknown_source(self):
        with pytest.raises(AnimeSourceError, match="Unknown anime source"):
            create_anime_api_service("unknown")

    def test_create_case_insensitive(self):
        with patch('anifeed.services.anime_service_factory.AniListApi'):
            with patch('anifeed.services.anime_service_factory.AniListParser'):
                create_anime_api_service("ANILIST")
                create_anime_api_service("AniList")

    def test_register_custom_source(self):
        mock_api = Mock()
        mock_parser = Mock()

        def custom_factory(session, logger):
            return (mock_api, mock_parser)

        register_anime_source("custom", custom_factory)

        api, parser = create_anime_api_service("custom")
        assert api == mock_api
        assert parser == mock_parser
