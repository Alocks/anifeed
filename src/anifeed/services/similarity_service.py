from typing import List

from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm

from anifeed.utils.log_utils import get_logger


class SimilarityService:
    def __init__(self, logger=None):
        self._model_name = "all-MiniLM-L6-v2"
        self._model = None
        self.logger = logger or get_logger(self.__class__.__name__)

    def load_model(self) -> None:
        if self._model is None:
            self.logger.debug("Loading similarity model from %s", self._model_name)
            self._model = SentenceTransformer(self._model_name)

    def compute(self, to_compare: str, candidates: List[str]) -> List[tuple[str, float]]:
        self.load_model()
        all_strings = [to_compare] + candidates
        embeddings = self._model.encode(all_strings)
        query_vector = embeddings[0]
        candidate_vectors = embeddings[1:]
        similarity_scores = []
        for vector in candidate_vectors:
            score = self.__cosine_similarity(query_vector, vector)
            similarity_scores.append(score)
        return list(zip(candidates, similarity_scores))

    @staticmethod
    def __cosine_similarity(a, b):
        return dot(a, b) / (norm(a) * norm(b))
