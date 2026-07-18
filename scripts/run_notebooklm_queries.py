#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_ID = "4cbe42bf-f9ec-4c8b-8b6c-e6501f50478b"
OUTPUT = ROOT / "research" / "notebooklm" / "queries.json"

QUESTIONS = [
    "Compare LLMLingua, LongLLMLingua, LLMLingua-2, Selective Context, RECOMP, PromptCompressor, 500xCompressor, deterministic compaction, and RAG reranking. For each, state compression mechanism, upstream compression ratio, quality caveats, latency/model requirements, local CPU viability, and suitability as a request-time proxy stage. Cite source numbers for every factual claim.",
    "Distinguish methods that actually reduce transmitted input tokens from KV-cache, prefix-cache, attention, or inference-memory methods that only reduce compute, memory, or time. Explain precisely which KV methods cannot save paid API input tokens in a Headroom proxy using hosted expensive models. Cite sources.",
    "Design a safe adaptive preprocessing policy for Headroom: which message roles and content types must bypass semantic rewriting, when deterministic cleanup should run, when LLMLingua-2 or query-aware extractive compression should run, when a cheap Gemini Flash-class model may compact or enhance, and what fail-open, quality, injection, citation, code, and latency gates are required. Cite sources and separate source facts from recommendations.",
    "Act as an adversarial reviewer. What evidence in this notebook argues against putting a cheap LLM in front of every request? Identify likely quality regressions, prompt-injection risks, cache damage, latency break-even problems, and cases where prompt enhancement increases tokens. Then give the narrowest defensible recommendation for Headroom, with citations.",
    "Synthesize a ranked decision for the external compression component to integrate into Headroom on a 100-point basis emphasizing measured token saving, fidelity, latency, cheap/local operation, proxy integration, reversibility, maturity, and popularity. Do not reward KV-only methods for token savings. Name one winner and explain why alternatives lose, with citations.",
]


def query(question: str) -> dict:
    completed = subprocess.run(
        ["nlm", "query", "notebook", NOTEBOOK_ID, question, "--json", "--timeout", "240"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    results = []
    for index, question in enumerate(QUESTIONS, start=1):
        answer = query(question)
        results.append({"index": index, "question": question, "result": answer})
        print(f"query {index}/{len(QUESTIONS)} complete")
    payload = {
        "notebook_id": NOTEBOOK_ID,
        "notebook_url": f"https://notebooklm.google.com/notebook/{NOTEBOOK_ID}",
        "queried_at_utc": datetime.now(UTC).isoformat(),
        "queries": results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
