import os
import glob
from chunking import chunk_by_size
from embeddings import get_embeddings_batch
from vector_store import get_collection

DOCS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

def load_documents():
    documents = {}
    for path in sorted(glob.glob(os.path.join(DOCS_FOLDER, "*.txt"))):
        filename = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            documents[filename] = f.read()
    return documents

def ingest_documents():
    collection = get_collection()
    documents = load_documents()
    for source_name, text in documents.items():
        chunks = chunk_by_size(text, chunk_size=500, overlap=100)
        vectors = get_embeddings_batch(chunks)
        ids = [f"{source_name}_{i}" for i in range (len(chunks))]
        metadatas = [{"source": source_name, "chunk_index": i} for i in range (len(chunks))]
        collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=chunks,
            metadatas=metadatas
        )
        print(f"indexed {source_name}: {len(chunks)} chunks")

if __name__ == "__main__":
    ingest_documents()