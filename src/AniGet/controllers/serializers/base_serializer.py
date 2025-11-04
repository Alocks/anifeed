__all__ = ["BaseSerializer"]

from datetime import datetime
from abc import ABC, abstractmethod
from typing import List

from anifeed.models.parsers.base_parser import AnimeMetadata
from anifeed.utils.commons import UniversalPath


class BaseSerializer(ABC):
    def __init__(self, animes: List[AnimeMetadata]):
        self._animes_list = animes
        self._serialized_animes = self.serialize_animes()

    @property
    def serialized_animes(self) -> str:
        return self._serialized_animes

    @property
    @abstractmethod
    def output_format(self) -> str:
        pass

    @abstractmethod
    def serialize_animes(self) -> str:
        pass

    def write_serialized_output(self):
        curent_time = datetime.now().strftime(format="%Y%m%d_%H%M%S")
        filename_output = f"{curent_time}.{self.output_format}"
        output_path = UniversalPath("output") / filename_output
        with open(file=output_path, mode="w") as f:
            f.write(self.serialized_animes)
