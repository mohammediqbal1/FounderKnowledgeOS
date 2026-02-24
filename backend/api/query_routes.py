from fastapi import APIRouter
from models.schemas import QueryRequest
from services.rag_service import RAGService

router = APIRouter()


@router.post("/query")
def query_knowledge(req: QueryRequest):
    """Query the knowledge base using RAG."""
    service = RAGService()
    return service.query(req.question, req.domain_filter)
