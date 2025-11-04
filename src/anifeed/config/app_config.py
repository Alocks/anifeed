from dataclasses import dataclass, field
from typing import List

from anifeed.constants.toml_config import APPLICATION_CONFIG


@dataclass
class ApplicationConfig:
    user: str = APPLICATION_CONFIG.get("user")
    api: str = APPLICATION_CONFIG.get("api")
    status: List[str] = field(default_factory=[k for k, v in APPLICATION_CONFIG.get("status").items() if v])
