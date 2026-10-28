# Execution Log: `EXP-000-baseline-example`

* **Worktree Path:** `.targets/worktrees/EXP-000-baseline-example/`
* **Target Repo:** `example-agent-repo`
* **Base Commit SHA:** `init-baseline`
* **Experiment Commit SHA:** `init-baseline`
* **Execution Timestamp:** `2026-10-28 16:30`

## 1. Sanity & Guard Run
* **Guard Command:** `pytest tests/unit -q` -> `42 passed in 3.81s`

## 2. Raw Verification Output
```json
{"pass_at_1": 0.640, "p95_latency_sec": 3.20, "episodes": 50, "failures_over_12_tools": 8}
```
