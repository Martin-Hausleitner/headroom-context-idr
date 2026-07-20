# IDR-Finisher Status — 20. Juli 2026

Alle zehn Hauptreports erfüllen den F1-Gate auf ihrem jeweiligen GitHub-Default-Branch: exakter Codex-Kopf, echte NotebookLM-UUID, Tool-/GitHub-/Lizenz-/Star-Matrix, 100-Punkte-Wertung, genau ein Kronen-Sieger und eine konkrete Empfehlung. Der abschließende Remote-Readback erfolgte über die GitHub-Contents-API am commitgebundenen SHA; jede veröffentlichte Fassung ließ sich außerdem über GitHubs GFM-Renderer fehlerfrei in HTML umwandeln.

| Repo | Report-Datei | 👑? | Blob-URL | Status |
|---|---|---:|---|---|
| headroom-context-idr | headroom-context-report.md | Ja, genau 1 | [5926fec](https://github.com/Martin-Hausleitner/headroom-context-idr/blob/5926fec82c87ebdb741af14f6bd0ddf76f3d9ebe/headroom-context-report.md) | ✅ fertig · 26.517 Bytes |
| secrets-idr-report | agentic-secrets-report.md | Ja, genau 1 | [06bda40](https://github.com/Martin-Hausleitner/secrets-idr-report/blob/06bda40450066fdc30dbc623546ebffe37f0d259/agentic-secrets-report.md) | ✅ fertig · 44.257 Bytes |
| web-archive-report | web-archive-report.md | Ja, genau 1 | [85c0b7b](https://github.com/Martin-Hausleitner/web-archive-report/blob/85c0b7b7857cd99b728f61bef07f2af38838a541/web-archive-report.md) | ✅ fertig · 32.449 Bytes |
| subs-value-report | subs-value-report.md | Ja, genau 1 | [1321d82](https://github.com/Martin-Hausleitner/subs-value-report/blob/1321d82396eadea2a8fd8e16cae1b7d81a82b604/subs-value-report.md) | ✅ fertig · 29.925 Bytes |
| recording-shield-report | recording-shield-report.md | Ja, genau 1 | [bda458a](https://github.com/Martin-Hausleitner/recording-shield-report/blob/bda458acf222eaf57b3185def8ecc1f0ccfec3b4/recording-shield-report.md) | ✅ fertig · 11.771 Bytes |
| paperclip-prio-report | paperclip-priority-system.md | Ja, genau 1 | [f24c354](https://github.com/Martin-Hausleitner/paperclip-prio-report/blob/f24c3547b11e7bcb966defeec539ef66a9a1d119/paperclip-priority-system.md) | ✅ fertig · 40.015 Bytes |
| paperclip-pr-match | paperclip-pr-match.md | Ja, genau 1 | [8299aba](https://github.com/Martin-Hausleitner/paperclip-pr-match/blob/8299aba20aedfbe08a2531b58f99d5e3a794150c/paperclip-pr-match.md) | ✅ fertig · 69.625 Bytes |
| homeserver-report | homeserver-report.md | Ja, genau 1 | [6bd5ef8](https://github.com/Martin-Hausleitner/homeserver-report/blob/6bd5ef82ea7c730bea627ba3540b7766ace3272a/homeserver-report.md) | ✅ fertig · 33.393 Bytes |
| paperclip-architecture | paperclip-architecture.md | Ja, genau 1 | [07d3482](https://github.com/Martin-Hausleitner/paperclip-architecture/blob/07d3482c4cab7bfecc1930daf3fe1f3e810e8904/paperclip-architecture.md) | ✅ fertig · 37.676 Bytes |
| unbrowse-market-skills | unbrowse-market-skills.md | Ja, genau 1 | [fc8ae1d](https://github.com/Martin-Hausleitner/unbrowse-market-skills/blob/fc8ae1dd349f7521c07b0c06d0ff27f9faa16f3d/unbrowse-market-skills.md) | ✅ fertig · 11.019 Bytes |

## Remote-Sonderfälle

- recording-shield-report existierte beim Abschluss bereits als privates GitHub-Repository; der lokale Checkout wurde mit diesem Remote verbunden und ohne Force-Push auf dessen aktueller Historie veröffentlicht.
- homeserver-report wurde privat unter Martin-Hausleitner angelegt und der lokale Remote vom Organisationsziel auf dieses persönliche Ziel umgestellt.
- web-archive-report zeigte lokal irrtümlich auf unbrowse-market-skills; der Remote wurde auf das bereits vorhandene private web-archive-report korrigiert.
- Web-Archive, Recording-Shield und Unbrowse wurden wegen divergierender lokaler Alt-Historien über isolierte Worktrees vom jeweiligen aktuellen Remote-HEAD als normale Fast-Forward-Commits veröffentlicht.
- Beim Subscription-Report wurden `main` und der tatsächliche Default-Branch `master` auf denselben F1-Commit fast-forward synchronisiert. Als der vorherige Notebook-Link im finalen Readback `NOT_FOUND` lieferte, wurde ein anderes echtes, fachlich passendes Notebook mit dem Report als 21. Quelle verknüpft und der reparierte Kopf erneut veröffentlicht.

## Verifikationsstandard

1. Jede Notebook-UUID mit `nlm notebook get` gegen das eingeloggte Konto geprüft; alle acht eindeutigen Notebook-Links sind abrufbar.
2. Stars und SPDX-Lizenzstatus am 20.07.2026 zwischen 16:18 und 16:30 CEST live über die GitHub-Repository-API erhoben; fehlende oder uneindeutige Lizenzdaten als [UNVERIFIZIERT] markiert.
3. Exakter Kopf, Matrixfelder, Kriteriengewichte = 100, jede Zeilensumme, Empfehlung, ausgeglichene Markdown-Fences und genau ein Kronen-Symbol automatisiert geprüft.
4. Git-Diff-Whitespace-Gate bestanden.
5. Jede Reportdatei über GitHub Contents API am vollständigen Commit-SHA gelesen.
6. Remote-Blob-SHA gegen die jeweilige lokale Publikationsfassung verglichen; 10/10 bytegleich.
7. Alle 141 im Paperclip-PR-Match verlinkten PRs live aufgelöst: 34 gemergt, 106 offen, 1 ungemergt geschlossen.
8. Alle zehn veröffentlichten Reports über GitHubs GFM-API gerendert; keine fehlenden repo-relativen Links, keine unausgeglichenen Fences und keine Strukturfehler.

## Ausgeführte Tests

- Headroom-spezifisches Quality Gate: **28/28 PASS**.
- Unbrowse: **78/78 Tests PASS** im sauberen Remote-Worktree; Privacy-Gate PASS über 171 Dateien mit 0 Verstößen.
- Paperclip-PR-Match: **141/141** verlinkte PRs per GitHub-API erreichbar und die Zustandsaggregate exakt nachgerechnet.
- Remote-Struktur-/Render-Gate: **10/10 Reports PASS** mit vollständiger F1-Matrix, korrekten Score-Summen, genau einer Krone, Empfehlung und vorhandenen repo-relativen Linkzielen.

## Bewusst unangetasteter Restbefund

- Der globale Privacy-Scan des Web-Archive-Arbeitsverzeichnisses erkennt in einer bereits vorhandenen, ungetrackten `.omo/run-continuation/...json`-Runtime-Datei die Klasse `credential_assignment`. Der Report-Commit selbst ist sauber; der Runtime-Wert wurde weder ausgegeben noch gestaged oder verändert.
