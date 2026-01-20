import json
import time
from datetime import datetime
from pathlib import Path

from rag.retrieve import retrieve
from rag.answer import answer_question

# ---- Config ----

QUESTIONS_PATH = "eval/questions.json"
LOGS_DIR = "logs"
TOP_K = 8
EVAL_MAX_QUESTIONS = 2  # cheap mode

Path(LOGS_DIR).mkdir(exist_ok=True)

# ---- Helpers ----

def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def now_ts():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")

# ---- Eval Runner ----

def run_eval():
    questions = load_questions()
    questions = questions[:EVAL_MAX_QUESTIONS]
    run_id = now_ts()

    results = {
        "run_id": run_id,
        "top_k": TOP_K,
        "num_questions": len(questions),
        "results": []
    }

    print(f"Running eval with TOP_K={TOP_K}")
    print(f"Questions: {len(questions)}\n")

    for q in questions:
        print(f"→ {q['id']}: {q['question']}")

        start = time.time()

        answer, retrieved_chunks = answer_question(
            q["question"],
            top_k=TOP_K
        )

        latency_ms = int((time.time() - start) * 1000)

        results["results"].append({
            "id": q["id"],
            "question": q["question"],
            "expected_sources": q.get("expected_sources", []),
            "retrieved_sources": [
                c["source_file"] for c in retrieved_chunks
            ],
            "answer": answer,
            "latency_ms": latency_ms,
            "manual_score": {
                "correct": None,
                "hallucinated": None,
                "notes": ""
            }
        })

    out_path = f"{LOGS_DIR}/eval_run_{run_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Eval run complete")
    print(f"Saved to {out_path}")

if __name__ == "__main__":
    run_eval()
