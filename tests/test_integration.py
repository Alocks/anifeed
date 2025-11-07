from unittest.mock import patch, Mock
from anifeed.services.anime_service import AnimeService
from anifeed.services.torrent_service import TorrentService
from anifeed.constants.anime_status_enum import AnimeStatus


class TestAnimeToTorrentWorkflow:
    @patch('anifeed.services.anime_service.create_anime_api_service')
    @patch('anifeed.services.torrent_service.NyaaApi')
    @patch('anifeed.services.torrent_service.NyaaParser')
    def test_fetch_anime_then_search_torrents(
        self,
        mock_nyaa_parser_class,
        mock_nyaa_api_class,
        mock_anime_factory,
        sample_anime_list,
        sample_torrent_list
    ):
        """Test fetching anime and then searching for torrents"""
        mock_anime_api = Mock()
        mock_anime_parser = Mock()
        mock_anime_api.get_user_anime_list.return_value = {"data": {}}
        mock_anime_parser.parse_api_metadata.return_value = sample_anime_list
        mock_anime_factory.return_value = (mock_anime_api, mock_anime_parser)

        mock_torrent_api = Mock()
        mock_torrent_parser = Mock()
        mock_torrent_api.fetch_search_result.return_value = "<html></html>"
        mock_torrent_parser.parse_api_metadata.return_value = sample_torrent_list
        mock_nyaa_api_class.return_value = mock_torrent_api
        mock_nyaa_parser_class.return_value = mock_torrent_parser

        anime_service = AnimeService(source="anilist")
        torrent_service = TorrentService()

        animes = anime_service.get_user_anime_list("testuser", AnimeStatus.WATCHING)
        assert len(animes) > 0

        first_anime = animes[0]
        search_query = first_anime.title_english or first_anime.title_romaji
        torrents = torrent_service.search(search_query)

        assert len(torrents) > 0
        assert torrents[0].seeders > 0
