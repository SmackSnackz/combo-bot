def chunk_by_size(text, chunk_size, overlap=0):
    """Chunk text by fixed size."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    print(chunk_by_size("abcdefghijklmnopqrst", 10, 2))