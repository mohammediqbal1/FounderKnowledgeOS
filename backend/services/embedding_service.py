from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Singleton-style embedding service using sentence-transformers."""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._instance

    def embed(self, texts: list) -> list:
        """Convert a list of texts to vector embeddings."""
        return self._model.encode(texts).tolist()

    def embed_query(self, text: str) -> list:
        """Convert a single query text to a vector embedding."""
        return self._model.encode([text])[0].tolist()
