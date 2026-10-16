MODEL = "claude-haiku-4-5-20251001"
EMBEDDING_MODEL = "voyage-4-lite"
RERANK_MODEL = "rerank-2.5-lite"
import os 

from dotenv import load_dotenv
load_dotenv(override=True)
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
voyage_api_key = os.getenv("VOYAGE_API_KEY")

embed_url = "https://api.voyageai.com/v1/embeddings"
rerank_url = "https://api.voyageai.com/v1/rerank"
anthropic_url = "https://api.anthropic.com/v1/messages"

voyage_headers = {
    "Authorization": f"Bearer {voyage_api_key}",
    "Content-Type": "application/json",
}

anthropic_headers = {
    "x-api-key": anthropic_api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}