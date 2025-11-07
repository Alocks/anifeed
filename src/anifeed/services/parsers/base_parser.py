from typing import Any

from anifeed.utils import log_utils


class BaseParser:
    def __init__(self, logger=None):
        self.logger = logger or log_utils.get_logger(f"anifeed.services.{self.__class__.__name__}")

    def parse_api_metadata(self, metadata: Any):
        raise NotImplementedError("parse_api_metadata must be implemented in subclasses")
