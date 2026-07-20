# Quality Gate

**Verdikt: PASS — 33/33 Checks bestanden.**

| Check | Ergebnis | Evidenz |
|---|:---:|---|
| Reportkopf IDR: ja | PASS | headroom-context-report.md |
| NotebookLM-Link im Kopf | PASS | https://notebooklm.google.com/notebook/4cbe42bf-f9ec-4c8b-8b6c-e6501f50478b |
| Mermaid-Architektur | PASS | Zielarchitektur |
| 100-Punkte-Rubrik | PASS | Rubriktabelle |
| Krone im Report | PASS | genau eine empfohlene Repo-Krone |
| Report mindestens 25 KiB | PASS | 26566 Bytes |
| 50 Repository-Zeilen | PASS | 50 |
| Mindestens 50 Matrixfelder | PASS | 60 |
| GitHub, Website, Lizenz, Stars und Score je Matrixzeile | PASS | github_url, homepage, license, repository, stars, total_100 |
| Report und CSV gegenseitig verlinkt | PASS | Report → CSV → gerenderter Report |
| Genau eine Matrix-Krone | PASS | open-compress/claw-compactor |
| Matrix nach TOTAL-SCORE sortiert | PASS | top=open-compress/claw-compactor (79.5) |
| Alle Scores summieren korrekt | PASS | 50/50 |
| Alle Scores in 0..100 | PASS | total_100 |
| GitHub-Metadaten-Snapshot höchstens 24 Stunden alt | PASS | 2026-07-20T15:18:47.402949+00:00 |
| Drei lange Promptklassen | PASS | code_debug, prose_rag, structured_json |
| Zehn gemessene Methoden | PASS | 10 |
| 30 Benchmark-Messzeilen | PASS | 30 |
| Zwei Tokenizer | PASS | cl100k_base, o200k_base |
| Token-Savings arithmetisch korrekt | PASS | 30/30 |
| LLMLingua real ausgeführt | PASS | microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank |
| Claw gepinnt und ausgeführt | PASS | c1b936d40b1145c7a257bd6e34a17994f467495f |
| Flash compaction real ausgeführt | PASS | Gemini 3.5 Flash Low |
| Fünf NotebookLM-Cross-Queries | PASS | 5 |
| Alle NotebookLM-Antworten nichtleer | PASS | queries.json |
| 40 Quellen im Manifest | PASS | 40 |
| Vier echte Browser-Screenshots inkl. GitHub-Render | PASS | headroom-dashboard.png, claw-compactor-github.png, llmlingua-github.png, github-report-rendered.png |
| Alle lokalen Reportlinks vorhanden | PASS | 9 |
| Externe Reportlinks erreichbar | PASS | 36 |
| GitHub-Remote ist der öffentliche Ziel-Repo | PASS | https://github.com/Martin-Hausleitner/headroom-context-idr.git |
| Gerenderter GitHub-Blob öffentlich erreichbar | PASS | https://github.com/Martin-Hausleitner/headroom-context-idr/blob/main/headroom-context-report.md (200) |
| Live Headroom gesund | PASS | {"status": "healthy", "ready": true, "version": "0.31.0"} |
| NotebookLM hat 40 verarbeitete Quellen | PASS | count=40 |

## Scope

Dieses Gate prüft Briefing-Vollständigkeit, Matrix- und Benchmark-Invarianten, NotebookLM-Provenienz, Link-/Screenshot-Beweise, die öffentliche GitHub-Publikation und den Live-Health-Status. Es ersetzt keine Produktions-Canary mit privaten realen Prompts.
