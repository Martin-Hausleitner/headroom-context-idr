## ADDED Requirements

### Requirement: Source-grounded repository comparison
The research deliverable SHALL compare 50 relevant public repositories in a 50-column CSV using live GitHub metadata, primary links, an explicit 100-point rubric, emoji-valued categorical cells, and exactly one overall winner marker.

#### Scenario: Matrix integrity is checked
- **WHEN** the comparison artifacts are finalized
- **THEN** an automated check confirms 50 data rows, 50 columns, current star values, valid repository URLs, numeric scores from 0 through 100, and exactly one crown

### Requirement: Reproducible prompt benchmark
The repository SHALL contain long-prompt fixtures, executable benchmark tooling, raw result data, tokenizer identity, latency, before/after token counts, compression percentage, and quality-retention evidence.

#### Scenario: Benchmark is rerun
- **WHEN** an operator executes the documented benchmark command
- **THEN** the result artifact is regenerated from the committed fixtures without fabricated observations

### Requirement: Evidence provenance
Every material conclusion SHALL distinguish locally measured results, upstream-reported results, NotebookLM synthesis, and analytical inference.

#### Scenario: Reader audits a recommendation
- **WHEN** a reader follows the recommendation's citations and evidence labels
- **THEN** the origin and limitations of each decisive claim are apparent

### Requirement: Genuine NotebookLM research
The report SHALL include a real NotebookLM notebook URL, the source count and source categories, the substantive queries used, and a synthesis that is checked against the local evidence.

#### Scenario: Notebook provenance is inspected
- **WHEN** the report header and IDR section are read
- **THEN** they identify `IDR:ja`, link the real notebook, and describe the actual research pass


