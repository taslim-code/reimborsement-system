# Invoice Reimbursement System

## Project Overview
This system automates invoice analysis against HR reimbursement policy using LLMs and stores results in a vector database. It also provides a RAG chatbot for querying processed invoices.

## Installation Instructions
1. Clone the repository or download the source code.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key as an environment variable (if using OpenAI):
   ```
   set OPENAI_API_KEY=your-openai-key
   ```

## Usage Guide
- Run the FastAPI app:
  ```
  uvicorn app.main:app --reload
  ```
- Access API docs at: http://localhost:8000/docs

## Technical Details
- **Framework:** FastAPI
- **LLM:** OpenAI GPT (or Hugging Face via LangChain)
- **Embeddings:** Sentence-Transformers
- **Vector Store:** ChromaDB
- **PDF Parsing:** PyPDF2

## Endpoints
- `/analyze`: Analyze invoices against policy and store results
- `/chatbot`: Query processed invoices using RAG chatbot

## Prompt Design
- See `app/utils/prompt_utils.py` for prompt templates.

## Code Structure
- Modular, with clear separation for endpoints, utilities, and configuration.

---

For more details, see code comments and docstrings.
