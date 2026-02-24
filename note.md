Founder Knowledge OS v1

Local AI-Powered Personal Knowledge Operating System
Architecture & Technical Specification

1. System Overview
Objective

Build a fully local, AI-powered Personal Knowledge OS that:

Ingests PDFs exported from Google Docs

Extracts and processes textual knowledge

Stores semantic embeddings in a local vector database

Enables Retrieval-Augmented Generation (RAG)

Uses a local LLM (via Ollama)

Provides a minimal localhost web interface

Target user: Single founder (internal tool)
Deployment: Windows, fully local
Scale: ~10–100 PDFs initially

2. Core Functional Capabilities (v1 Scope)
2.1 Ingestion

Manual PDF drop into local folder

Manual “Ingest” trigger

Extract text

Chunk intelligently

Classify document domain

Generate embeddings

Store chunks in vector database

2.2 Query (RAG)

Accept natural language query

Generate embedding for query

Retrieve top-k relevant chunks

Assemble contextual prompt

Send to local LLM

Return synthesized response + source references

3. System Architecture
Frontend (Localhost Web UI)
            ↓
FastAPI (API Layer)
            ↓
Application Services Layer
            ↓
Core Engines
   • Ingestion Engine
   • Chunking Engine
   • Classification Engine
   • Embedding Engine
   • RAG Engine
            ↓
Storage Layer
   • ChromaDB (Vector Store)
   • Local File System (PDFs)
            ↓
Local LLM (Ollama - Mistral)

Architecture Style:

Modular

Service-oriented

Single-user

Local-only

4. Project Structure
FounderOS/
│
├── backend/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── ingest_routes.py
│   │   └── query_routes.py
│   │
│   ├── services/
│   │   ├── ingestion_service.py
│   │   ├── rag_service.py
│   │   ├── embedding_service.py
│   │   └── classification_service.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── chunking.py
│   │   └── utils.py
│   │
│   ├── db/
│   │   └── vector_store.py
│   │
│   └── models/
│       └── schemas.py
│
├── data/
│   └── knowledge_docs/
│
├── chroma_db/
│
└── frontend/
5. Technology Stack
Backend

Python 3.10+

FastAPI

Uvicorn

PDF Processing

PyMuPDF (fitz)

Embeddings

sentence-transformers

Model: all-MiniLM-L6-v2

Vector Database

ChromaDB (persistent mode)

Local LLM

Ollama

Model: mistral (or llama3)

Utility

requests (Ollama API call)

python-dotenv

pydantic

tiktoken (optional for token estimation)

6. Core Modules (Design Specification)
6.1 config.py

Responsible for:

Base directory paths

Chroma DB path

Knowledge docs folder path

Ollama base URL (http://localhost:11434)

Default model name

Chunk size & overlap values

Example config items:

BASE_DIR
KNOWLEDGE_FOLDER
CHROMA_PATH
OLLAMA_URL
LLM_MODEL_NAME
CHUNK_SIZE
CHUNK_OVERLAP
6.2 Chunking Engine (core/chunking.py)

Responsibilities:

Clean extracted text

Split into logical paragraph blocks

Enforce chunk size: 700–900 tokens

Maintain overlap: 100–150 tokens

Output format:

[
   {
      "chunk_id": "...",
      "text": "...",
      "sequence": 1
   }
]
6.3 Embedding Service

Responsibilities:

Load embedding model once (singleton)

Convert list of texts → vector embeddings

Return embeddings as float arrays

Must be efficient and reusable.

6.4 Classification Service

Uses local LLM.

Prompt Template:

Classify the following document into exactly one of:

- ELECTRICAL_CONTRACT
- SEMICONDUCTOR
- AI_SYSTEM
- FINANCIAL
- GENERAL

Document:
{document_text_sample}

Return only the category name.

Output:
Single label string

Stored as metadata for all chunks of document.

6.5 Vector Store (ChromaDB)

Persistent storage path:

FounderOS/chroma_db/

Each stored item contains:

{
  id: chunk_id,
  embedding: vector,
  document: text,
  metadata: {
      document_name,
      domain,
      created_date,
      chunk_index
  }
}

Retrieval:

similarity search

top_k = 5–10

optional metadata filter by domain

6.6 Ingestion Service

Workflow:

Scan data/knowledge_docs/

For each PDF:

Extract text (PyMuPDF)

Clean text

Classify document (once)

Chunk document

Generate embeddings

Store in ChromaDB

Log ingestion results

Important:
Avoid duplicate re-indexing using simple hash check or filename tracking.

6.7 RAG Service

Workflow:

Receive user query

Generate query embedding

Retrieve top_k relevant chunks

Build context string

Construct final prompt:

You are the founder's private knowledge assistant.
Answer based only on provided context.

Context:
{retrieved_chunks}

Question:
{user_query}

If insufficient information, say so clearly.

Send to Ollama API

Return:

Answer

List of referenced documents

7. API Design
POST /ingest

Trigger ingestion process.

Response:

{
  "status": "success",
  "documents_processed": X
}
POST /query

Request body:

{
   "question": "What margin risks did I observe?",
   "domain_filter": "ELECTRICAL_CONTRACT" (optional)
}

Response:

{
   "answer": "...",
   "sources": [
      {
         "document_name": "...",
         "domain": "...",
         "preview": "..."
      }
   ]
}
8. Frontend Specification (Minimal)

Framework:

Basic HTML + Tailwind OR React (minimal)

Layout:

Top:

Title: Founder Knowledge OS

Center:

Input box

Submit button

Below:

Answer section

Side Panel (optional):

List of document references

No login.
No analytics.
No charts.
No multi-user.

9. Performance Considerations

Initial documents: ~10

Chunk count per PDF: approx. 30–60

Total vectors expected: 300–600

Suitable for CPU-only machine

Future scaling requires:

Persistent indexing logic

Embedding batching

Possibly upgrading to more powerful model

10. Security & Privacy

Fully local

No external API calls

LLM runs via Ollama locally

Sensitive tender data never leaves machine

11. Future Extensions (Not in v1)

File watcher auto-ingestion

Google Drive API sync

Knowledge graph visualization

Pattern detection across projects

Margin trend analytics

Timeline evolution analysis

Multi-user SaaS architecture

12. Development Phases
Phase 1

Environment setup

Phase 2

Core ingestion logic

Phase 3

Vector store integration

Phase 4

RAG pipeline

Phase 5

Minimal UI

13. Design Philosophy

Every feature must:

Improve recall
OR

Improve synthesis

Avoid feature creep.

This system is built to compound long-term founder knowledge.

End of Specification