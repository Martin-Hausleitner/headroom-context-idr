## Why

Headroom forwards every request to an expensive model without a dedicated, evidence-based preprocessing decision. A reproducible comparison is needed to determine when a cheap prompt enhancer or compressor actually reduces paid context without silently damaging instructions, code, citations, or retrieval quality.

## What Changes

- Create a source-grounded research report covering prompt compression, context selection, semantic summarization, prompt enhancement, and KV-cache-adjacent techniques.
- Produce a 50-repository comparison with current GitHub metadata, a documented 100-point scoring rubric, exactly one overall winner, and proxy-integration criteria.
- Build and run a reproducible benchmark over multiple long prompt classes, reporting tokenizer-specific before/after counts, latency, compression, and quality retention.
- Perform real NotebookLM deep research and preserve its notebook URL, source set, queries, and synthesis in the report.
- Specify a request-time Headroom architecture with policy routing, safety bypasses, observability, rollout gates, and rollback behavior.

## Capabilities

### New Capabilities

- `compression-research-evidence`: Reproducible, traceable evidence for comparing prompt/context compression and enhancement alternatives.
- `headroom-preprocessor-plan`: Decision-ready architecture and rollout plan for a cheap preprocessing stage in Headroom.

### Modified Capabilities

None.

## Impact

The deliverables are documentation, machine-readable research evidence, and benchmark tooling in this repository. The plan targets Headroom's OpenAI-compatible request path at `127.0.0.1:8787`; this change does not modify or deploy the live gateway.

