from typing import Protocol, Sequence, List

import sqlite3 as db
from anifeed.models.anime_model import Anime
from anifeed.models.torrent_model import Torrent
from anifeed.db.mapper import row_to_anime, anime_to_row
from anifeed.utils.commons import UniversalPath
dbpath = UniversalPath("db\\database.db")

INSERT_SQL = """
INSERT OR IGNORE INTO anime (anime_id, source, title_romaji, title_english, status, episodes) 
VALUES (?, ?, ?, ?, ?, ?)"""

SELECT_SQL = """SELECT * FROM anime"""
class AnimeRepository():

    def __init__(self):
        self.connection = db.connect(dbpath)
        
    """Persistence port for cached anime lists."""
    def save_batch(self, animes: Sequence[Anime]) -> None:
        params = [
            anime_to_row(x)
            for x in animes]
        self.cursor = self.connection.cursor()
        self.cursor.executemany(INSERT_SQL, params)
        self.connection.commit()

    def load(self) -> List[Anime]:  # For now just create a simple select with no filters
        self.cursor = self.connection.cursor()
        animes = self.cursor.execute(SELECT_SQL).fetchall()
        rows = [
            row_to_anime(x)
            for x in animes]
        return rows 