import requests
from config import embed_url, voyage_headers, rerank_url, EMBEDDING_MODEL, RERANK_MODEL
 


def get_embeddings(text, input_type="document"):
    body = {"input": text, "input_type": input_type, "model":EMBEDDING_MODEL}

    response = requests.post(embed_url, json=body, headers=voyage_headers)
    data = response.json()

    if "data" not in data:
        raise RuntimeError(
            f"Voyage request failed. Response: {data}"
        )
    return data["data"][0]["embedding"]


def get_embeddings_batch(texts, input_type="document"):
    """Batch text embeddings. Used for embedding multiple text simultaneously."""
    body = {"input": texts, "input_type": input_type, "model":EMBEDDING_MODEL}

    response = requests.post(embed_url, json=body, headers=voyage_headers)
    data = response.json()

    if "data" not in data:
        raise RuntimeError(
            f"Voyage embedding request failed. Response: {data}"
        )
    return [item["embedding"] for item in data["data"]]


def rerank(query, documents, top_k=3):
    body = {
        "query": query,
        "documents": documents,
        "top_k": top_k,
        "model": RERANK_MODEL,
        "return_documents": False
    }
    response = requests.post(rerank_url, json=body, headers=voyage_headers)
    data = response.json()

    if "data" not in data:
        raise RuntimeError(f"Voyage API error: {data}")
    return data["data"]


















