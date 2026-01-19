# React Docs RAG Evaluation

## Overview
This project explores how retrieval quality, prompt design, and model choice affect
factual accuracy and hallucination in a Retrieval-Augmented Generation (RAG) system.

The system answers questions over a bounded subset of the official React documentation
and includes an evaluation harness to measure correctness, hallucinations, and regressions
as system parameters change.

The goal is understanding and evaluation, not building a production chatbot.

---

## Corpus
**Source:** Official React documentation  
**Scope:** `reactjs/react.dev/src/content/learn`  
**Format:** Markdown (MDX flattened during ingestion)

The corpus is intentionally limited to the “Learn” section to:
- Keep retrieval precise
- Make evaluation unambiguous
- Reduce cross-topic noise

Third-party documentation content is not included in this repository.

---

## Architecture
High-level flow:

1. Load and clean Markdown documents
2. Chunk content by section and paragraph
3. Embed chunks into a vector store
4. Retrieve top-k chunks for a query
5. Generate answers constrained to retrieved context
6. Log inputs, outputs, and metadata
7. Evaluate results against a fixed question set

```
User Question
      ↓
Retriever (Vector Search)
      ↓
Retrieved Chunks
      ↓
Prompt Builder
      ↓
     LLM
      ↓
Answer + Citations
```

---

## Evaluation Methodology
A fixed set of manually-curated questions is used to evaluate the system.

Each evaluation run records:
- Retrieved chunks
- Model response
- Latency
- Manual scores:
  - Correctness
  - Hallucination (yes/no)
  - Notes

This allows regression testing across changes to:
- Chunk size and overlap
- Retrieval depth (top-k)
- Prompt constraints
- Model choice

---

## Metrics
Primary metrics tracked:
- Answer accuracy (%)
- Hallucination rate (%)
- Unsupported but plausible answers
- Mean latency per query

Evaluation emphasizes **failure modes**, not just aggregate accuracy.

---

## Key Findings
_(To be filled in after experiments)_

Examples:
- Retrieval errors were the dominant failure mode.
- Increasing top-k improved recall but increased hallucinations.
- Prompt strictness reduced hallucinations but lowered answer completeness.
- Code examples biased answers even when semantically irrelevant.

---

## Repository Structure
```text
rag-eval/
├── data/
│   ├── raw/          # excluded from git
│   └── processed/
├── ingest/
├── rag/
├── eval/
├── logs/
├── config.yaml
├── main.py
└── README.md
```

---

## Third-Party Content

This project uses React documentation content sourced from reactjs/react.dev
for evaluation purposes only.

The React documentation is © Meta Platforms, Inc. and is not covered by this
project’s license.

## License
This project’s code is licensed under the MIT License.

Third-party React documentation content is © Meta Platforms, Inc. and not covered by this license.
