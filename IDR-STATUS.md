# IDR-Finisher Status — 20. Juli 2026

Alle zehn Hauptreports erfüllen den lokalen F1-Gate: exakter Codex-Kopf, echte NotebookLM-UUID, Tool-/GitHub-/Lizenz-/Star-Matrix, 100-Punkte-Wertung, genau ein Kronen-Sieger und eine konkrete Empfehlung. Der Remote-Readback erfolgte über die GitHub-Contents-API am commitgebundenen SHA; die Remote-Blob-Hashes stimmen mit den lokalen Reportdateien überein.

| Repo | Report-Datei | 👑? | Blob-URL | Status |
|---|---|---:|---|---|
| headroom-context-idr | headroom-context-report.md | Ja, genau 1 | [9d4545b](https://github.com/Martin-Hausleitner/headroom-context-idr/blob/9d4545b50e5bc5a555d40e40c700ce906c0013b9/headroom-context-report.md) | ✅ fertig · 26.245 Bytes |
| secrets-idr-report | agentic-secrets-report.md | Ja, genau 1 | [2565ed8](https://github.com/Martin-Hausleitner/secrets-idr-report/blob/2565ed836652137dc78ff29a7fb7182266b0a05c/agentic-secrets-report.md) | ✅ fertig · 44.004 Bytes |
| web-archive-report | web-archive-report.md | Ja, genau 1 | [44c5c7a](https://github.com/Martin-Hausleitner/web-archive-report/blob/44c5c7a8782174d51bbdbefd6d223f891094bef0/web-archive-report.md) | ✅ fertig · 30.241 Bytes |
| subs-value-report | subs-value-report.md | Ja, genau 1 | [7765803](https://github.com/Martin-Hausleitner/subs-value-report/blob/77658032dc220b36e8de5040a858cdd67e513024/subs-value-report.md) | ✅ fertig · 30.095 Bytes |
| recording-shield-report | recording-shield-report.md | Ja, genau 1 | [6806a60](https://github.com/Martin-Hausleitner/recording-shield-report/blob/6806a60d70dbdaa84e44b12a42a18d9f0b04bccc/recording-shield-report.md) | ✅ fertig · 8.484 Bytes |
| paperclip-prio-report | paperclip-priority-system.md | Ja, genau 1 | [6c513c3](https://github.com/Martin-Hausleitner/paperclip-prio-report/blob/6c513c3a955d8e080049386b7891d0944046021a/paperclip-priority-system.md) | ✅ fertig · 39.377 Bytes |
| paperclip-pr-match | paperclip-pr-match.md | Ja, genau 1 | [3473b32](https://github.com/Martin-Hausleitner/paperclip-pr-match/blob/3473b32889631dfe84f6469376dcc105a017146d/paperclip-pr-match.md) | ✅ fertig · 62.903 Bytes |
| homeserver-report | homeserver-report.md | Ja, genau 1 | [c18a60d](https://github.com/Martin-Hausleitner/homeserver-report/blob/c18a60d8343fc97babc5342a49a0bad380c16e59/homeserver-report.md) | ✅ fertig · 33.337 Bytes |
| paperclip-architecture | paperclip-architecture.md | Ja, genau 1 | [4b26d63](https://github.com/Martin-Hausleitner/paperclip-architecture/blob/4b26d637d2d0846808411e765d21b3bd5077555d/paperclip-architecture.md) | ✅ fertig · 31.496 Bytes |
| unbrowse-market-skills | unbrowse-market-skills.md | Ja, genau 1 | [f3c1f02](https://github.com/Martin-Hausleitner/unbrowse-market-skills/blob/f3c1f021fc8cdbc1aa8750d2700f9d487abee347/unbrowse-market-skills.md) | ✅ fertig · 10.963 Bytes |

## Remote-Sonderfälle

- recording-shield-report existierte beim Abschluss bereits als privates GitHub-Repository; der lokale Checkout wurde mit diesem Remote verbunden und ohne Force-Push auf dessen aktueller Historie veröffentlicht.
- homeserver-report wurde privat unter Martin-Hausleitner angelegt und der lokale Remote vom Organisationsziel auf dieses persönliche Ziel umgestellt.
- web-archive-report zeigte lokal irrtümlich auf unbrowse-market-skills; der Remote wurde auf das bereits vorhandene private web-archive-report korrigiert.
- Web-Archive, Recording-Shield und Unbrowse wurden wegen divergierender lokaler Alt-Historien über isolierte Worktrees vom jeweiligen aktuellen Remote-HEAD als normale Fast-Forward-Commits veröffentlicht.
- Beim Subscription-Report wurden `main` und der tatsächliche Default-Branch `master` auf denselben F1-Commit fast-forward synchronisiert.

## Verifikationsstandard

1. Notebook-UUID gegen die eingeloggte Ausgabe von nlm list notebooks geprüft.
2. Stars und SPDX-Lizenzstatus am 20.07.2026 um 12:33 CEST live über die GitHub-Repository-API erhoben; NOASSERTION als [UNVERIFIZIERT] markiert.
3. Exakter Kopf, Matrixfelder, 100-Punkte-Signal, Empfehlung, Mindestumfang, ausgeglichene Markdown-Fences und genau ein Kronen-Symbol automatisiert geprüft.
4. Git-Diff-Whitespace-Gate bestanden.
5. Jede Reportdatei über GitHub Contents API am vollständigen Commit-SHA gelesen.
6. Remote-Blob-SHA gegen git hash-object der lokalen Datei verglichen.

## Ausgeführte Tests

- Headroom-spezifisches Quality Gate: **28/28 PASS**; Kopfprüfung auf das verbindliche F1-Format aktualisiert und Kronenprüfung auf exakt ein Symbol verschärft.
- Web-Archive: **78/78 Tests PASS**, anschließend Privacy-Gate PASS mit 0 Verstößen.
- Unbrowse: **79/79 Tests PASS**, anschließend Privacy-Gate PASS mit 0 Verstößen.
