from typing import Protocol, Sequence, List

import sqlite3 as db
from anifeed.models.anime_model import Anime
from anifeed.models.torrent_model import Torrent
from anifeed.db.mapper import row_to_torrent, torrent_to_row
from anifeed.utils.commons import UniversalPath
dbpath = UniversalPath("db\\database.db")

INSERT_SQL = """
INSERT INTO Torrent (torrent_id, title, download_url, size, seeders, leechers, anime_id, anime_source) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

SELECT_SQL = "SELECT * FROM torrent"

class TorrentRepository():

    def __init__(self):
        self.connection = db.connect(dbpath)

    """Optional cache/history port for torrents."""
    def save_batch(self, torrents: Sequence[Torrent], anime_id: int, anime_source: str) -> None:
        params = [
            torrent_to_row(x, anime_id, anime_source)
            for x in torrents]
        self.cursor = self.connection.cursor()
        self.cursor.executemany(INSERT_SQL, params)
        self.connection.commit()

    def load(self) -> List[Torrent]:  # For now just create a simple select with no filters
        self.cursor = self.connection.cursor()
        torrents = self.cursor.execute(SELECT_SQL).fetchall()
        rows = [
            row_to_torrent(x)
            for x in torrents]
        return rows