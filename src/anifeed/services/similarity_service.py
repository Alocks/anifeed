from typing import List, Optional, Callable, Protocol
from numpy import dot
from numpy.linalg import norm

from anifeed.utils.log_utils import get_logger


class EmbeddingModelProtocol(Protocol):
    def encode(self, texts: List[str]):
        ...


class SimilarityService:
    def __init__(
        self,
        model_factory: Optional[Callable[[], EmbeddingModelProtocol]] = None,
        logger=None
    ):
        self._model_factory = model_factory or self._default_model_factory
        self._model: Optional[EmbeddingModelProtocol] = None
        self.logger = logger or get_logger("anifeed.services.SimilarityService")

    @staticmethod
    def _default_model_factory() -> EmbeddingModelProtocol:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")

    def load_model(self) -> None:
        if self._model is None:
            self.logger.debug("Loading embedding model")
            self._model = self._model_factory()
            self.logger.info("Model loaded successfully")

    def compute(self, to_compare: str, candidates: List[str]) -> List[tuple[str, float]]:
        if not candidates:
            return []

        self.load_model()
        all_strings = [to_compare] + candidates
        embeddings = self._model.encode(all_strings)
        query_vector = embeddings[0]
        candidate_vectors = embeddings[1:]

        results = [
            (candidate, self._cosine_similarity(query_vector, vec))
            for candidate, vec in zip(candidates, candidate_vectors)
        ]

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    @staticmethod
    def _cosine_similarity(a, b) -> float:
        return float(dot(a, b) / (norm(a) * norm(b)))
