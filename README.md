# 🧠 Founder Knowledge OS v1

### Local AI-Powered Personal Knowledge Operating System

Founder Knowledge OS is a high-performance, privacy-first technical intelligence platform designed for founders. It allows you to ingest complex PDFs (Technical Tenders, Semiconductor Specs, Financial Reports), semantically index them using local embeddings, and query them using the state-of-the-art **Gemini 2.0 Flash** API with a robust RAG (Retrieval-Augmented Generation) pipeline.

![Status](https://img.shields.io/badge/Status-Live-success?style=for-the-badge)
![Tech](https://img.shields.io/badge/Stack-Python%20|%20FastAPI%20|%20ChromaDB-blue?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-orange?style=for-the-badge)

---

## 🚀 Key Features

*   **⚡ Gemini 2.0 Flash Intelligence**: Blazing fast, high-quality answers derived from your private documents.
*   **🛡️ Privacy First**: Your documents stay local. We only send relevant context chunks to the LLM; your original files never leave your machine.
*   **🔍 Semantic Retrieval**: Go beyond keyword search. Find information based on meaning and context across hundreds of PDF pages.
*   **📂 Automatic Domain Classification**: Intelligent document sorting into categories (Electrical, Semiconductor, Finance, AI, General).
*   **🔄 Robust Rate Limiting**: Built-in exponential backoff and ingestion throttling to maximize performance on Gemini Free Tier.
*   **✨ Premium UI**: Modern glassmorphism landing page and a polished, dark-theme intelligence interface.
*   **📦 Local Vector Storage**: Persistent indexing using ChromaDB for instant recall.

---

## 📂 Project Structure

```text
Founder_Knowledge_OS/
├── backend/                # FastAPI Application
│   ├── api/                # Route definitions (Ingest, Query)
│   ├── core/               # Config, Chunking, HTTP Client
│   ├── db/                 # ChromaDB Vector Store wrapper
│   ├── services/           # RAG, Embedding, Ingestion, Classification
│   └── main.py             # Entry point & Routing Hub
├── data/
│   └── knowledge_docs/     # [LOCAL ONLY] Drop your PDFs here
├── frontend/
│   ├── index.html          # Premium Landing Page
│   └── app.html            # Core Intelligence Interface
├── chroma_db/              # [LOCAL ONLY] Persistent Vector Database
├── .env                    # [LOCAL ONLY] API Keys & Secrets
├── requirements.txt        # Python Dependencies
└── README.md               # You are here
```

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/mohammediqbal1/pytube.git
cd Founder_Knowledge_OS
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application
Start the backend server:
```bash
cd backend
python -m uvicorn main.py:app --reload --host 0.0.0.0 --port 8000
```

---

## 📖 How to Use

1.  **Ingest Data**: Drop your PDF documents into `data/knowledge_docs/`.
2.  **Launch Dashboard**: Navigate to `http://localhost:8000`.
3.  **Process Documents**: Click **📥 Ingest Documents** to index your library.
4.  **Ask Questions**: Use the chat interface to query your specialized knowledge base.

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **PDF Engine**: PyMuPDF (fitz)
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **LLM**: Google Gemini 2.0 Flash
- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), JavaScript

---

## 🛡️ Security Note
The system is configured via `.gitignore` to **NEVER** push your `data/` folder, `chroma_db/`, or `.env` file to GitHub. Your internal notes and sensitive keys remain strictly on your local machine.

---
Built with ❤️ for Founders.
