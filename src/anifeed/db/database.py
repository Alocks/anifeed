from typing import List
from importlib import resources
import sqlite3
import os
from anifeed.utils.commons import UniversalPath

MIGRATIONS_DIR = "anifeed.db.sql"

def init_db() -> None:
    with sqlite3.connect("db/database.db") as conn:
        for name in sorted(resources.contents(MIGRATIONS_DIR)):
            if name.endswith(".sql"):
              script = resources.read_text(MIGRATIONS_DIR, name)
              conn.executescript(script)
        conn.commit()