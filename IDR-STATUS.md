# IDR-Finisher Status — 20. Juli 2026

Alle zehn Hauptreports erfüllen den lokalen F1-Gate: exakter Codex-Kopf, echte NotebookLM-UUID, Tool-/GitHub-/Lizenz-/Star-Matrix, 100-Punkte-Wertung, genau ein Kronen-Sieger und eine konkrete Empfehlung. Der Remote-Readback erfolgte über die GitHub-Contents-API am commitgebundenen SHA; die Remote-Blob-Hashes stimmen mit den lokalen Reportdateien überein.

| Repo | Report-Datei | 👑? | Blob-URL | Status |
|---|---|---:|---|---|
| headroom-context-idr | headroom-context-report.md | Ja, genau 1 | [275e6fd](https://github.com/Martin-Hausleitner/headroom-context-idr/blob/275e6fd1bbfeb1599fa255845b6a28a39ce68163/headroom-context-report.md) | ✅ fertig · 26.517 Bytes |
| secrets-idr-report | agentic-secrets-report.md | Ja, genau 1 | [4da069c](https://github.com/Martin-Hausleitner/secrets-idr-report/blob/4da069ce7541142af173b148cda7d27fe1d0703d/agentic-secrets-report.md) | ✅ fertig · 44.004 Bytes |
| web-archive-report | web-archive-report.md | Ja, genau 1 | [0867aeb](https://github.com/Martin-Hausleitner/web-archive-report/blob/0867aeb034b095d585542413a6246d8cc4b59259/web-archive-report.md) | ✅ fertig · 32.262 Bytes |
| subs-value-report | subs-value-report.md | Ja, genau 1 | [c8174b6](https://github.com/Martin-Hausleitner/subs-value-report/blob/c8174b65a476a740dfdd0c6484b538a472144abb/subs-value-report.md) | ✅ fertig · 30.371 Bytes |
| recording-shield-report | recording-shield-report.md | Ja, genau 1 | [e12df8a](https://github.com/Martin-Hausleitner/recording-shield-report/blob/e12df8a472a4c38b48093419a93d6e4e73029ac7/recording-shield-report.md) | ✅ fertig · 11.013 Bytes |
| paperclip-prio-report | paperclip-priority-system.md | Ja, genau 1 | [aea9b08](https://github.com/Martin-Hausleitner/paperclip-prio-report/blob/aea9b08ca75aa0b72c807358925f32b938f4131b/paperclip-priority-system.md) | ✅ fertig · 39.377 Bytes |
| paperclip-pr-match | paperclip-pr-match.md | Ja, genau 1 | [dc53e90](https://github.com/Martin-Hausleitner/paperclip-pr-match/blob/dc53e90c73e252fee8b4d29e91573d123f1840bf/paperclip-pr-match.md) | ✅ fertig · 63.667 Bytes |
| homeserver-report | homeserver-report.md | Ja, genau 1 | [abe1d52](https://github.com/Martin-Hausleitner/homeserver-report/blob/abe1d52559915765f80f35a9e6b4e2f7a07c5b74/homeserver-report.md) | ✅ fertig · 33.379 Bytes |
| paperclip-architecture | paperclip-architecture.md | Ja, genau 1 | [b8ef2a6](https://github.com/Martin-Hausleitner/paperclip-architecture/blob/b8ef2a69d2446b251438cdaaff180df3e0583c67/paperclip-architecture.md) | ✅ fertig · 31.496 Bytes |
| unbrowse-market-skills | unbrowse-market-skills.md | Ja, genau 1 | [3e46f84](https://github.com/Martin-Hausleitner/unbrowse-market-skills/blob/3e46f84a8acfd3d455d1395d9e56f9e22d7f3106/unbrowse-market-skills.md) | ✅ fertig · 10.963 Bytes |

## Remote-Sonderfälle

- recording-shield-report existierte beim Abschluss bereits als privates GitHub-Repository; der lokale Checkout wurde mit diesem Remote verbunden und ohne Force-Push auf dessen aktueller Historie veröffentlicht.
- homeserver-report wurde privat unter Martin-Hausleitner angelegt und der lokale Remote vom Organisationsziel auf dieses persönliche Ziel umgestellt.
- web-archive-report zeigte lokal irrtümlich auf unbrowse-market-skills; der Remote wurde auf das bereits vorhandene private web-archive-report korrigiert.
- Web-Archive, Recording-Shield und Unbrowse wurden wegen divergierender lokaler Alt-Historien über isolierte Worktrees vom jeweiligen aktuellen Remote-HEAD als normale Fast-Forward-Commits veröffentlicht.
- Beim Subscription-Report wurden `main` und der tatsächliche Default-Branch `master` auf denselben F1-Commit fast-forward synchronisiert.

## Verifikationsstandard

1. Notebook-UUID gegen die eingeloggte Ausgabe von nlm list notebooks geprüft.
2. Stars und SPDX-Lizenzstatus am 20.07.2026 um 13:10 CEST live über die GitHub-Repository-API erhoben; NOASSERTION als [UNVERIFIZIERT] markiert.
3. Exakter Kopf, Matrixfelder, 100-Punkte-Signal, Empfehlung, Mindestumfang, ausgeglichene Markdown-Fences und genau ein Kronen-Symbol automatisiert geprüft.
4. Git-Diff-Whitespace-Gate bestanden.
5. Jede Reportdatei über GitHub Contents API am vollständigen Commit-SHA gelesen.
6. Remote-Blob-SHA gegen `git hash-object` der lokalen Datei verglichen; 10/10 bytegleich.
7. Alle 129 im Paperclip-PR-Match verlinkten PRs live aufgelöst: 31 gemergt, 97 offen, 1 ungemergt geschlossen; PR #1172 entsprechend korrigiert.
8. Sämtliche Mermaid-Blöcke mit lokalem Chromium gerendert; 10/10 Reports ohne Syntaxfehler.

## Ausgeführte Tests

- Headroom-spezifisches Quality Gate: **28/28 PASS**.
- Web-Archive: **78/78 Tests PASS** im vollständigen lokalen Projekt; Report-only Privacy-Gate im sauberen Publikations-Worktree PASS mit 0 Verstößen.
- Unbrowse: Test-Suite PASS im sauberen Remote-Worktree, anschließend Privacy-Gate PASS mit 0 Verstößen.
- Struktur-Gate: 10/10 Reports mit exaktem Kopf, echtem Notebook, mindestens einer vollständigen Matrix, korrekten Score-Summen, genau einer Krone, Empfehlung, ausgeglichenen Fences und vorhandenen lokalen Linkzielen.
