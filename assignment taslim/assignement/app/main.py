from fastapi import FastAPI
from app.endpoints import analyze, chatbot

app = FastAPI(
    title="Invoice Reimbursement System",
    description="Automated invoice analysis and RAG chatbot API",
    version="1.0.0"
)

app.include_router(analyze.router, prefix="/analyze", tags=["Invoice Analysis"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["RAG Chatbot"])
