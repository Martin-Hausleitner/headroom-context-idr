# IDR-Finisher Status — 20. Juli 2026

Alle zehn Hauptreports erfüllen den lokalen F1-Gate: exakter Codex-Kopf, echte NotebookLM-UUID, Tool-/GitHub-/Lizenz-/Star-Matrix, 100-Punkte-Wertung, genau ein Kronen-Sieger und eine konkrete Empfehlung. Der Remote-Readback erfolgte über die GitHub-Contents-API am commitgebundenen SHA; die Remote-Blob-Hashes stimmen mit den lokalen Reportdateien überein.

| Repo | Report-Datei | 👑? | Blob-URL | Status |
|---|---|---:|---|---|
| headroom-context-idr | headroom-context-report.md | Ja, genau 1 | [09618b0](https://github.com/Martin-Hausleitner/headroom-context-idr/blob/09618b0bb64224ab877307a61d7603ab4bb1c1ac/headroom-context-report.md) | ✅ fertig · 26.231 Bytes |
| secrets-idr-report | agentic-secrets-report.md | Ja, genau 1 | [93c1315](https://github.com/Martin-Hausleitner/secrets-idr-report/blob/93c131577bf9231350f644297a21a1612604c055/agentic-secrets-report.md) | ✅ fertig · 43.992 Bytes |
| web-archive-report | web-archive-report.md | Ja, genau 1 | [488e356](https://github.com/Martin-Hausleitner/web-archive-report/blob/488e35603a63d80a19755e55258940e10d2e5b9c/web-archive-report.md) | ✅ fertig · 30.265 Bytes |
| subs-value-report | subs-value-report.md | Ja, genau 1 | [5dc66a9](https://github.com/Martin-Hausleitner/subs-value-report/blob/5dc66a97c5d09cc2785d0a86d788f8e41c9cec01/subs-value-report.md) | ✅ fertig · 30.081 Bytes |
| recording-shield-report | recording-shield-report.md | Ja, genau 1 | [d83803b](https://github.com/Martin-Hausleitner/recording-shield-report/blob/d83803b7528360af82a514bc6a322766087e5ca2/recording-shield-report.md) | ✅ fertig · 8.337 Bytes |
| paperclip-prio-report | paperclip-priority-system.md | Ja, genau 1 | [aba899f](https://github.com/Martin-Hausleitner/paperclip-prio-report/blob/aba899f101a8f7eca97ccd35653374d8a30e563a/paperclip-priority-system.md) | ✅ fertig · 39.363 Bytes |
| paperclip-pr-match | paperclip-pr-match.md | Ja, genau 1 | [5f7dd90](https://github.com/Martin-Hausleitner/paperclip-pr-match/blob/5f7dd9073d7109417670f45e52119d5e228ae94d/paperclip-pr-match.md) | ✅ fertig · 62.889 Bytes |
| homeserver-report | homeserver-report.md | Ja, genau 1 | [ff5b1a8](https://github.com/Martin-Hausleitner/homeserver-report/blob/ff5b1a8245d2e7bffe9491171ff5ebf87dfc7cfc/homeserver-report.md) | ✅ fertig · 33.311 Bytes |
| paperclip-architecture | paperclip-architecture.md | Ja, genau 1 | [a1af2ba](https://github.com/Martin-Hausleitner/paperclip-architecture/blob/a1af2bada02546c888e64f56dfb4b3e21a9a34e5/paperclip-architecture.md) | ✅ fertig · 31.482 Bytes |
| unbrowse-market-skills | unbrowse-market-skills.md | Ja, genau 1 | [1fb7bdb](https://github.com/Martin-Hausleitner/unbrowse-market-skills/blob/1fb7bdb990baaf767f2808f90c09195938e771d7/unbrowse-market-skills.md) | ✅ fertig · 10.949 Bytes |

## Remote-Sonderfälle

- recording-shield-report existierte beim Abschluss bereits als privates GitHub-Repository; der lokale Checkout wurde mit diesem Remote verbunden und ohne Force-Push auf dessen aktueller Historie veröffentlicht.
- homeserver-report wurde privat unter Martin-Hausleitner angelegt und der lokale Remote vom Organisationsziel auf dieses persönliche Ziel umgestellt.
- web-archive-report zeigte lokal irrtümlich auf unbrowse-market-skills; der Remote wurde auf das bereits vorhandene private web-archive-report korrigiert.
- Web-Archive, Recording-Shield und Unbrowse wurden wegen divergierender lokaler Alt-Historien über isolierte Worktrees vom jeweiligen aktuellen Remote-HEAD als normale Fast-Forward-Commits veröffentlicht.

## Verifikationsstandard

1. Notebook-UUID gegen die eingeloggte Ausgabe von nlm list notebooks geprüft.
2. Stars und SPDX-Lizenzstatus live über die GitHub-Repository-API erhoben; NOASSERTION als [UNVERIFIZIERT] markiert.
3. Exakter Kopf, Matrixfelder, 100-Punkte-Signal, Empfehlung, Mindestumfang, ausgeglichene Markdown-Fences und genau ein Kronen-Symbol automatisiert geprüft.
4. Git-Diff-Whitespace-Gate bestanden.
5. Jede Reportdatei über GitHub Contents API am vollständigen Commit-SHA gelesen.
6. Remote-Blob-SHA gegen git hash-object der lokalen Datei verglichen.
