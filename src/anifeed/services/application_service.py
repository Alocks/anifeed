from dataclasses import dataclass

from anifeed.services.parser_service import ParserService
from anifeed.services.similarity_service import SimilarityService
from anifeed.utils.log_utils import get_logger


@dataclass
class ApplicationParser:
    logger = get_logger(__name__)
    parser_service: ParserService = ParserService()
    similarity_service: SimilarityService = SimilarityService()
