from pydantic import BaseModel
from typing import Optional, List


class QueryRequest(BaseModel):
    question: str
    domain_filter: Optional[str] = None


class SourceReference(BaseModel):
    document_name: str
    domain: str
    preview: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]


class IngestResponse(BaseModel):
    status: str
    documents_processed: int
