# Feature Matrix

| Emoji | Area | Feature | Status | Done % | Stability % | E2E Testing | Screenshot / Proof | Evidence / Files | Next Step |
|---|---|---|---|---:|---:|---|---|---|---|
| 📚 | IDR | Echtes NotebookLM mit 40 Quellen und fünf Cross-Queries | Done | 100% | 95% | Passed | CLI proof only — `nlm source list` und Query-JSON | `research/notebooklm/queries.json`, `research/source-manifest.md` | Notebook bei wesentlichen neuen Quellen aktualisieren |
| 🧭 | Discovery | 50 echte Repositories mit Live-GitHub-Metadaten | Done | 100% | 95% | Passed | Screenshot: `proofs/llmlingua-github.png`, `proofs/claw-compactor-github.png` | `data/candidates.csv`, `research/github-metadata.json` | Stars bei späterer Entscheidung neu erfassen |
| 📊 | Decision | 50×60 Matrix, 100-Punkte-Rubrik, genau eine Krone | Done | 100% | 90% | Passed | Report: `headroom-context-report.md` | `data/repository-matrix.csv` | Produktionsgewichte mit echten Kosten kalibrieren |
| 🧪 | Benchmark | Drei lange Prompts, zehn Methoden, zwei Tokenizer | Done | 100% | 85% | Passed | CLI proof only — reproduzierbarer Benchmark | `benchmarks/fixtures/`, `benchmarks/results/benchmark-results.*` | Mit privaten Produktionsprompts nur nach Datenschutzfreigabe wiederholen |
| 🔒 | Safety | Pflichtfakten, Schutzspannen und Headroom-Adversarial-Grid | Done | 100% | 90% | Passed | CLI proof only — 210 adversariale Zellen | `benchmarks/results/headroom-adversarial.json`, `QUALITY-GATE.md` | Externe Flash-Stufe separat red-teamen |
| 🏗️ | Architecture | Adaptive Rollen-/Content-Policy mit Fail-open und Cache-Schutz | Done | 100% | 85% | N/A | N/A — dokumentationsbasierter Architekturplan | `headroom-context-report.md` | In Headroom-Repo als Shadow-Mode implementieren |
| 🖥️ | Runtime | Live Headroom 0.31.0 inspiziert und im Browser validiert | Done | 100% | 95% | Passed | Screenshot: `proofs/headroom-dashboard.png` | Health, Stats, Metrics und Dashboard-Beweis | Live-Metriken nach Canary erneut erfassen |
| 🚀 | Publication | GitHub-Blob-Link und gerenderte Datei | Planned | 90% | 90% | Planned | Noch kein Screenshot — Veröffentlichung ist letzter Gate-Schritt | Git-Status und Remote nach Commit | Committen, pushen, Blob-URL per HTTP validieren |
