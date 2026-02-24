from fastapi import APIRouter
from services.ingestion_service import IngestionService

router = APIRouter()


@router.post("/ingest")
def ingest_documents():
    """Trigger ingestion of all new PDFs in the knowledge folder."""
    service = IngestionService()
    result = service.ingest()
    return result
