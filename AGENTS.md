# Operational Schema: Epistemic Research Lab (`AGENTS.md`)

You operate inside a dedicated **Research & Experimentation Control Repository**.
Your mission is to systematically discover, plan, implement, verify, and document improvements across external target repositories (ML, NLP, and AI Agent systems) while compounding institutional knowledge in `wiki-llm/` and `JOURNAL.md`.

## 1. Architectural Invariants (Read First)

1. **Three-Layer Memory Discipline:**
   - `experiments/EXP-*/` is the **Immutable Evidence Layer** (raw plans, execution logs, quantitative `results.json`, `patch.diff`, and `postmortem.md`). Never rewrite past experiment results.
   - `JOURNAL.md` is the **Episodic & Routing Layer** (current baselines, active `Sparks`, master index of experiments, and the `Anti-Repeat Banlist`).
   - `wiki-llm/` is the **Compiled Semantic Layer** (`index.md`, `purpose.md`, `gap_map.md`, `systems/`, `findings/`, `literature/`). Compile new lessons into existing wiki pages rather than dumping raw logs.
2. **External Code Isolation (`.targets/`):**
   - Never modify code directly inside `.targets/repos/<repo>` (the base clone).
   - Every experiment MUST execute inside its own isolated Git worktree at `.targets/worktrees/<EXP-ID>/` on branch `exp/<EXP-ID>`, created via `uv run scripts/lab.py new-exp`.
3. **Anti-Reward-Hacking & Guard Rail:**
   - Never modify evaluation scripts, benchmark datasets, or unit tests listed in `forbidden_scope`.
   - Every experiment requires TWO mechanical checks: `guard_cmd` (regression suite that must stay green) and `verify_cmd` (benchmark/metric script).
4. **Capture Hygiene (Anti-Self-Poisoning):**
   - Strictly separate **infrastructure/setup bugs** (`INFRA_INCONCLUSIVE`) from **scientific refutations** (`HYPOTHESIS_REFUTED`).
   - If a run crashes due to OOM, missing credentials, or a typo, fix the bug or log a technical note in `wiki-llm/systems/`, but NEVER record in `wiki-llm/findings/` or the `Anti-Repeat Banlist` that the scientific idea failed until it has actually run cleanly.
5. **Shared Experiment Language (Continuity Across Experiments):**
   - Every experiment on a given target repo MUST "speak the same language" as the ones before it, in the broad sense: the **same concepts and vocabulary**, the **same structure** (where things live, how a run is wired, how configs/variants/metrics are expressed and named), and the **same mental model** of how an experiment works. Tooling (programming language, frameworks, libraries) is one part of this, not all of it.
   - The goal is readability across the lab: someone who understood `EXP-N` should open `EXP-N+1` and see at once what is happening, because only the hypothesis changed and the frame stayed the same. This also keeps results comparable: a metric delta can be attributed to the idea, not to a different way of building things.
   - The canonical language is recorded in the `Experiment Language` section of `wiki-llm/systems/<repo>.md`. Reuse its terms, files, extension points, and patterns. Do not coin new names for existing concepts, restructure the flow, add a parallel code path, or swap frameworks just because it is convenient.
   - Changing the language is only allowed when that change **is** the hypothesis. It must be stated explicitly in `plan.md`, and if the experiment is promoted, the `Experiment Language` section is updated so the next experiment inherits the new frame.
6. **Attention Management & Delegation:**
   - The orchestrating agent's context is a scarce resource reserved for judgement: choosing hypotheses, reviewing evidence, and deciding verdicts. Do not burn it on bulk work.
   - Whenever subagents are available, **delegate** self-contained, high-volume tasks: literature/source gathering, implementing the code change from `plan.md` inside the worktree, running and debugging long evaluations, and ingesting results into `wiki-llm/` (findings, gap map, index, log).
   - Give every subagent a narrow written brief (the relevant `plan.md` or postmortem section, exact paths it may touch, and the expected deliverable), then **review its output** instead of redoing the work.
7. **Python Tooling = `uv` (Lab and Targets):**
   - The lab repo is a `uv` project (`pyproject.toml` + `uv.lock`). Run every lab command as `uv run scripts/lab.py ...`, and add dependencies with `uv add`, never `pip install`, ad-hoc `venv`, or `requirements.txt`.
   - Experiment commands follow the same convention (`setup_cmd: uv sync`, `guard_cmd`/`verify_cmd` via `uv run ...`). Notebook/Colab bootstrap cells are the only place a `pip`-style install is tolerated, and only when `uv` is not available on that runtime.
8. **Shared Skills via `npx skills` & `skills-lock.json`:**
   - Skill management in both this lab repo and all experiment repos/worktrees is handled via `npx skills` (`npx skills add <owner>/<repo>`, `npx skills experimental_install`, `npx skills update -p`) backed by `skills-lock.json`.
   - Inside each repository/instance, `npx skills` stores a **static copy** of every skill in `.agents/skills/<skill-name>/` (never symlinking outside the repo to a user home folder) and creates relative **symlinks** in `.claude/skills/<skill-name> -> ../../.agents/skills/<skill-name>`.
   - `uv run scripts/lab.py new-exp` automatically provisions `skills-lock.json`, the static `.agents/skills/` copies, and the `.claude/skills/` symlinks into each new experiment worktree under `.targets/worktrees/<EXP>/`. Every experiment and subagent shares this locked skill set; never fork or edit a skill for a single experiment.

## 2. The 4-Phase Closed Experiment Loop

Whenever asked to run an experiment cycle or explore a new direction, execute these four phases in order:

### Phase 1: Evaluate & Orient (Architect Role)
1. Run `uv run scripts/lab.py check-drift` to check if any external target repository changed since `wiki-llm/systems/*.md` was last updated. If a page is flagged `DRIFTED`, inspect the git diff in `.targets/repos/<repo>` and update the system wiki page and its `Fingerprint: git:<sha>`.
2. Run `uv run scripts/lab.py context-pack` and read `wiki-llm/query_pack.md` (which compiles `purpose.md`, `gap_map.md`, and `JOURNAL.md`).
3. Drill into specific pages in `wiki-llm/findings/` and `wiki-llm/systems/` listed in `wiki-llm/index.md` that relate to the current bottleneck.

### Phase 2: Ideate & Plan (Architect Role)
This is the phase where the research is won or lost — give it real depth. Do not just pick the most obvious next tweak.
1. **Think deeply and creatively.** Activate the `iterative-deep-researcher` skill and run its gather → read → think → update loop on the target gap: look for prior art, papers, and techniques from adjacent fields; question *why* the bottleneck exists; generate **at least 3 competing hypotheses** (including at least one non-obvious or contrarian one) before choosing. Delegate the source-gathering legs to subagents (see Invariant 6) and save useful paper notes to `wiki-llm/literature/`.
2. Select and sharpen one testable hypothesis that addresses an open gap in `wiki-llm/gap_map.md` or follows a high-priority `Spark` in `JOURNAL.md`. Record the rejected alternatives and why in `plan.md` — they are future Sparks.
3. **Banlist Check:** Verify that the proposed idea does not repeat a refuted approach in `JOURNAL.md` (`Anti-Repeat Banlist`) unless testing a specific new condition noted there.
4. **Language Check:** Confirm the idea can be expressed in the repo's `Experiment Language` (Invariant 5), using its existing concepts, structure, and extension points. Creativity belongs in the *idea*, not in a new vocabulary or a new way of wiring experiments.
5. Scaffold the experiment:
   ```bash
   uv run scripts/lab.py new-exp --id EXP-XXX --repo <target-repo> --title "<short-slug>"
   ```
6. Complete `experiments/EXP-XXX-<short-slug>/plan.md` with exact `editable_scope`, `guard_cmd`, `verify_cmd`, expected metric direction, falsification criteria, and the experiment-language statement. Write it so it can serve as a self-contained brief for an implementation subagent.
   *(If operating in human-in-the-loop mode, pause here for user approval of `plan.md` before Phase 3).*

### Phase 3: Implement & Verify (Technician Role)
1. Switch focus strictly to `experiments/EXP-XXX-<short-slug>/plan.md` and the isolated worktree `.targets/worktrees/EXP-XXX-<short-slug>/`.
2. **Baseline Check:** If no baseline metric is recorded for the current base commit, run `uv run scripts/lab.py evaluate --exp EXP-XXX --baseline` first.
3. Make the minimal, atomic code or configuration changes required by `plan.md` inside the worktree and commit them to the `exp/EXP-XXX-<short-slug>` branch. Write it in the repo's `Experiment Language` (Invariant 5): the same concepts, names, file layout, and flow as previous experiments, so the diff reads as "same frame, new idea". Follow existing patterns rather than inventing new ones.
   - **Prefer delegating this step** to an implementation subagent with `plan.md` as its brief and the worktree as its only workspace; the orchestrator reviews the resulting diff and `results.json`.
4. Run mechanical verification:
   ```bash
   uv run scripts/lab.py evaluate --exp EXP-XXX
   ```
   This verifies `editable_scope`, runs `guard_cmd`, runs `verify_cmd`, saves `patch.diff`, and writes `results.json`.
5. If `execution.md` encounters a syntax/setup error, debug and retry (up to 3 attempts) before declaring `INFRA_INCONCLUSIVE`.

### Phase 4: Distill & Compound (Wiki Maintainer Role)
1. Write `experiments/EXP-XXX-<short-slug>/postmortem.md`:
   - State the verdict (`HYPOTHESIS_SUPPORTED`, `HYPOTHESIS_REFUTED`, or `INFRA_INCONCLUSIVE`).
   - Analyze *why* the metric moved (or failed to move), citing specific error cases or traces.
   - **Mandatory `Spark` Section:** While execution context is fresh, write 1–2 concrete follow-up hypotheses sparked by what you just observed.
2. Update `JOURNAL.md` via `uv run scripts/lab.py record-verdict` (or direct edit):
   - Add the row to the Experiment Matrix.
   - Update `Current Frontier` if a new best score was achieved, or add to `Anti-Repeat Banlist` if refuted.
   - Copy the new `Spark` into the `Active Sparks Queue`.
3. Update `wiki-llm/` (**delegate to a wiki-maintainer subagent** when available — hand it the finished `postmortem.md` and `results.json`, then review its edits):
   - Integrate the empirical lesson into the relevant page under `wiki-llm/findings/` (use `Status: Superseded by [[EXP-XXX]]` if overturning an older claim—never silently delete history).
   - Update `wiki-llm/gap_map.md` if a gap was resolved or a new bottleneck emerged.
   - Update `wiki-llm/index.md` and append a parseable line to `wiki-llm/log.md`.
4. Optional cleanup: run `uv run scripts/lab.py cleanup-worktree --exp EXP-XXX` (the `patch.diff` and `results.json` remain safely in `experiments/EXP-XXX/`).
