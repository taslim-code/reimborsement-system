# Pydantic models for request/response and metadata
from pydantic import BaseModel
from typing import Optional, List

class InvoiceAnalysisRequest(BaseModel):
    employee_name: str

class InvoiceAnalysisResponse(BaseModel):
    success: bool
    message: str
    details: Optional[List[dict]] = None

class ChatbotQueryRequest(BaseModel):
    query: str
    previous_context: Optional[List[dict]] = None

class ChatbotQueryResponse(BaseModel):
    response: str
    sources: Optional[List[dict]] = None
