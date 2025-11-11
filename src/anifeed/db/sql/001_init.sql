CREATE TABLE IF NOT EXISTS anime(
        anime_id INTEGER,
        source TEXT ,
        title_romaji TEXT , 
        title_english TEXT , 
        status TEXT, 
        episodes INTEGER,
        PRIMARY KEY(anime_id, source)
        );
CREATE TABLE IF NOT EXISTS torrent(
        torrent_sk INTEGER PRIMARY KEY AUTOINCREMENT,
        torrent_id INTEGER,
        title TEXT, 
        download_url TEXT, 
        size TEXT , 
        seeders INTEGER, 
        leechers INTEGER,
        anime_id INTEGER,
        anime_source TEXT,
        UNIQUE (torrent_sk, torrent_id)
        FOREIGN KEY(anime_id, anime_source) REFERENCES anime(anime_id, source)
        );