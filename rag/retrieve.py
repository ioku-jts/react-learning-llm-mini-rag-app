import json
import faiss
import numpy as np
from rag.config import load_openai_client
client = load_openai_client()

INDEX_PATH = "data/processed/react_docs.index"
METADATA_PATH = "data/processed/metadata.json"
EMBED_MODEL = "text-embedding-3-small"
TOP_K = 5

def embed_query(query: str):
    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=query
    )
    return np.array(resp.data[0].embedding).astype("float32")

def load_index():
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

def retrieve(query: str):
    index, metadata = load_index()
    q_embedding = embed_query(query).reshape(1, -1)
    _, indices = index.search(q_embedding, TOP_K)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])
    return results

if __name__ == "__main__":
    query = "Why shouldn't you call hooks conditionally?"
    results = retrieve(query)

    for i, r in enumerate(results):
        print(f"\n--- Result {i+1} ({r['source_file']}) ---")
        print(r["text"][:500])
