import os

# Base directory (backend/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data paths
KNOWLEDGE_FOLDER = os.path.join(BASE_DIR, "..", "data", "knowledge_docs")
CHROMA_PATH = os.path.join(BASE_DIR, "..", "chroma_db")

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

# Chunking parameters
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# RAG parameters
TOP_K = 6
TEMPERATURE = 0.2

# Ensure knowledge folder exists
os.makedirs(KNOWLEDGE_FOLDER, exist_ok=True)
os.makedirs(CHROMA_PATH, exist_ok=True)
