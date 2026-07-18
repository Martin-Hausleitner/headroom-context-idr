## Context

The brief asks for a plan rather than a live gateway modification, but the recommendation must be based on current OSS repositories, real token measurements, quality checks, and genuine NotebookLM research. Compression techniques differ materially: extractive token pruning, retrieval/reranking, abstractive summarization, rewrite/enhancement, and KV-cache optimizations do not provide interchangeable guarantees.

## Goals / Non-Goals

**Goals:**

- Compare candidates using primary sources and live GitHub metadata.
- Measure multiple long prompt classes with an explicit tokenizer and deterministic fixtures.
- Separate measured results from upstream claims and analytical estimates.
- Recommend a safe Headroom policy that can bypass compression for fragile inputs.
- Preserve enough evidence that another operator can reproduce the conclusion.

**Non-Goals:**

- Deploy changes to the live Headroom gateway.
- Claim runtime measurements for repositories that cannot be executed in this environment.
- Treat KV-cache methods as prompt-token reduction when they only reduce compute or memory.
- Send private prompts or credentials to public services.

## Decisions

1. **Use a layered evidence model.** Each claim is labeled as locally measured, NotebookLM-synthesized, upstream-reported, or inferred. This prevents paper benchmarks from being presented as local results.
2. **Use a 50-row by 50-column CSV as the exhaustive matrix.** The report presents a compact decision table and links the machine-readable matrix. GitHub stars and repository metadata are captured through GitHub's API with a UTC timestamp.
3. **Benchmark prompt classes, not one anecdote.** Fixtures cover prose/RAG, code/debugging, and structured instruction/data prompts. Quality is evaluated with required-fact retention, protected-span integrity, and task-answer agreement.
4. **Recommend policy routing, not unconditional rewriting.** Requests are classified into bypass, lossless cleanup, extractive compression, or semantic compression; fail-open behavior preserves the original prompt.
5. **Treat enhancement and compression as competing actions.** Enhancement is allowed only when it improves task clarity within a strict token budget; it is not counted as token saving if it expands context.

## Risks / Trade-offs

- **Compression deletes decisive details** → protected-span extraction, minimum quality threshold, and automatic fallback to the original request.
- **Tokenizer mismatch changes savings** → publish raw text plus counts for the target tokenizer and state the tokenizer version.
- **Model-based judging is biased** → combine deterministic fact/protected-span checks with blinded model judging and disclose the rubric.
- **Repository popularity dominates technical fit** → cap popularity at 5/100 points and weight measured quality, savings, latency, deployability, and integration.
- **Preprocessor latency erases economic savings** → route only above a configurable break-even token threshold and record added latency/cost.
- **Prompt injection targets the preprocessor** → isolate system/developer messages, never let the cheap model rewrite authority-bearing instructions, and validate output structure.

## Migration Plan

1. Add shadow-mode classification and metrics without changing forwarded prompts.
2. Enable deterministic cleanup for oversized requests behind a feature flag.
3. Canary extractive compression for eligible low-risk requests with original-prompt fallback.
4. Add cheap-model semantic compression only after quality and cost SLOs hold.
5. Roll back by disabling the preprocessor flag; the original request path remains unchanged.

## Open Questions

- Which expensive target models and exact provider prices should define the production break-even threshold?
- Does Headroom already expose stable hooks for per-message preprocessing and trace metadata, or is an adapter middleware required?

