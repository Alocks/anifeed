__all__ = ["NyaaParser"]


from typing import List
from dataclasses import dataclass

from bs4 import BeautifulSoup

from anifeed.models.parsers.base_parser import BaseParser


@dataclass
class NyaaMetadata:
    name: str
    torrent_file: str
    size: int
    seeders: int
    leechers: int


class NyaaParser(BaseParser):
    def parse_api_metadata(self) -> List[NyaaMetadata]:
        soup = BeautifulSoup(self._api_metadata, 'html.parser')
        res = []
        for row in soup.find('tbody').find_all('tr'):
            content = row.find_all("td")
            links = [x["href"] for x in content[2].find_all("a")]
            res.append(
                NyaaMetadata(
                    name=content[1].text.replace("\n", ""),
                    torrent_file=links[0],
                    size=content[3].text,
                    seeders=content[4].text,
                    leechers=content[5].text,
                ))
        return res
