## ADDED Requirements

### Requirement: Safe preprocessing policy
The plan SHALL route each request to bypass, deterministic cleanup, extractive compression, or semantic compression based on size, content type, risk, and expected break-even value.

#### Scenario: Fragile request is received
- **WHEN** a request contains code, exact quotations, tool schemas, structured output constraints, or protected authority-bearing instructions
- **THEN** the policy bypasses lossy rewriting or applies only protected-span-aware cleanup

### Requirement: Fail-open request path
The design SHALL forward the original, byte-equivalent message payload whenever preprocessing fails, times out, produces invalid structure, or misses its quality gate.

#### Scenario: Compressor times out
- **WHEN** the preprocessing timeout expires
- **THEN** Headroom forwards the original request and records the bypass reason without failing the user request

### Requirement: Observable economic gate
The design SHALL record original tokens, forwarded tokens, preprocessor tokens, added latency, estimated cost saved, policy decision, and fallback reason using privacy-safe metadata.

#### Scenario: Break-even is not met
- **WHEN** expected downstream savings do not exceed preprocessor cost and latency budget
- **THEN** the request bypasses semantic preprocessing

### Requirement: Staged rollout and rollback
The plan SHALL define shadow, canary, guarded general-availability, and immediate rollback stages with measurable acceptance thresholds.

#### Scenario: Quality degrades during canary
- **WHEN** quality retention or protected-span integrity falls below the defined threshold
- **THEN** the canary automatically disables lossy preprocessing and continues with original prompts

