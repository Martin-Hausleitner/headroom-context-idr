# Headroom Context IDR

[Vollständiger IDR-Report](headroom-context-report.md) · [Feature Matrix](docs/FEATURE_MATRIX.md) · [50×60 Repo-Matrix](data/repository-matrix.csv) · [Quality Gate](QUALITY-GATE.md)

Reproduzierbare Untersuchung einer billigen Prompt-Enhance-/Compression-Stufe vor Headroom 0.31.0.

## Kernergebnis

- 👑 Externer deterministischer Baustein: `open-compress/claw-compactor` mit 79,5/100, nur hinter harten Rollen- und Qualitäts-Gates.
- Semantische Zwischen-KI: agy Gemini 3.5 Flash Low nur für sehr lange, redundante Prosa/RAG-Payloads.
- Kein generativer Rewrite für jede Prompt; jede Request wird lediglich billig klassifiziert.
- KV-Cache-Methoden sparen bei gehosteten Zielmodellen keine übertragenen Input-Tokens.

## Reproduktion

```bash
python3 scripts/fetch_github_metadata.py
python3 scripts/run_notebooklm_queries.py
python3 scripts/benchmark.py
python3 scripts/append_claw_results.py
headroom evals adversarial --json-output benchmarks/results/headroom-adversarial.json
```

Der Benchmark benötigt Headroom 0.31.0 im Host-Python, `llmlingua==0.2.2` in `.venv`, das Modell `microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank`, einen gepinnten Claw-Clone und einen eingeloggten `agy`-Client mit `Gemini 3.5 Flash (Low)`.

## Wichtige Artefakte

- `benchmarks/fixtures/`: drei lange Eingabeprompts
- `benchmarks/results/benchmark-results.csv`: 30 Messzeilen
- `benchmarks/results/benchmark-results.json`: Messwerte plus tatsächliche Ausgaben
- `research/notebooklm/queries.json`: fünf echte NotebookLM-Cross-Queries
- `research/github-metadata.json`: GitHub-API-Snapshot
- `proofs/`: Browser-Screenshots der Live-/Primärquellenflächen
