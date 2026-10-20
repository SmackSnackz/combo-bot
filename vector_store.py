
import os
import chromadb

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db")

def get_collection(name= "notes"):
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )