# ...existing code...
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Any
from anifeed.utils import log_utils


class BaseApi:
    def __init__(self,
                 base_url: Optional[str] = None,
                 session: Optional[requests.Session] = None,
                 logger=None
                 ):
        self.base_url = base_url
        self.session = session or self._create_session()
        self.logger = logger or log_utils.get_logger(self.__class__.__name__)

    def _create_session(self) -> requests.Session:
        s = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist={500, 502, 503, 504})
        adapter = HTTPAdapter(max_retries=retries)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        return s

    def _build_url(self, path: Optional[str]) -> str:
        if not path:
            return self.base_url or ""
        if self.base_url and not path.startswith("http"):
            return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        return path

    def get(self, path: Optional[str] = None, **kwargs) -> requests.Response:
        url = self._build_url(path)
        self.logger.debug("HTTP GET %s %s", url, kwargs)
        return self.session.get(url, **kwargs)

    def post(self, path: Optional[str] = None, json: Any = None, data: Any = None, **kwargs) -> requests.Response:
        url = self._build_url(path)
        self.logger.debug("HTTP POST %s json=%s data=%s kwargs=%s", url, json, data, kwargs)
        return self.session.post(url, json=json, data=data, **kwargs)
