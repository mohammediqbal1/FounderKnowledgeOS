from core.config import GEMINI_URL, TOP_K, TEMPERATURE
from core.http_client import call_gemini_with_retry
from services.embedding_service import EmbeddingService
from db.vector_store import VectorStore


class RAGService:
    """Retrieval-Augmented Generation service using Gemini API with retry logic."""

    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()

    def build_prompt(self, context_chunks: list, question: str) -> str:
        """Build the final prompt with context and question."""
        context_text = "\n\n---\n\n".join(context_chunks)

        return f"""You are the founder's private knowledge intelligence system.

Answer ONLY based on the provided context below.
If the context does not contain enough information to answer, say: "I don't have enough information in my knowledge base to answer this question."

Context:
{context_text}

Question:
{question}

Provide a clear, structured answer with key points."""

    def query(self, question: str, domain_filter: str = None) -> dict:
        """
        Process a user query through the RAG pipeline.
        
        Args:
            question: The user's natural language question.
            domain_filter: Optional domain category to filter results.
        
        Returns:
            Dict with answer and source references.
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_query(question)

        # Build filters
        filters = {"domain": domain_filter} if domain_filter else None

        # Retrieve top-k relevant chunks
        results = self.vector_store.query(
            query_embedding, top_k=TOP_K, filters=filters
        )

        documents = results["documents"][0] if results["documents"] else []
        metadatas = results["metadatas"][0] if results["metadatas"] else []

        if not documents:
            return {
                "answer": "No relevant documents found in the knowledge base.",
                "sources": [],
            }

        # Build prompt and send to Gemini
        prompt = self.build_prompt(documents, question)

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": TEMPERATURE,
                "maxOutputTokens": 2048,
            },
        }

        try:
            data = call_gemini_with_retry(GEMINI_URL, payload)
            
            answer = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "No response from Gemini.")
            )

        except Exception as e:
            answer = f"Error communicating with Gemini: {str(e)}"

        # Build unique source references
        seen = set()
        sources = []
        for meta in metadatas:
            doc_name = meta.get("document_name", "Unknown")
            if doc_name not in seen:
                seen.add(doc_name)
                sources.append({
                    "document_name": doc_name,
                    "domain": meta.get("domain", "GENERAL"),
                })

        return {"answer": answer, "sources": sources}
