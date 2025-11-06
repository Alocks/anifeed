from typing import List, Dict, Any

from bs4 import BeautifulSoup

from anifeed.adapters.parsers.base_parser import BaseParser
from anifeed.models.torrent_model import Torrent


class NyaaParser(BaseParser):
    def parse_api_metadata(self, metadata: Dict[Any, Any]) -> List[Torrent]:
        soup = BeautifulSoup(metadata, 'html.parser')
        res = []
        for row in soup.find('tbody').find_all('tr'):
            content = row.find_all("td")
            links = [x["href"] for x in content[2].find_all("a")]
            res.append(
                Torrent(
                    title=content[1].text.replace("\n", ""),
                    download_url=links[0],
                    size=content[3].text,
                    seeders=int(content[5].text),
                    leechers=int(content[6].text),
                ))
        return res
