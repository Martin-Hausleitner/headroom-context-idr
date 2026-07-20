#!/usr/bin/env python3

from __future__ import annotations

import csv
import json
import re
import subprocess
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "headroom-context-report.md"
OUTPUT = ROOT / "QUALITY-GATE.md"
RESULTS = ROOT / "quality-gate.json"
PUBLIC_REPO_URL = "https://github.com/Martin-Hausleitner/headroom-context-idr"
PUBLIC_BLOB_URL = f"{PUBLIC_REPO_URL}/blob/main/headroom-context-report.md"
PUBLIC_REMOTE_URL = f"{PUBLIC_REPO_URL}.git"


def check_url(url: str) -> tuple[str, bool, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "headroom-context-idr/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return url, 200 <= response.status < 400, str(response.status)
    except urllib.error.HTTPError as error:
        return url, error.code in {401, 403, 429}, str(error.code)
    except Exception as error:
        return url, False, type(error).__name__


def main() -> None:
    checks = []

    def record(name: str, passed: bool, evidence: str) -> None:
        checks.append({"name": name, "passed": passed, "evidence": evidence})

    report = REPORT.read_text(encoding="utf-8")
    header = report.splitlines()[0]
    header_pattern = (
        r"^\[ L\d{2} · R\d{3} \] 🟣 Codex · gpt-5\.6-sol · "
        r"🧠 IDR: ja · 🕐 \d{4}-\d{2}-\d{2} \d{2}:\d{2} CE(?:S)?T$"
    )
    record("Reportkopf IDR: ja", re.fullmatch(header_pattern, header) is not None, REPORT.name)
    notebook_url = "https://notebooklm.google.com/notebook/4cbe42bf-f9ec-4c8b-8b6c-e6501f50478b"
    record("NotebookLM-Link im Kopf", notebook_url in "\n".join(report.splitlines()[:10]), notebook_url)
    record("Mermaid-Architektur", "```mermaid" in report and "flowchart LR" in report, "Zielarchitektur")
    record("100-Punkte-Rubrik", "**Gesamt** | **100**" in report, "Rubriktabelle")
    record("Krone im Report", report.count("👑") == 1, "genau eine empfohlene Repo-Krone")
    record("Report mindestens 25 KiB", REPORT.stat().st_size >= 25 * 1024, f"{REPORT.stat().st_size} Bytes")

    matrix_path = ROOT / "data" / "repository-matrix.csv"
    matrix_text = matrix_path.read_text(encoding="utf-8")
    with matrix_path.open(newline="", encoding="utf-8") as handle:
        matrix = list(csv.DictReader(handle))
    record("50 Repository-Zeilen", len(matrix) == 50, str(len(matrix)))
    record("Mindestens 50 Matrixfelder", len(matrix[0]) >= 50, str(len(matrix[0])))
    required_matrix_fields = {"repository", "github_url", "homepage", "license", "stars", "total_100"}
    record(
        "GitHub, Website, Lizenz, Stars und Score je Matrixzeile",
        required_matrix_fields <= set(matrix[0])
        and all(row["github_url"] == f"https://github.com/{row['repository']}" for row in matrix)
        and all(row["license"] and row["license"] != "NOASSERTION" for row in matrix)
        and all(row["stars"].isdigit() and int(row["stars"]) >= 0 for row in matrix),
        ", ".join(sorted(required_matrix_fields)),
    )
    record(
        "Report und CSV gegenseitig verlinkt",
        "data/repository-matrix.csv" in report and PUBLIC_BLOB_URL in matrix_text,
        "Report → CSV → gerenderter Report",
    )
    crowns = [row for row in matrix if row["crown"] == "CROWN"]
    record("Genau eine Matrix-Krone", len(crowns) == 1, crowns[0]["repository"] if crowns else str(len(crowns)))
    scores = [float(row["total_100"]) for row in matrix]
    record(
        "Matrix nach TOTAL-SCORE sortiert",
        scores == sorted(scores, reverse=True) and matrix[0]["crown"] == "CROWN",
        f"top={matrix[0]['repository']} ({matrix[0]['total_100']})",
    )
    score_fields = ["savings_20", "quality_20", "latency_10", "local_deploy_10", "model_footprint_8", "proxy_integration_12", "safety_reversibility_8", "maturity_7", "popularity_5"]
    score_sums = [abs(sum(float(row[field]) for field in score_fields) - float(row["total_100"])) < 0.01 for row in matrix]
    record("Alle Scores summieren korrekt", all(score_sums), f"{sum(score_sums)}/{len(score_sums)}")
    record("Alle Scores in 0..100", all(0 <= float(row["total_100"]) <= 100 for row in matrix), "total_100")
    captured_values = {row["captured_at_utc"] for row in matrix}
    captured_at = datetime.fromisoformat(next(iter(captured_values))) if len(captured_values) == 1 else None
    capture_age = datetime.now(UTC) - captured_at if captured_at else None
    record(
        "GitHub-Metadaten-Snapshot höchstens 24 Stunden alt",
        capture_age is not None and capture_age.total_seconds() <= 86_400,
        next(iter(captured_values)) if len(captured_values) == 1 else f"{len(captured_values)} Zeitstempel",
    )

    benchmark = json.loads((ROOT / "benchmarks" / "results" / "benchmark-results.json").read_text(encoding="utf-8"))
    rows = benchmark["rows"]
    fixtures = {row["fixture"] for row in rows}
    methods = {row["method"] for row in rows}
    record("Drei lange Promptklassen", len(fixtures) == 3, ", ".join(sorted(fixtures)))
    record("Zehn gemessene Methoden", len(methods) == 10, str(len(methods)))
    record("30 Benchmark-Messzeilen", len(rows) == 30, str(len(rows)))
    record("Zwei Tokenizer", set(benchmark["tokenizers"]) == {"cl100k_base", "o200k_base"}, ", ".join(benchmark["tokenizers"]))
    formulas = [abs((int(row["before_cl100k"]) - int(row["after_cl100k"])) - int(row["saved_cl100k"])) == 0 for row in rows]
    record("Token-Savings arithmetisch korrekt", all(formulas), f"{sum(formulas)}/{len(formulas)}")
    record("LLMLingua real ausgeführt", any(row["method"] == "llmlingua2_mbert_cpu" and "measured" in row["evidence"] for row in rows), benchmark["llmlingua_model"])
    record("Claw gepinnt und ausgeführt", benchmark.get("claw_compactor_commit") == "c1b936d40b1145c7a257bd6e34a17994f467495f", benchmark.get("claw_compactor_commit", "missing"))
    record("Flash compaction real ausgeführt", any(row["method"] == "agy_gemini_3.5_flash_low_compaction" and "measured remote" in row["evidence"] for row in rows), "Gemini 3.5 Flash Low")

    notebook = json.loads((ROOT / "research" / "notebooklm" / "queries.json").read_text(encoding="utf-8"))
    record("Fünf NotebookLM-Cross-Queries", len(notebook["queries"]) == 5, str(len(notebook["queries"])))
    record("Alle NotebookLM-Antworten nichtleer", all(query["result"].get("answer") for query in notebook["queries"]), "queries.json")
    manifest_urls = re.findall(r"^\d+\. (https://\S+)$", (ROOT / "research" / "source-manifest.md").read_text(encoding="utf-8"), re.M)
    record("40 Quellen im Manifest", len(manifest_urls) == 40, str(len(manifest_urls)))

    pngs = list((ROOT / "proofs").glob("*.png"))
    valid_pngs = [path for path in pngs if path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n") and path.stat().st_size > 10_000]
    publication_screenshot = ROOT / "proofs" / "github-report-rendered.png"
    record(
        "Vier echte Browser-Screenshots inkl. GitHub-Render",
        len(valid_pngs) == 4 and publication_screenshot in valid_pngs,
        ", ".join(path.name for path in valid_pngs),
    )

    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", report)
    local_links = sorted({link for link in links if not link.startswith(("http://", "https://"))})
    missing_local = []
    for link in local_links:
        target = link.split("#", 1)[0]
        if target and not (ROOT / target).exists():
            missing_local.append(link)
    record("Alle lokalen Reportlinks vorhanden", not missing_local, ", ".join(missing_local) or str(len(local_links)))

    external_links = sorted({link for link in links if link.startswith(("http://", "https://"))})
    with ThreadPoolExecutor(max_workers=12) as executor:
        url_results = list(executor.map(check_url, external_links))
    bad_urls = [f"{url} ({status})" for url, passed, status in url_results if not passed]
    record("Externe Reportlinks erreichbar", not bad_urls, ", ".join(bad_urls) or str(len(url_results)))

    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    record("GitHub-Remote ist der öffentliche Ziel-Repo", remote == PUBLIC_REMOTE_URL, remote)
    _, blob_passed, blob_status = check_url(PUBLIC_BLOB_URL)
    record("Gerenderter GitHub-Blob öffentlich erreichbar", blob_passed and blob_status == "200", f"{PUBLIC_BLOB_URL} ({blob_status})")

    try:
        health = json.loads(urllib.request.urlopen("http://127.0.0.1:8787/health", timeout=10).read())
        healthy = health.get("status") == "healthy" and health.get("ready") is True and health.get("version") == "0.31.0"
        record("Live Headroom gesund", healthy, json.dumps({key: health.get(key) for key in ("status", "ready", "version")}))
    except Exception as error:
        record("Live Headroom gesund", False, type(error).__name__)

    source_list = subprocess.run(
        ["nlm", "source", "list", "4cbe42bf-f9ec-4c8b-8b6c-e6501f50478b"],
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )
    sources = json.loads(source_list.stdout)
    record("NotebookLM hat 40 verarbeitete Quellen", len(sources) == 40 and all(source.get("status") == 2 for source in sources), f"count={len(sources)}")

    passed = sum(check["passed"] for check in checks)
    verdict = "PASS" if passed == len(checks) else "FAIL"
    lines = [
        "# Quality Gate",
        "",
        f"**Verdikt: {verdict} — {passed}/{len(checks)} Checks bestanden.**",
        "",
        "| Check | Ergebnis | Evidenz |",
        "|---|:---:|---|",
    ]
    for check in checks:
        result = "PASS" if check["passed"] else "FAIL"
        evidence = str(check["evidence"]).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {check['name']} | {result} | {evidence} |")
    lines.extend(
        [
            "",
            "## Scope",
            "",
            "Dieses Gate prüft Briefing-Vollständigkeit, Matrix- und Benchmark-Invarianten, NotebookLM-Provenienz, Link-/Screenshot-Beweise, die öffentliche GitHub-Publikation und den Live-Health-Status. Es ersetzt keine Produktions-Canary mit privaten realen Prompts.",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    RESULTS.write_text(json.dumps({"verdict": verdict, "passed": passed, "total": len(checks), "checks": checks}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": verdict, "passed": passed, "total": len(checks), "failed": [check["name"] for check in checks if not check["passed"]]}))
    if verdict != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
