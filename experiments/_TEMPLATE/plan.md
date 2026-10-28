---
exp_id: EXP-XXX
title: "Short descriptive title"
date: YYYY-MM-DD
target_repo: example-agent-repo
base_branch: main
exp_branch: exp/EXP-XXX
linked_gaps:
  - G1
inspired_by:
  - SPARK-01
editable_scope:
  - "src/agents/**"
  - "src/prompts/**"
forbidden_scope:
  - "eval/**"
  - "tests/**"
guard_cmd: "pytest tests/unit -q"
verify_cmd: "python3 eval/run_bench.py --output-json"
primary_metric: "pass_at_1"
metric_direction: "maximize"
timeout_sec: 600
status: PLANNED
---
# Experiment Plan: `EXP-XXX` — [Title]

## 1. Context & Motivation
* **Gap / Spark Addressed:** [Reference `G1` in `wiki-llm/gap_map.md` or `SPARK-XX` in `JOURNAL.md`]
* **Prior Knowledge:** [What do we already know from `wiki-llm/findings/` and previous experiments?]
* **Anti-Repeat Check:** [Confirm this does not duplicate a refuted entry in `JOURNAL.md` Banlist]

## 2. Testable Hypothesis
> **If** we modify [specific component/mechanism in target repo] to [exact change], **then** [primary metric] will improve from [baseline] to at least [target threshold] without degrading [secondary metric / guard suite], **because** [mechanistic reason].

## 3. Implementation Specification
* **Files to Modify:**
  - `path/to/file.py`: [Exact change description]
* **Invariants / Constants:** [What stays strictly fixed so the comparison is fair?]

## 4. Verification & Falsification Criteria
* **Sanity Check:** [Fastest 10-second check to confirm no syntax/runtime crash]
* **Success Criterion (`KEEP`):** `guard_cmd` passes AND `primary_metric` improves by $\ge$ [X] without blowing up latency/cost.
* **Refutation Criterion (`DISCARD`):** If `guard_cmd` passes and the code runs cleanly, but `primary_metric` is $\le$ baseline, the hypothesis is refuted.
