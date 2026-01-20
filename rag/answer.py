import os
from rag.config import load_openai_client
from rag.retrieve import retrieve

# Parameters
TOP_K = 5                 # Number of chunks to retrieve
LLM_MODEL = "gpt-3.5-turbo"  # Model to generate answers
MAX_TOKENS = 500           # LLM output limit

client = load_openai_client()

def build_prompt(query, retrieved_chunks):
    """
    Construct a prompt that:
    - Includes retrieved chunks
    - Instructs LLM to answer with citations
    """
    context = "\n\n".join(
        [f"[{c['source_file']}] {c['text']}" for c in retrieved_chunks]
    )
    
    prompt = f"""
You are a helpful assistant answering questions about React.

Use only the information in the provided context to answer the question.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{query}

Answer with concise explanation and cite sources in [filename] format.
"""
    return prompt.strip()

def answer_question(query, top_k=TOP_K):
    # Retrieve relevant chunks
    chunks = retrieve(query, k=top_k)

    # Build prompt for LLM
    prompt = build_prompt(query, chunks)

    # Call LLM
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS,
        temperature=0
    )

    answer = resp.choices[0].message.content.strip()
    return answer, chunks

if __name__ == "__main__":
    while True:
        query = input("\nEnter React question (or 'quit'): ")
        if query.lower() in ("quit", "exit"):
            break

        answer, chunks = answer_question(query)
        print("\n=== Answer ===")
        print(answer)
        print("\n=== Retrieved Chunks ===")
        for i, c in enumerate(chunks, 1):
            snippet = c['text'][:200].replace("\n", " ")
            print(f"{i}. [{c['source_file']}] {snippet}...")
