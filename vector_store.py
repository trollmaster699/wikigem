import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize ChromaDB client. 
# We use PersistentClient to save data locally to a folder.
CHROMA_DATA_PATH = "./chroma_db"
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

# Using a standard embedding function. 
# For testing locally, the default all-MiniLM-L6-v2 is fast and free. 
# For production congruence testing, we can swap this to Gemini embeddings via google-generativeai
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

# Collections (like tables in SQLite)
def get_tips_collection():
    """
    Returns the ChromaDB collection for Tips. 
    This allows us to do semantic search over the extracted tips (e.g. "push knees out")
    """
    return client.get_or_create_collection(
        name="fitness_tips",
        embedding_function=embedding_fn
    )

def get_research_collection():
    """
    Returns the ChromaDB collection for Research Papers.
    Used for Retrieval-Augmented Generation (RAG) when verifying tips.
    """
    return client.get_or_create_collection(
        name="research_papers",
        embedding_function=embedding_fn
    )

def add_tip_to_vector_store(tip_id: str, text: str, metadata: dict = None):
    """
    Converts tip text into an embedding and stores it.
    The tip_id should match the primary key `id` from the SQLite Tip model.
    """
    collection = get_tips_collection()
    collection.add(
        documents=[text],
        metadatas=[metadata] if metadata else [{}],
        ids=[str(tip_id)]
    )

def search_similar_tips(query_text: str, n_results: int = 5):
    """
    Searches the vector store for tips that are semantically similar to the query.
    This is the core of the Congruence Engine.
    """
    collection = get_tips_collection()
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results
