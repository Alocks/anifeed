from typing import List

from bs4 import BeautifulSoup

from anifeed.adapters.parsers.base_parser import BaseParser
from anifeed.models.anime_model import Anime


class NyaaParser(BaseParser):
    def parse_api_metadata(self) -> List[Anime]:
        soup = BeautifulSoup(self._api_metadata, 'html.parser')
        res = []
        for row in soup.find('tbody').find_all('tr'):
            content = row.find_all("td")
            links = [x["href"] for x in content[2].find_all("a")]
            res.append(
                Anime(
                    name=content[1].text.replace("\n", ""),
                    torrent_file=links[0],
                    size=content[3].text,
                    seeders=int(content[5].text),
                    leechers=int(content[6].text),
                ))
        return res
