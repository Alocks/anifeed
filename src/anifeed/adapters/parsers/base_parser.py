from anifeed.utils import log_utils


class BaseParser:
    def __init__(self, session=None, logger=None):
        self.session = session
        self.logger = logger or log_utils.get_logger(__name__)

    def parse_api_metadata(self):
        raise NotImplementedError("parse_api_metadata must be implemented in subclasses")
