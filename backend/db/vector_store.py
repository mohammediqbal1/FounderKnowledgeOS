import chromadb
from core.config import CHROMA_PATH


class VectorStore:
    """Wrapper around ChromaDB for persistent vector storage."""

    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(
            name="founder_knowledge"
        )

    def add_documents(self, ids, embeddings, documents, metadatas):
        """Add document chunks with embeddings and metadata to the store."""
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query(self, embedding, top_k=6, filters=None):
        """Query the vector store for similar documents."""
        kwargs = {
            "query_embeddings": [embedding],
            "n_results": top_k,
        }
        if filters:
            kwargs["where"] = filters

        return self.collection.query(**kwargs)

    def get_all_ids(self):
        """Get all document IDs in the collection."""
        result = self.collection.get()
        return result["ids"] if result["ids"] else []

    def count(self):
        """Return the number of documents in the collection."""
        return self.collection.count()
