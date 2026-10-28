# Postmortem & Knowledge Distillation: `EXP-000-baseline-example`

* **Verdict:** `BASELINE`
* **Branch Action:** `Reference Baseline Recorded`

## 1. What Happened & Why (Mechanistic Analysis)
* **Quantitative Outcome:** `Pass@1 = 64.0%`, `P95 Latency = 3.2s` across 50 benchmark episodes.
* **Qualitative / Error Analysis:** Inspecting the 18 failed episodes showed that 8 of them (44.4%) occurred in episodes where more than 12 MCP tools were mounted. The model hallucinated argument names from sibling tools.

## 2. Knowledge Distillation (Updates to `wiki-llm/` & `JOURNAL.md`)
* **Wiki Pages Updated:** Created `wiki-llm/findings/tool-calling-and-routing.md` and logged Gap `G1` in `wiki-llm/gap_map.md`.

## 3. Mandatory `Spark` (Next Hypothesis While Context is Hot)
* **[SPARK-01]:** Implement a two-stage tool selector in `src/agents/tool_selector.py` that shows only 1-line tool summaries initially and expands full JSON schemas for the top-5 relevant tools.
