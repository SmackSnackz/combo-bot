from embeddings import get_embeddings, rerank
from vector_store import get_collection

def search_documents(query):
    collection = get_collection()
    query_vector = get_embeddings(query, input_type="query")
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=15
    )
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    ranked = rerank(query, docs, top_k=5)

    parts = []
    for item in ranked:
        i = item["index"]
        parts.append(f"[{metas[i]['source']}] {docs[i]}")
    return "\n\n".join(parts)


if __name__ == "__main__":
    print(search_documents("What is RAG?"))