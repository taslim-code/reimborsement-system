from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..utils.vector_utils import get_or_create_collection, query_collection
from ..utils.embedding_utils import get_embedding
from ..utils.prompt_utils import CHATBOT_SYSTEM_PROMPT
from ..config import GROQ_API_KEY
import requests

router = APIRouter()

@router.post("/", summary="RAG Chatbot for invoice queries")
async def chatbot_query(request: Request):
    data = await request.json()
    query = data.get("query", "")
    if not query:
        return JSONResponse({"response": "No query provided."})
    # Embed the query
    query_embedding = get_embedding(query)
    # Try to extract metadata filters from the query (simple example)
    filters = {}
    if "declined" in query.lower():
        filters["status"] = "Declined"
    # Add more parsing as needed for employee name, etc.
    if "samad" in query.lower():
        filters["employee_name"] = "samad"
    collection = get_or_create_collection()
    if filters:
        results = query_collection(collection, query_embedding, filters=filters, n_results=5)
    else:
        results = query_collection(collection, query_embedding, n_results=5)
    docs = []
    for md in results.get("metadatas", [[]])[0]:
        docs.append(f"Invoice: {md.get('filename')}\nStatus: {md.get('status')}\nReason: {md.get('reason')}")
    # Compose context for LLM
    context = "\n---\n".join(docs)
    prompt = CHATBOT_SYSTEM_PROMPT + "\n\n" + context + f"\n\nUser Query: {query}"
    # Call Groq LLM API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": prompt}
        ]
    }
    groq_url = "https://api.groq.com/openai/v1/chat/completions"
    groq_response = requests.post(groq_url, headers=headers, json=payload)
    if groq_response.ok:
        llm_output = groq_response.json()["choices"][0]["message"]["content"]
    else:
        llm_output = f"Groq API error: {groq_response.text}"
    return JSONResponse({"response": llm_output})
