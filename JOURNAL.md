# Lab Journal & Master Experiment Index (`JOURNAL.md`)

> **How to use this file:** Read this file first at the start of every session. It tracks our current best baselines, active follow-up ideas (`Sparks`), the complete index of conducted experiments, and the `Anti-Repeat Banlist` of refuted hypotheses.

## 1. Current Frontier (Best Verified Baselines)

| Target Repo | Task / Benchmark | Best Branch / Commit | Primary Metric | Guard Suite | Provenance Experiment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `example-agent-repo` | Multi-Step Tool Calling Bench | `main` (`init`) | `Pass@1: 64.0%`, `P95: 3.2s` | `pytest: 42/42 pass` | `[[EXP-000-baseline-example]]` |
| `example-nlp-pipeline` | Domain QA Retrieval & Synthesis | `main` (`init`) | `F1: 71.5%`, `Recall@5: 82.0%` | `pytest: 18/18 pass` | `[[EXP-000-baseline-example]]` |

## 2. Active Sparks Queue (Next Hypotheses to Test)

* **[SPARK-01] (from `[[EXP-000-baseline-example]]`, Priority: HIGH, Gap: `G1`):** Error analysis on baseline failures showed 45% of tool-call errors happen when more than 12 tool schemas are injected simultaneously. Test a lightweight schema router/filter in `src/agents/tool_selector.py`.
* **[SPARK-02] (from `[[EXP-000-baseline-example]]`, Priority: MEDIUM, Gap: `G2`):** In `example-nlp-pipeline`, queries with temporal constraints fail because chunk metadata lacks document dates. Test prepending `[Date: YYYY-MM-DD]` to chunk headers before embedding.

## 3. Master Experiment Matrix (Chronological Index)

| Exp ID | Date | Target Repo (`Branch`) | Hypothesis Tested | Metric Delta vs. Baseline | Guard Status | Verdict | One-Line Takeaway |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[[EXP-000-baseline-example]]` | 2026-10-28 | `example-agent-repo` (`main`) | Establish reproducible baseline and profile top failure modes | `Pass@1: 64.0%` (Baseline) | ✅ Pass | ✅ **BASELINE** | Tool schema overload (>12 tools) accounts for 45% of parameter hallucinations |

## 4. Anti-Repeat Banlist (Graveyard of Refuted Ideas)

* *(No refuted hypotheses recorded yet. When an experiment cleanly refutes a hypothesis (`HYPOTHESIS_REFUTED`), document it here with `[Banned Pattern] -> [Why it failed] -> [Unless condition X changes]` so future planning loops never repeat it.)*
