from typing import Sequence
from anifeed.models.anime_model import Anime
from anifeed.models.torrent_model import Torrent
from dataclasses import dataclass
from sqlite3 import Row

def row_to_anime(row: list[tuple]) -> Anime:
    return Anime(
        anime_id=row[0],
        source=row[1],
        title_romaji=row[2],
        title_english=row[3],
        status=row[4],
        episodes=row[5]
    )    
def anime_to_row(anime: Anime) -> Sequence:
    return (
        anime.anime_id,
        anime.source,
        anime.title_romaji,
        anime.title_english,
        anime.status,
        anime.episodes
    )
    
def row_to_torrent(row: Row) -> Torrent:
    return Torrent(
        torrent_id=row[1],
        title=row[2],
        download_url=row[3],
        size=row[4],
        seeders=row[5],
        leechers=row[6],
        anime_id=row[7],
        anime_source=row[8]
    )    
def torrent_to_row(torrent: Torrent, anime_id: int, anime_source: str) -> Sequence:
    return (
        torrent.torrent_id,
        torrent.title,
        torrent.download_url,
        torrent.size,
        torrent.seeders,
        torrent.leechers,
        anime_id,
        anime_source
    )