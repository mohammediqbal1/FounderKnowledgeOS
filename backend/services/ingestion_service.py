import os
import time
import uuid
import fitz  # PyMuPDF
from datetime import datetime

from core.config import KNOWLEDGE_FOLDER
from core.chunking import chunk_text
from core.utils import compute_file_hash
from services.embedding_service import EmbeddingService
from services.classification_service import classify_document
from db.vector_store import VectorStore


class IngestionService:
    """Service to ingest PDFs into the vector store."""

    def __init__(self):
        self.embedder = EmbeddingService()
        self.vector_store = VectorStore()
        self._processed_hashes_file = os.path.join(
            KNOWLEDGE_FOLDER, ".processed_hashes"
        )

    def _load_processed_hashes(self) -> set:
        """Load the set of already-processed file hashes."""
        if os.path.exists(self._processed_hashes_file):
            with open(self._processed_hashes_file, "r") as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def _save_hash(self, file_hash: str):
        """Append a hash to the processed hashes file."""
        with open(self._processed_hashes_file, "a") as f:
            f.write(file_hash + "\n")

    def extract_text(self, file_path: str) -> str:
        """Extract all text from a PDF file using PyMuPDF."""
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    def ingest(self) -> dict:
        """
        Scan the knowledge folder, process new PDFs, and store them
        in the vector database.
        
        Returns:
            Dict with status and number of documents processed.
        """
        processed_hashes = self._load_processed_hashes()
        documents_processed = 0

        pdf_files = [
            f for f in os.listdir(KNOWLEDGE_FOLDER)
            if f.lower().endswith(".pdf")
        ]

        for file_name in pdf_files:
            file_path = os.path.join(KNOWLEDGE_FOLDER, file_name)

            # Skip already-processed files
            file_hash = compute_file_hash(file_path)
            if file_hash in processed_hashes:
                print(f"[Ingestion] Skipping already processed: {file_name}")
                continue

            print(f"[Ingestion] Processing: {file_name}")

            # Extract text
            text = self.extract_text(file_path)
            if not text.strip():
                print(f"[Ingestion] No text found in: {file_name}")
                continue

            # Classify document domain
            domain = classify_document(text)
            print(f"[Ingestion] Classified '{file_name}' as: {domain}")

            # Throttle to avoid 429 errors on free tier
            time.sleep(2)

            # Chunk the text
            chunks = chunk_text(text)
            if not chunks:
                continue

            # Generate embeddings
            embeddings = self.embedder.embed(chunks)

            # Create IDs and metadata
            ids = [str(uuid.uuid4()) for _ in chunks]
            metadatas = [
                {
                    "document_name": file_name,
                    "domain": domain,
                    "created_date": datetime.now().isoformat(),
                    "chunk_index": i,
                }
                for i in range(len(chunks))
            ]

            # Store in vector database
            self.vector_store.add_documents(ids, embeddings, chunks, metadatas)

            # Mark as processed
            self._save_hash(file_hash)
            documents_processed += 1
            print(f"[Ingestion] Done: {file_name} ({len(chunks)} chunks)")

        return {
            "status": "success",
            "documents_processed": documents_processed,
        }
