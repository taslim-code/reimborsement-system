from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
import zipfile
import io
import uuid
from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.prompt_utils import INVOICE_ANALYSIS_PROMPT
from app.utils.embedding_utils import get_embedding
from app.utils.vector_utils import get_or_create_collection, add_invoice_embedding
import requests
from app.config import GROQ_API_KEY

router = APIRouter()

@router.post("/", summary="Analyze invoices against HR policy")
async def analyze_invoices(
    policy_pdf: UploadFile = File(...),
    invoices_zip: UploadFile = File(...),
    employee_name: str = Form(...)
):
    try:
        # Extract policy text
        policy_text = extract_text_from_pdf(policy_pdf.file)
        # Extract invoice PDFs from ZIP
        invoices = []
        with zipfile.ZipFile(io.BytesIO(await invoices_zip.read())) as z:
            for filename in z.namelist():
                if filename.lower().endswith(".pdf"):
                    with z.open(filename) as f:
                        invoices.append((filename, extract_text_from_pdf(f)))
        # Analyze each invoice
        results = []
        collection = get_or_create_collection()
        for filename, invoice_text in invoices:
            prompt = INVOICE_ANALYSIS_PROMPT.format(policy=policy_text, invoice=invoice_text)
            # Call Groq LLM API
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-70b-8192",  # updated to a supported Groq model
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
            # For simplicity, try to parse JSON from LLM output
            import json
            try:
                analysis = json.loads(llm_output)
            except Exception:
                analysis = {"status": "Unknown", "reason": llm_output}
            # Store in vector DB
            embedding = get_embedding(invoice_text + "\n" + llm_output)
            metadata = {
                "employee_name": employee_name,
                "filename": filename,
                "status": analysis.get("status", "Unknown"),
                "reason": analysis.get("reason", ""),
            }
            doc_id = str(uuid.uuid4())
            add_invoice_embedding(collection, doc_id, embedding, metadata)
            results.append({"filename": filename, **metadata})
        return JSONResponse({"success": True, "message": "Invoices analyzed and stored.", "details": results})
    except Exception as e:
        return JSONResponse({"success": False, "message": str(e)})
