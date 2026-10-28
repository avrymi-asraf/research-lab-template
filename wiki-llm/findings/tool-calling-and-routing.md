---
type: finding
topic: tool-calling-and-routing
status: active
confidence: initial
supporting_experiments:
  - EXP-000-baseline-example
updated: 2026-10-28
---
# Finding: Tool Schema Density & Routing Behavior

> Raw: experiments/EXP-000-baseline-example/results.json, experiments/EXP-000-baseline-example/postmortem.md

## Summary Thesis
Injecting more than 12 full JSON tool schemas into the agent context simultaneously causes a disproportionate spike in parameter hallucination and wrong-tool selection.

## Empirical Evidence
* In `[[EXP-000-baseline-example]]`, overall `Pass@1` was `64.0%` (`P95 latency: 3.2s`).
* Breakdown by active tool count in the episode:
  - `1–8 tools`: `81.2% Pass@1`
  - `9–12 tools`: `68.0% Pass@1`
  - `13+ tools`: `43.5% Pass@1` (45% of all benchmark failures occurred in this bucket).

## Open Hypotheses
* See `[[gap_map]]` (`G1`) and `SPARK-01` in `JOURNAL.md`: testing a two-stage lazy schema loader (1-line descriptions first, full JSON schema only for selected tools).
