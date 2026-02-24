Founder Knowledge OS v1
Full Developer Build Plan with Code Skeleton
1️⃣ Development Phases Overview
Phase	Goal	Output
Phase 1	Core Config & Vector DB	Persistent vector layer
Phase 2	Embedding Engine	Semantic embedding system
Phase 3	Ingestion Engine	PDF → Chunks → Vectors
Phase 4	RAG Engine	Retrieval + LLM Synthesis
Phase 5	API Layer	Query & Ingest endpoints
Phase 6	Minimal Frontend	Localhost UI
2️⃣ Phase 1 — Core Config + Vector Store
📁 backend/core/config.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KNOWLEDGE_FOLDER = os.path.join(BASE_DIR, "..", "data", "knowledge_docs")
CHROMA_PATH = os.path.join(BASE_DIR, "..", "chroma_db")

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL_NAME = "mistral"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

TOP_K = 6
TEMPERATURE = 0.2
📁 backend/db/vector_store.py
import chromadb
from chromadb.config import Settings
from core.config import CHROMA_PATH

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(
            Settings(persist_directory=CHROMA_PATH)
        )
        self.collection = self.client.get_or_create_collection(
            name="founder_knowledge"
        )

    def add_documents(self, ids, embeddings, documents, metadatas):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def query(self, embedding, top_k=6, filters=None):
        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=filters
        )
3️⃣ Phase 2 — Embedding Engine
📁 backend/services/embedding_service.py
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()
4️⃣ Phase 3 — Chunking + Classification + Ingestion
📁 backend/core/chunking.py
def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks
📁 backend/services/classification_service.py
import requests
from core.config import OLLAMA_URL, LLM_MODEL_NAME

CATEGORIES = [
    "ELECTRICAL_CONTRACT",
    "SEMICONDUCTOR",
    "AI_SYSTEM",
    "FINANCIAL",
    "GENERAL"
]

def classify_document(text):
    prompt = f"""
Assign exactly ONE category from:
{CATEGORIES}

Document:
{text[:1500]}

Return only the category name.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL_NAME,
            "prompt": prompt,
            "temperature": 0
        }
    )

    result = response.json()["response"].strip()
    return result
📁 backend/services/ingestion_service.py
import os
import fitz
import uuid
from core.config import KNOWLEDGE_FOLDER
from core.chunking import chunk_text
from services.embedding_service import EmbeddingService
from services.classification_service import classify_document
from db.vector_store import VectorStore

class IngestionService:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()

    def extract_text(self, file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def ingest(self):
        for file_name in os.listdir(KNOWLEDGE_FOLDER):
            if not file_name.endswith(".pdf"):
                continue

            file_path = os.path.join(KNOWLEDGE_FOLDER, file_name)
            text = self.extract_text(file_path)

            domain = classify_document(text)

            chunks = chunk_text(text)

            embeddings = self.embedder.embed(chunks)

            ids = [str(uuid.uuid4()) for _ in chunks]

            metadatas = [{
                "document_name": file_name,
                "domain": domain
            } for _ in chunks]

            self.vector_store.add_documents(
                ids, embeddings, chunks, metadatas
            )

        return {"status": "success"}
5️⃣ Phase 4 — RAG Engine
📁 backend/services/rag_service.py
import requests
from core.config import OLLAMA_URL, LLM_MODEL_NAME, TOP_K, TEMPERATURE
from services.embedding_service import EmbeddingService
from db.vector_store import VectorStore

class RAGService:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()

    def build_prompt(self, context_chunks, question):
        context_text = "\n\n".join(context_chunks)

        return f"""
You are the founder’s private knowledge intelligence system.

Answer ONLY from the provided context.

Context:
{context_text}

Question:
{question}
"""

    def query(self, question, domain_filter=None):
        query_embedding = self.embedder.embed_query(question)

        filters = {"domain": domain_filter} if domain_filter else None

        results = self.vector_store.query(
            query_embedding,
            top_k=TOP_K,
            filters=filters
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        prompt = self.build_prompt(documents, question)

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": LLM_MODEL_NAME,
                "prompt": prompt,
                "temperature": TEMPERATURE
            }
        )

        return {
            "answer": response.json()["response"],
            "sources": metadatas
        }
6️⃣ Phase 5 — API Layer
📁 backend/api/ingest_routes.py
from fastapi import APIRouter
from services.ingestion_service import IngestionService

router = APIRouter()

@router.post("/ingest")
def ingest_documents():
    service = IngestionService()
    return service.ingest()
📁 backend/api/query_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.rag_service import RAGService

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    domain_filter: str | None = None

@router.post("/query")
def query_knowledge(req: QueryRequest):
    service = RAGService()
    return service.query(req.question, req.domain_filter)
📁 backend/main.py
from fastapi import FastAPI
from api.ingest_routes import router as ingest_router
from api.query_routes import router as query_router

app = FastAPI()

app.include_router(ingest_router)
app.include_router(query_router)

Run:

uvicorn main:app --reload
7️⃣ Phase 6 — Minimal Frontend (Optional Starter)

Simple HTML file:

<h1>Founder Knowledge OS</h1>
<input id="question" />
<button onclick="ask()">Ask</button>

<script>
async function ask() {
    const question = document.getElementById("question").value;
    const response = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
    });

    const data = await response.json();
    console.log(data);
}
</script>
8️⃣ Final System Ready

You now have:

Modular architecture

Clean separation of services

Local RAG engine

Domain-aware classification

Scalable structure

Founder-grade knowledge engine