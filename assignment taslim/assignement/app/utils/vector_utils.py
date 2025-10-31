# ChromaDB vector store utilities
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(persist_directory="./chroma_db"))

def get_or_create_collection(name="invoices"):
    return client.get_or_create_collection(name)

def add_invoice_embedding(collection, doc_id, embedding, metadata):
    collection.add(
        embeddings=[embedding],
        ids=[doc_id],
        metadatas=[metadata]
    )

def query_collection(collection, query_embedding, filters=None, n_results=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=filters
    )
