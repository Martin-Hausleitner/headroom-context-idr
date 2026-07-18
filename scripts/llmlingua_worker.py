#!/usr/bin/env python3

import json
import sys
import time

from llmlingua import PromptCompressor


def main() -> None:
    source_path, output_path = sys.argv[1:3]
    payload = json.load(open(source_path, encoding="utf-8"))
    started = time.perf_counter()
    compressor = PromptCompressor(
        model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
        use_llmlingua2=True,
        device_map="cpu",
    )
    load_ms = (time.perf_counter() - started) * 1000
    results = []
    for fixture in payload:
        started = time.perf_counter()
        result = compressor.compress_prompt(
            [fixture["text"]],
            rate=0.5,
            force_tokens=fixture["force_tokens"],
            force_reserve_digit=True,
            drop_consecutive=True,
        )
        results.append(
            {
                "fixture": fixture["name"],
                "text": result["compressed_prompt"],
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
            }
        )
    json.dump({"model_load_ms": round(load_ms, 2), "results": results}, open(output_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
