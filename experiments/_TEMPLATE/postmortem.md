# Postmortem & Knowledge Distillation: `EXP-XXX`

* **Verdict:** `[HYPOTHESIS_SUPPORTED | HYPOTHESIS_REFUTED | INFRA_INCONCLUSIVE]`
* **Branch Action:** `[Kept & Promoted | Reverted / Worktree Cleaned]`

## 1. What Happened & Why (Mechanistic Analysis)
* **Quantitative Outcome:** [Compare candidate metrics against baseline from `results.json`]
* **Qualitative / Error Analysis:** [Which specific examples, slices, or agent trajectories improved or regressed? Why?]

## 2. Knowledge Distillation (Updates to `wiki-llm/` & `JOURNAL.md`)
* **Wiki Pages Updated:**
  - `wiki-llm/findings/...`: [What durable lesson was added or superseded?]
  - `wiki-llm/gap_map.md`: [Did this close a gap or reveal a new one?]
* **Anti-Repeat Banlist Entry (if refuted):** [If `HYPOTHESIS_REFUTED`, state the exact rule to add to `JOURNAL.md` Section 4]

## 3. Mandatory `Spark` (Next Hypothesis While Context is Hot)
* **[SPARK-NEW]:** [Based on the specific failure modes or behaviors observed right now in this run, what is the single highest-leverage follow-up experiment we should run next?]
