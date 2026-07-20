[ L50 · R350 ] 🟣 Codex · gpt-5.6-sol · 🧠 IDR: ja · 🕐 2026-07-20 12:00 CEST
> 🧠 NotebookLM: https://notebooklm.google.com/notebook/4cbe42bf-f9ec-4c8b-8b6c-e6501f50478b

# IDR: Headroom Prompt-Enhance/Compact

**Notebook:** 40 verarbeitete Primär-/Kuratorquellen, 5 gespeicherte Cross-Queries  
**Stand:** 2026-07-18, Europe/Berlin  
**Zielsystem:** Headroom 0.31.0 auf `127.0.0.1:8787`  
**Rohmatrix:** [50 Repositories × 60 Felder](data/repository-matrix.csv)  
**Messdaten:** [CSV](benchmarks/results/benchmark-results.csv) · [JSON mit Ausgaben](benchmarks/results/benchmark-results.json)  
**Quality Gate:** [QUALITY-GATE.md](QUALITY-GATE.md)

## Ergebnis in einem Satz

## F1-Abschlussmatrix: Toolauswahl und 100-Punkte-Wertung

Gewichtung: Integration in Headroom 25, lokale/deterministische Ausführung 20, Kompressionsnutzen 20, Beobachtbarkeit und Reversibilität 20, Wartung/Reife 15 = **100 Punkte**. Stars und SPDX-Lizenzstatus wurden am 20.07.2026 um 12:33 CEST über die GitHub-Repository-API erhoben; NOASSERTION ist keine verifizierte Lizenz.

| Rang | Tool (GitHub) | Lizenz | ⭐ echte Stars | Integration /25 | Lokal /20 | Nutzen /20 | Observability /20 | Reife /15 | Gesamt /100 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 👑 [Headroom](https://github.com/headroomlabs-ai/headroom) | Apache-2.0 | 60.542 | 25 | 18 | 18 | 20 | 13 | **94** |
| 2 | [LLMLingua](https://github.com/microsoft/LLMLingua) | MIT | 6.452 | 18 | 17 | 20 | 15 | 14 | **84** |
| 3 | [Claw Compactor](https://github.com/open-compress/claw-compactor) | MIT | 2.188 | 22 | 20 | 17 | 12 | 12 | **83** |
| 4 | [RTK](https://github.com/rtk-ai/rtk) | Apache-2.0 | 71.975 | 16 | 20 | 15 | 16 | 15 | **82** |
| 5 | [Selective Context](https://github.com/liyucheng09/Selective_Context) | [UNVERIFIZIERT] (NOASSERTION) | 423 | 13 | 17 | 15 | 10 | 8 | **63** |

**Empfehlung:** Headroom bleibt der kanonische Policy-, Proxy- und Mess-Layer. Claw Compactor wird nur als deterministischer, rollensensitiver Kompressionsbaustein eingebunden; LLMLingua bleibt ein selektiver Pfad für lange Prosa/RAG-Kontexte. Die Krone bewertet die Gesamtplattform, nicht den isolierten Kompressionsalgorithmus.

Nicht jede Prompt sollte von einer billigen KI umgeschrieben werden: Jede Request soll durch eine billige **Policy-Entscheidung** laufen, aber System-/Developer-Nachrichten, Tool-Schemas, Code und strukturiertes JSON bleiben standardmäßig unangetastet; für die deterministische Stufe gewinnt **[Claw Compactor](https://github.com/open-compress/claw-compactor)** mit 79,5/100, und für seltene, sehr lange, redundante Prosa/RAG-Prompts ist **agy Gemini 3.5 Flash Low** die beste gemessene semantische Zwischen-KI.

## Klare Empfehlung

1. **Headrooms bestehende Router-/CCR-Schicht behalten.** Der laufende Dienst hat bereits SmartCrusher, Code-, Log-, Search-, Tabular- und Text-Kompressoren, CCR-Retrieval, Queue-Grenzen und Prometheus-Metriken.
2. **Claw Compactor als externen deterministischen Kandidaten integrieren, aber nur blockweise.** System/Developer und Tool-Schemas müssen vor Claw hart eingefroren werden. `Abbrev`/`Nexus` dürfen nur auf unstrukturierter Prosa laufen. Für JSON wird nur ein strukturwahrender Pfad mit Pflichtwert-Guard aktiviert.
3. **Gemini 3.5 Flash Low nur hinter einem Break-even- und Qualitäts-Gate.** Im lokalen Test sparte der Modus „compaction“ 97,5–98,9 % bei vollständigem Recall der definierten Pflichtfakten, benötigte aber 5,0–7,7 s. Das ist für große RAG-Kontexte interessant, nicht für jede Request.
4. **Enhancement ist kein Sparmodus.** Flash-Enhancement vergrößerte die Testprompts im Mittel um 1,33 % und brauchte im Mittel 28,5 s. Enhancement gehört in einen expliziten Qualitätsmodus oder offline in Prompt-Optimierung, nie in die Savings-Bilanz.
5. **LLMLingua-2 nur Shadow/Canary.** Die Paperlage ist stark, aber der echte CPU-Lauf auf dieser Maschine brauchte 28–51 s je Prompt, erhielt im Mittel nur 18,7 % der deterministisch geprüften Qualität und veränderte Autoritätstext. Keine unbedingte Live-Stufe.
6. **KV-Cache-Tricks getrennt halten.** vLLM, LMCache, H2O, SnapKV, KVQuant, KIVI, PyramidKV/KVCache-Factory und FlashAttention sparen bei einem gehosteten teuren Zielmodell keine übertragenen oder abgerechneten Input-Tokens. Sie sind nur relevant, wenn Headroom den Ziel-Inference-Server selbst kontrolliert.

## Warum „jede Prompt enhancen oder compacten“ falsch ist

Die harte Formulierung erzeugt vier Produktionsrisiken:

- Ein Rewrite kann die Hierarchie von System, Developer, User und Tool-Nachrichten verändern.
- Stochastische Rewrites zerstören byte-identische Provider-Prefixe und damit Prompt-Cache-Hits.
- Enhancement fügt häufig Beispiele, Rollen, Begründungen und Formatregeln hinzu und erhöht die Tokens.
- Die Zwischen-KI addiert Kosten und Latenz, selbst wenn der teure Zielaufruf dadurch kaum billiger wird.

Die sichere Interpretation lautet deshalb: **Jede Request wird klassifiziert; nur geeignete Inhalte werden transformiert.** Fail-open bedeutet immer: Bei Timeout, Modellfehler, Qualitätsverlust oder nicht positivem Break-even wird die originale Request weitergeleitet.

## Evidenzklassen

| Kennzeichnung | Bedeutung |
|---|---|
| **lokal gemessen** | In dieser Arbeitsumgebung frisch ausgeführt, Tokenzahl und Laufzeit gespeichert |
| **live beobachtet** | Laufender Headroom-Dienst/API/Dashboard auf `127.0.0.1:8787` |
| **NotebookLM-synthetisiert** | Antwort aus 40 verarbeiteten Quellen; Query und Antwort gespeichert |
| **upstream berichtet** | README/Paper-Behauptung des Projekts, nicht als lokale Messung ausgegeben |
| **analytisch** | Architekturschluss, etwa 0 % API-Input-Saving durch KV-only-Techniken |

Die fünf NotebookLM-Antworten und ihre Fragen liegen unverändert in [`research/notebooklm/queries.json`](research/notebooklm/queries.json). Context7 wurde verpflichtend aufgerufen, war aber wegen ausgeschöpfter Monatsquote nicht nutzbar; deshalb wurden offizielle Repositories, ACL Anthology, arXiv und aktuelle GitHub-API-Daten verwendet.

## Live-Baseline: Was Headroom heute schon kann

Der Health-Check meldete `status=healthy`, `ready=true`, Version 0.31.0. Die aktive Konfiguration komprimiert User-Nachrichten, schützt die letzten zwei Nachrichten, schützt Analysekontext, nutzt SmartCrusher mit Compaction und hat `force_kompress=false`.

Das im Browser validierte Dashboard zeigte zum Messzeitpunkt:

| Live-Metrik | Wert |
|---|---:|
| Proxy-Tokens vor Kompression | 1.419,3 M |
| Proxy-Tokens nach Kompression | 1.366,0 M |
| Proxy-Tokens gespart | 53,3 M |
| Proxy-Savings | 3,8 % |
| RTK-Savings separat | 15.489,8 M |
| Cache Reads | 1.070,7 M Tokens |
| beobachtete Cache Busts | 337 |
| Session-Fehler | 0 |

![Live Headroom Dashboard](proofs/headroom-dashboard.png)

Der Ist-Stand widerlegt die Annahme „Headroom leitet alles unkomprimiert weiter“. Die neue Stufe muss vorhandene Kompression ergänzen, nicht duplizieren. Besonders wichtig ist die Dashboard-Sektion „Compression vs Cache“: eingesparte Prompt-Tokens können durch Cache-Busts teilweise wieder verloren gehen.

## Kandidatenentdeckung

Die Recherche begann mit kuratierten Listen für Context Compression, Agent Context Compression, LLM Compression, Prompt Engineering und LLM Inference. Daraus und aus GitHub Search wurden 50 echte Repositories kuratiert. Stars, Forks, Issues, Lizenz, Sprache und Push-Zeitpunkt wurden am 2026-07-18 per GitHub API erfasst.

Verwendete Awesome-Quellen:

- [Awesome Context Compression LLMs](https://github.com/broalantaps/Awesome-Context-Compression-LLMs)
- [Awesome Agent Context Compression](https://github.com/YerbaPage/Awesome-Agent-Context-Compression)
- [Awesome LLM Compression](https://github.com/HuangOwen/Awesome-LLM-Compression)
- [Awesome Prompt Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering)
- [Awesome LLM Inference](https://github.com/xlite-dev/Awesome-LLM-Inference)

### Top 15 der post-Benchmark-Matrix

| Rang | Repository | Stars | Punkte | Einordnung |
|---:|---|---:|---:|---|
| 1 | [open-compress/claw-compactor](https://github.com/open-compress/claw-compactor) | 2.188 | 79,5 | externer deterministischer Sieger; Guard nötig |
| 2 | [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | 71.648 | 77,0 | sehr stark für CLI-Ausgaben, kein allgemeiner Prompt-Rewriter |
| 3 | [run-llama/llama_index](https://github.com/run-llama/llama_index) | 50.925 | 76,0 | RAG-Postprocessing und LongLLMLingua-Adapter |
| 4 | [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | 25.933 | 75,5 | produktionsreife RAG-Pipeline |
| 5 | [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 142.043 | 75,0 | ContextualCompressionRetriever |
| 6 | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) | 18.552 | 74,5 | Gateway mit gestapelter Kompression |
| 7 | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 90.459 | 71,0 | aggressive Sprachverkürzung, Präzisionsrisiko |
| 8 | [wilpel/caveman-compression](https://github.com/wilpel/caveman-compression) | 1.057 | 70,5 | modellfreie semantische Kurzschrift |
| 9 | [FlagOpen/FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) | 11.950 | 70,5 | starke Retrieval-/Reranking-Bausteine |
| 10 | [AnswerDotAI/rerankers](https://github.com/AnswerDotAI/rerankers) | 1.624 | 69,5 | einfache extraktive Kontextselektion |
| 11 | [huggingface/sentence-transformers](https://github.com/huggingface/sentence-transformers) | 18.917 | 69,5 | Embedding-Baustein, benötigt eigene Policy |
| 12 | [microsoft/promptflow](https://github.com/microsoft/promptflow) | 11.184 | 68,5 | Workflow und LLMLingua-Integration |
| 13 | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | 120.797 | 68,0 | lokaler Billigmodell-Host, kein Compressor |
| 14 | [liyucheng09/Selective_Context](https://github.com/liyucheng09/Selective_Context) | 423 | 65,5 | self-information pruning |
| 15 | [carriex/recomp](https://github.com/carriex/recomp) | 148 | 65,5 | RAG-extraktiv/abstraktiv, selektive Augmentation |

Stars sind ein eingefrorener Snapshot und können sich nach dem Erfassungszeitpunkt ändern. Popularität ist absichtlich nur 5/100 Punkte wert.

## 100-Punkte-Rubrik

| Dimension | Gewicht | Leitfrage |
|---|---:|---|
| echte Input-Token-Savings | 20 | Verkürzt die Methode die übertragene Text-Payload? |
| Qualität/Fidelity | 20 | Bleiben Pflichtfakten, Aufgabenabsicht und Struktur erhalten? |
| Hot-Path-Latenz | 10 | Ist die Laufzeit gegenüber dem Zielmodell wirtschaftlich? |
| lokale/billige Ausführung | 10 | Läuft sie lokal oder auf einer nachweislich billigen Modellklasse? |
| Modell-Footprint | 8 | Ist CPU/kleiner Speicher realistisch? |
| Proxy-Integration | 12 | Text-in/Text-out, Streaming, Rollen und Fallback? |
| Sicherheit/Reversibilität | 8 | Bypass, CCR/Rewind, Injection- und Strukturgrenzen? |
| Reife | 7 | Tests, Wartung, Dokumentation, Lizenz? |
| Popularität | 5 | begrenztes Vertrauenssignal, nicht technische Eignung |
| **Gesamt** | **100** | genau eine Krone |

Die Rohmatrix enthält 60 Spalten, darunter 29 konkrete Fähigkeitsfelder und alle neun Score-Dimensionen. Jede Zeile unterscheidet lokale Messung, Primärquellenbewertung und nicht ausgeführte Kandidaten.

## Methodenvergleich

### Prompt- und Kontextkompressoren

| Methode | Mechanismus | Upstream-Claim | Modellbedarf | Proxy-Fit |
|---|---|---|---|---|
| [LLMLingua](https://github.com/microsoft/LLMLingua) | kausale Perplexity, coarse-to-fine Tokenpruning | bis 20× | GPT-2-small bis LLaMA-7B | text-in/text-out, aber langsam/irreversibel |
| LongLLMLingua | query-aware Ranking, Reordering, Tokenpruning | 4× weniger Tokens, bis +21,4 % RAG-Leistung | kleines kausales LM | gut für RAG, nicht für beliebige Systemtexte |
| LLMLingua-2 | bidirektionale Tokenklassifikation | 3–6× schneller als LLMLingua | BERT/mBERT/XLM-R | prinzipiell gut, lokal hier zu langsam |
| [Selective Context](https://github.com/liyucheng09/Selective_Context) | self-information pruning | etwa 2× / 40 % Speicher- und GPU-Ersparnis | kleines kausales LM | Prosa, nicht Code/JSON |
| [RECOMP](https://github.com/carriex/recomp) | extraktive oder abstraktive RAG-Kompression | Kontext bis etwa 6 % | trainierter Extractor/Seq2Seq | sehr gut für Retrieval-Kontext |
| [PromptCompressor](https://github.com/JungHoyoun/PromptCompressor) | Forschungsprototyp/PCRL-Familie | kein belastbarer universeller Ratio | Policy-Modell plus Training | eher offline/task-spezifisch |
| [500xCompressor](https://github.com/ZongqianLi/500xCompressor) | Soft-Token/KV-Zustände | 6–480× | 8B-Modell, LoRA, Serving-Kopplung | nicht für gehostete Text-APIs |
| [Claw Compactor](https://github.com/open-compress/claw-compactor) | 14 deterministische/optionale Stufen | 15–82 %, reversibel je nach Stufe | modellfrei, optionale Komponenten | guter Baustein, harte Rollen-Gates nötig |

![LLMLingua GitHub](proofs/llmlingua-github.png)

![Claw Compactor GitHub](proofs/claw-compactor-github.png)

### Prompt-Enhancer/Optimierer

[linshenkx/prompt-optimizer](https://github.com/linshenkx/prompt-optimizer), [PromptWizard](https://github.com/microsoft/PromptWizard), [DSPy](https://github.com/stanfordnlp/dspy), [GEPA](https://github.com/gepa-ai/gepa), [TextGrad](https://github.com/zou-group/textgrad), [OPRO](https://github.com/google-deepmind/opro), Promptist in [LMOps](https://github.com/microsoft/LMOps), Promptflow, Agenta, Promptfoo, LangGPT und AdalFlow wurden verglichen. Ihr primäres Ziel ist höhere Taskqualität, nicht kürzere Payload. Sie gehören überwiegend offline in Promptentwicklung und Evals.

### KV-Cache und Serving-Tricks

| Klasse | Beispiele | Spart API-Input-Tokens? | Wann sinnvoll? |
|---|---|:---:|---|
| Prefix/KV reuse | LMCache, vLLM, Prompt Cache | nein | selbst gehostetes Zielmodell oder Provider-Cache |
| KV eviction | H2O, SnapKV, PyramidKV | nein | eigener Decoder/Attention-Stack |
| KV quantization | KVQuant, KIVI | nein | eigener GPU-Server mit langen Kontexten |
| Attention kernels | FlashAttention, FlashInfer | nein | eigener Inference-Server |
| Sparse/offload | MInference, TriForce, ShadowKV | nein | eigener Runtime-Stack |

Für Headroom vor Anthropic/OpenAI bleibt die Text-Payload unverändert; der Provider tokenisiert und berechnet weiterhin den vollständigen Input. Deshalb erhalten KV-only-Methoden in der Rubrik „echte Input-Token-Savings“ 0/20.

## Echte Messungen

### Aufbau

Drei realistische, deterministisch erzeugte lange Prompts wurden gespeichert:

| Fixture | Inhalt | cl100k Tokens vorab | Pflichtfakten |
|---|---|---:|---|
| `prose_rag` | 45 Dokumente, redundante Betriebsprosa, verteilte Incident-Fakten | 8.434 | Projekt, Region, Incident-ID, Deadline, Retention |
| `code_debug` | 35 ähnliche Funktionen, PaymentWriter-Code, 180 Logzeilen | 6.093 | Klasse, Invariant, Fehler-ID, Betrag, Store-Aufruf |
| `structured_json` | 160 Ledger-Datensätze mit einem kritischen Record | 14.631 | Schema, Record-ID, Betrag, Policy, Aktion |

Gezählt wurde mit `tiktoken` sowohl `cl100k_base` als auch `o200k_base`. Die Qualitätsmetrik ist bewusst konservativ und reproduzierbar: 70 % Pflichtfakten-Recall plus 30 % exakte Schutzspan-Integrität. Sie ersetzt keinen vollständigen Endtask-Benchmark; sie verhindert aber, dass reine Tokenreduktion als Qualität verkauft wird.

### Aggregat über alle drei Prompts

| Methode | Ø Savings | Ø Qualität | Ø Latenz | schlechtester Fakten-Recall | schlechtester Schutzspan |
|---|---:|---:|---:|---:|---:|
| **Gemini 3.5 Flash Low compaction** | **98,31 %** | **100 %** | 6,04 s | 100 % | 100 % |
| Claw 7.1 `compress_messages` | 67,89 % | 70,67 % | 0,88 s | 60 % | 0 % |
| Claw Text-API | 67,89 % | 70,67 % | 0,80 s | 60 % | 0 % |
| query-aware lexikalische Baseline | 64,71 % | 100 % | **9,83 ms** | 100 % | 100 % |
| LLMLingua-2 mBERT CPU | 41,40 % | 18,67 % | 36,99 s | 20 % | 0 % |
| Headroom 0.31 Router | 22,69 % | 80 % | 10,00 s | 100 % | 0 % |
| lossless Cleanup | 5,72 % | 100 % | 2,17 ms | 100 % | 100 % |
| KV-only Kontrollzeile | 0 % | 100 % | 0 ms | 100 % | 100 % |
| **Gemini Flash Low enhancement** | **−1,33 %** | 90 % | 28,53 s | 100 % | 0 % |

Die extrem hohe Flash-Kompression ist auf stark redundante Testprompts zurückzuführen und darf nicht auf beliebige Produktionstexte extrapoliert werden. Positiv ist, dass die ausgegebenen Kompaktprompts die geforderten Fakten und exakten Autoritätszeilen vollständig enthielten. Negativ sind zusätzliche Remote-Kosten, 5–8 s Latenz und eine neue Prompt-Injection-/Datenschutzgrenze.

### Per-Fixture: Flash Low compaction

| Fixture | vorher | nachher | Savings | Latenz | Qualität |
|---|---:|---:|---:|---:|---:|
| prose/RAG | 8.434 | 123 | 98,54 % | 7,66 s | 100 % |
| Code/Debug | 6.093 | 152 | 97,51 % | 4,95 s | 100 % |
| JSON | 14.631 | 162 | 98,89 % | 5,51 s | 100 % |

### Wichtige Fehlermuster

- LLMLingua-2 trennte Satzzeichen in IDs/Daten und entfernte Systemtext; bei Code und JSON blieben nur 20 % der Pflichtfakten.
- Claw veränderte selbst in `compress_messages` Systemformulierungen (`and` → `+`) und verlor im JSON-Fall den Betrag `9917.42` sowie die Policy `never_delete`.
- Headrooms Router komprimierte Code/JSON, erhielt die Fakten, veränderte aber die exakte Systemspanne und erreichte einmal sein 20-s-Kompressortimeout; der Rest wurde fail-open übernommen.
- Enhancement expandierte alle drei Prompts und ist deshalb kein Savings-Feature.
- Die query-aware Baseline schnitt auf den synthetisch klar markierten Fixtures sehr gut ab; das ist ein positiver Kontrollwert, kein Beweis für allgemeine semantische Qualität.

### Headroom-Adversarial-Eval

`headroom evals adversarial` prüfte 210 Zellen: 10 Carrier, 7 Payloadklassen und drei Positionen. Keine Payloadklasse schlug den benignen Survival-Baselinewert oder unterdrückte Kompression. Das ist ein gutes Signal für die bestehende deterministische Pipeline, ersetzt aber nicht die Sicherheitsprüfung einer externen generativen Zwischen-KI.

## Modellentscheidung

| Option | real verfügbar? | gemessen? | Urteil |
|---|:---:|:---:|---|
| **agy Gemini 3.5 Flash Low** | ja | ja | beste semantische Kompression, nur gated für große Prosa/RAG-Kontexte |
| Gemini 3.5 Flash Medium/High | ja | nein | höhere Denkstufe ohne nachgewiesenen Savings-Vorteil; nicht zuerst einsetzen |
| Codex Spark | im Headroom-Dashboard sichtbar, aber nicht als stabiler agy-Preprocessor-Endpunkt | nein | nicht als Produktionsabhängigkeit planen, bis API/Kosten/SLA klar sind |
| LLMLingua-2 mBERT lokal | ja | ja | kein API-Preis, aber auf dieser CPU viel zu langsam und ungefiltert qualitativ schwach |
| llama.cpp + kleines GGUF | Repo bewertet, kein lokales Modell aktiv | nein | möglicher späterer lokaler Dienst; erst gegen denselben Benchmark testen |
| rein deterministische Policy | ja | ja | Default-Hot-Path, billigste und sicherste Stufe |

## Zielarchitektur

```mermaid
flowchart LR
    A[Client Request] --> B[Role & Prefix Freeze]
    B --> C[Cheap Policy Classifier]
    C -->|system/developer/tool schema/code/small| D[Bypass semantic rewrite]
    C -->|structured/tool output| E[Headroom deterministic router + CCR]
    C -->|long redundant prose/RAG| F[Claw safe stages]
    F --> G{Break-even and quality gate}
    G -->|very large + low risk| H[Gemini 3.5 Flash Low compaction]
    G -->|otherwise| I[Use deterministic result]
    H --> J{Facts, spans, size, timeout pass?}
    J -->|yes| K[Forward compacted request]
    J -->|no| L[Fail open to original]
    D --> M[Headroom 127.0.0.1:8787]
    E --> M
    I --> M
    K --> M
    L --> M
    M --> N[Expensive target model]
    M --> O[Metrics + shadow ledger]
```

### Harte Invarianten

- System, Developer, Tool-Schemas und Cache-Prefixe werden byte-identisch eingefroren.
- Nur User-/Tool-Inhaltsblöcke dürfen transformiert werden; nie die gesamte serialisierte Request als ein String.
- Code, Diffs, JSON und Tabellen nutzen ausschließlich strukturwahrende Handler.
- Jede Transformation muss kleiner sein; sonst Original.
- Timeout oder Exception bedeutet Original, nicht 5xx.
- Original und Transformation erhalten einen Trace-Hash; Volltext-Logging bleibt standardmäßig aus.
- Remote-Kompression erhält keine Secrets, Credentials, personenbezogenen Daten oder privaten Repository-Inhalte ohne explizite Policy.
- Der teure Modellaufruf darf niemals auf eine fehlgeschlagene Zwischen-KI warten, sobald das Latenzbudget überschritten ist.

## Einbauplan für Headroom

### Phase 0 — Mess- und Policy-Gerüst

Neue interne Komponente `PreprocessPolicy` direkt nach Provider-Request-Parsing, aber vor Headrooms heutiger Kompressionspipeline. Sie gibt pro Content-Block `bypass`, `deterministic`, `extractive`, `semantic_compact` oder `enhance` zurück.

Vorgeschlagene Konfiguration:

| Variable | Startwert | Zweck |
|---|---:|---|
| `HEADROOM_PREPROCESSOR_MODE` | `shadow` | keine Payloadänderung |
| `HEADROOM_SEMANTIC_MIN_TOKENS` | `8000` | Remote-Break-even |
| `HEADROOM_SEMANTIC_TIMEOUT_MS` | `8000` | harte Zusatzlatenz |
| `HEADROOM_SEMANTIC_TARGET_RATIO` | `0.45` | nicht auf Maximalreduktion optimieren |
| `HEADROOM_SEMANTIC_MODEL` | `gemini-3.5-flash-low` | gemessene billige KI |
| `HEADROOM_PROTECTED_ROLES` | `system,developer` | byte-identischer Bypass |
| `HEADROOM_PREFIX_FREEZE_MESSAGES` | `all-but-latest-user` | Provider-Cache schützen |
| `HEADROOM_QUALITY_MIN_FACT_RECALL` | `1.0` | Canary-Gate |
| `HEADROOM_QUALITY_REQUIRE_SPANS` | `1` | alle Schutzspannen exakt |

Shadow-Metriken:

- `headroom_preprocess_decisions_total{decision,content_type}`
- `headroom_preprocess_tokens_total{stage,before_after}`
- `headroom_preprocess_latency_ms{stage}`
- `headroom_preprocess_fallback_total{reason}`
- `headroom_preprocess_quality_total{gate,result}`
- `headroom_preprocess_cache_prefix_mutations_total`
- `headroom_preprocess_cost_usd_total{model}`

### Phase 1 — deterministische Live-Stufe

- Lossless Cleanup und vorhandenen Headroom-Router zuerst ausführen.
- Claw nur mit einer expliziten Stage-Allowlist integrieren: zunächst `Cortex`, `RLE`, `SemanticDedup`, `LogCrunch`, `SearchCrunch`, `DiffCrunch`, `StructuralCollapse`, `TokenOpt`.
- `Nexus` und `Abbrev` bleiben aus, bis System-/Developer-Bypass und Pflichtwert-Guard bewiesen sind.
- Rewind/CCR-IDs in Headrooms bestehendem `/v1/retrieve`-Modell konsolidieren statt einen zweiten inkompatiblen Store einzuführen.

### Phase 2 — extraktive query-aware Stufe

- Nur RAG-/Dokumentblöcke, nicht Instruktionen.
- Chunk-Ranking mit kleinem Embedding-/Reranker-Modell.
- Top-K plus Diversity; alle Zitate und Dokument-IDs schützen.
- Die locally measured lexical baseline dient als Test-Orakel, nicht als alleinige Produktionsmethode.

### Phase 3 — Flash Shadow und Canary

- Flash Low nur ab 8k Tokens, nur Prosa/RAG, nur wenn erwartete Downstream-Ersparnis größer als Zwischenmodellkosten plus Latenzwert ist.
- Zuerst 100 % Shadow, dann 1 %, 5 %, 20 % Canary.
- Für jede Canary-Request Original und Compact parallel nur im Offline-Eval vergleichen; niemals zwei teure Produktionscalls erzeugen.
- Sofortiger Rollback bei Pflichtfaktenverlust, Schutzspannenmutation, höherer Gesamtkostenrate oder p95-Zusatzlatenz über 8 s.

### Phase 4 — Enhancement separat

Enhancement bekommt einen eigenen Modus und ein eigenes Budget. Es wird nur aktiviert, wenn ein Eval nachweist, dass die Taskqualität den zusätzlichen Tokenpreis rechtfertigt. Es darf weder `tokens_saved` erhöhen noch in Kompressionsquoten eingehen.

## Break-even

Eine semantische Stufe wird nur ausgeführt, wenn

`erwartete Zielmodell-Ersparnis > Zwischenmodell-Inputkosten + Zwischenmodell-Outputkosten + monetarisierte Zusatzlatenz + erwarteter Cache-Bust-Verlust`.

Praktisch benötigt die Policy mindestens:

- Zielmodell und aktueller Inputpreis,
- erwartete Ziel-Tokenreduktion aus historischen Buckets,
- Zwischenmodellpreis,
- Provider-Prefix-Cache-Status,
- Latenz-SLO der aufrufenden Anwendung.

Ohne diese Daten ist `bypass` die korrekte Entscheidung.

## Rollout-Akzeptanzkriterien

| Gate | Mindestwert |
|---|---:|
| Pflichtfakten-Recall auf Canary-Evals | 100 % |
| exakte System-/Developer-Spannen | 100 % |
| Code-/JSON-Parse-Erfolg | 100 % |
| Anteil kleinerer Ausgaben | ≥ 99 % |
| Fail-open bei Timeout/Exception | 100 % |
| zusätzliche p95-Latenz deterministisch | < 100 ms Ziel; aktueller Claw-Prototyp verfehlt dies bei großen Prosa/JSON-Prompts |
| zusätzliche p95-Latenz Flash | < 8 s |
| Netto-Kostenersparnis nach Cache-Busts | > 0, konservativ ≥ 20 % |
| Security-Eval | kein Payload-Survival-Vorteil gegenüber benignem Baseline |

## Schlussentscheidung

**Compression-Repo:** Claw Compactor, weil es im Vergleich die beste Kombination aus echter Tokenreduktion, lokaler Ausführung, Strukturstufen, Rewind-Konzept und Proxy-Nähe bietet. Es ist kein sicherer Drop-in: Systemrollen und sensible strukturierte Werte müssen von Headroom geschützt werden, und `Nexus`/`Abbrev` dürfen nicht pauschal laufen.

**Billige Zwischen-KI:** agy Gemini 3.5 Flash Low, aber nur als seltene gated Semantic-Compaction-Stufe für sehr lange, redundante Prosa/RAG-Payloads. Der reale Test war qualitativ stark und extrem kompakt, aber zu langsam und zu risikoreich für jede Prompt.

**Nicht empfohlen:** Unbedingtes LLMLingua-2 auf der aktuellen CPU, allgemeines Prompt-Enhancement im Savings-Pfad und jede KV-only-Technik als angebliche API-Tokenersparnis.

## Primärquellen

- [LLMLingua, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.825/)
- [LongLLMLingua, ACL 2024](https://aclanthology.org/2024.acl-long.91/)
- [LLMLingua-2, ACL Findings 2024](https://aclanthology.org/2024.findings-acl.57/)
- [Selective Context, arXiv 2310.06201](https://arxiv.org/abs/2310.06201)
- [RECOMP, arXiv 2310.04408](https://arxiv.org/abs/2310.04408)
- [Headroom](https://github.com/headroomlabs-ai/headroom)
- [Claw Compactor](https://github.com/open-compress/claw-compactor)
- [LLMLingua Repository](https://github.com/microsoft/LLMLingua)
- [Repository-Quellenmanifest](research/source-manifest.md)
