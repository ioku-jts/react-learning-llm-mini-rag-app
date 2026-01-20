import json
import os
import faiss
import numpy as np
from rag.config import load_openai_client

CHUNKS_PATH = "data/processed/chunks.json"
INDEX_PATH = "data/processed/react_docs.index"
METADATA_PATH = "data/processed/metadata.json"

EMBED_MODEL = "text-embedding-3-small"
BATCH_SIZE = 50      # safe batch size for free tier
MAX_CHUNKS = None     # max chunks to embed initially (set smaller for testing)

os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

client = load_openai_client()

def embed_batch(texts):
    """
    Embed a list of texts and return embeddings as a float32 numpy array.
    """
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return np.array([d.embedding for d in resp.data], dtype="float32")

def main():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        all_chunks = json.load(f)

    # Optionally limit chunks to conserve free quota
    if MAX_CHUNKS:
        all_chunks = all_chunks[:MAX_CHUNKS]

    texts = [c["text"] for c in all_chunks]

    embeddings = []
    print(f"Embedding {len(texts)} chunks in batches of {BATCH_SIZE}...")
    for i in range(0, len(texts), BATCH_SIZE):
        batch_texts = texts[i:i+BATCH_SIZE]
        batch_embeddings = embed_batch(batch_texts)
        embeddings.extend(batch_embeddings)
        print(f"  Embedded chunks {i+1}-{i+len(batch_texts)}")

    embeddings = np.array(embeddings, dtype="float32")

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"✅ Saved FAISS index to {INDEX_PATH}")
    print(f"✅ Saved metadata to {METADATA_PATH}")

if __name__ == "__main__":
    main()
