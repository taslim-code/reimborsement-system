# Configuration for API keys, model names, etc.
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
VECTOR_DB_DIR = "./chroma_db"
