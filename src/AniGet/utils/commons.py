__all__ = ["UniversalPath"]

from pathlib import Path
from typing import Union
import tomllib
import os


class UniversalPath:
    def __init__(self, path_string: Union[str, 'Path']):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._path = os.path.join(base_dir, str(path_string))

    def __str__(self) -> str:
        return self._path

    def __repr__(self) -> str:
        return f'Path("{self._path}")'

    def __fspath__(self) -> str:
        return self._path

    def __truediv__(self, other: Union[str, 'Path']) -> 'Path':
        other_path = str(other)
        retVal = os.path.join(self._path, other_path)
        return UniversalPath(retVal)


class DictWrangler:
    @classmethod
    def find_value_recursively(cls, data, target_key):
        if isinstance(data, dict):
            if target_key in data:
                return data[target_key]

            for key, value in data.items():
                result = DictWrangler.find_value_recursively(value, target_key)
                if result is not None:
                    return result

        elif isinstance(data, list):
            for item in data:
                result = DictWrangler.find_value_recursively(item, target_key)
                if result is not None:
                    return result
        return None


class TomlParser:
    @classmethod
    def get_config(cls, table_name: str) -> Dict:
        with open(file=UniversalPath("config.toml"), mode="rb") as f:
            retVal = tomllib.load(f).get(table_name)
        return retVal
