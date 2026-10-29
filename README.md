# Research Lab Template (`wiki-llm` + `JOURNAL` + `experiments` + Worktree Loop)

A **Research & Experimentation Control Repository** for running disciplined, compounding ML, NLP, and AI Agent experiments across external target repositories without polluting target codebases or losing institutional memory between sessions.

---

## Core Philosophy

Instead of cluttering production or model repositories with dozens of dead experiment branches—or losing insights between AI agent sessions—this repository separates **institutional research memory** (tracked here in Git) from **execution sandboxes** (spawned as isolated `git worktree` instances under `.targets/worktrees/` and cleaned up when done).

### Three-Layer Epistemic Memory

1. **`wiki-llm/` (Compiled Semantic Knowledge Base):**
   Interlinked Markdown pages maintained by the agent: target codebase architectures (`systems/`), verified empirical lessons by topic (`findings/`), paper notes (`literature/`), and open bottlenecks (`gap_map.md`). Every system page carries a `Fingerprint: git:<sha>` header for zero-token code-drift detection.
2. **`JOURNAL.md` (Episodic Lab Journal & Experiment Index):**
   The entry point for every session. Tracks the **Current Frontier** (best verified baseline per repo), the **Active Sparks Queue** (next hypotheses to test), the **Master Experiment Matrix**, and the **Anti-Repeat Banlist** (refuted ideas that must not be repeated under the same conditions).
3. **`experiments/EXP-XXX/` (Immutable Evidence Folders):**
   Every experiment gets a permanent folder with 5 files:
   - `plan.md` — Hypothesis, linked gaps, ideation trail, experiment-language conformance, `editable_scope`, `guard_cmd`, and `verify_cmd`.
   - `execution.md` — Execution log, base/candidate commit SHAs, and technical notes.
   - `results.json` — Quantitative metrics (Baseline vs. Candidate) and `Guard` status.
   - `postmortem.md` — Error analysis, verdict (`HYPOTHESIS_SUPPORTED` / `HYPOTHESIS_REFUTED` / `INFRA_INCONCLUSIVE`), and a mandatory **`Spark`** section capturing the next hypothesis while context is hot.
   - `patch.diff` — Exact Git diff from the target worktree so any experiment can be reproduced even after its worktree is removed.

---

## Key Operating Principles

1. **Shared Experiment Language (Continuity Across Experiments):**
   Every experiment on a target repository must speak the **same language** in the broadest sense: the same concepts and vocabulary, the same structure (where components live, how runs and configs are wired), the same mental model, and the same tooling (`uv`). Anyone moving from `EXP-N` to `EXP-N+1` should immediately understand what is happening because only the hypothesis changed while the underlying frame stayed fixed. The canonical language for each repo is documented in the `Experiment Language` section of `wiki-llm/systems/<repo>.md`.
2. **Deep & Creative Ideation (`Ideate & Plan`):**
   Before planning an experiment, the agent activates the `iterative-deep-researcher` skill (`gather -> read -> think -> update`), investigates prior art and adjacent domains, and formulates **at least 3 competing hypotheses** (including non-obvious or contrarian angles) before selecting one to test.
3. **Attention Management & Subagent Delegation:**
   The orchestrating agent protects its context window for reasoning, hypothesis selection, and evaluating evidence. High-volume tasks—gathering sources/papers, implementing `plan.md` inside the worktree, and distilling updates into `wiki-llm/`—are delegated to subagents with narrow written briefs and then reviewed by the orchestrator.
4. **Python Environment Managed with `uv`:**
   Both this control repository (`pyproject.toml` + `uv.lock`) and experiment commands (`uv sync`, `uv run ...`) use `uv` exclusively rather than raw `pip` or ad-hoc virtualenvs.
5. **Skill Management via `npx skills` & `skills-lock.json`:**
   Skills are shared across the lab and all experiments using the [`skills` CLI (`npx skills`)](https://skills.sh) and locked in `skills-lock.json` (see below).

---

## Managing Shared Skills (`npx skills` & `skills-lock.json`)

All agent skills in both this lab repository and target experiment repositories/worktrees are managed via `npx skills` and pinned in `skills-lock.json`:

- **Static Copy per Instance (`.agents/skills/`):** `npx skills` installs a full **static copy** of each skill into `.agents/skills/<skill-name>/` inside the repository/instance (rather than symlinking outside the repository to a user home directory). This guarantees that every clone and every experiment worktree has a self-contained, reproducible copy of the skills.
- **Symlinks in `.claude/skills/`:** Inside the repository, `.claude/skills/<skill-name>` is a relative **symlink** pointing to `../../.agents/skills/<skill-name>`. Agents that read `.agents/skills/` (Antigravity, Gemini CLI, Codex, OpenCode, Cursor, Copilot) and agents that read `.claude/skills/` (Claude Code) all share the exact same local source of truth.
- **Automatic Worktree Provisioning:** When `uv run scripts/lab.py new-exp` creates a new experiment worktree under `.targets/worktrees/<EXP>/`, it ensures `skills-lock.json`, the static `.agents/skills/` copies, and the `.claude/skills/` symlinks are present inside the worktree (and excluded via `.git/info/exclude` so they do not pollute `patch.diff`).

### Common `npx skills` Commands

```bash
# List installed project skills and their sources
npx skills list

# Restore all locked skills from skills-lock.json into .agents/skills/
npx skills experimental_install

# Install a new skill (or all skills from a repo) into .agents/skills/ + symlink into .claude/skills/
npx skills add <owner>/<repo> --skill <skill-name> -y
npx skills add avrymi-asraf/agent-skills --all

# Check for upstream skill updates and update project skills
npx skills check
npx skills update -p -y
```

---

## Repository Structure

```text
research-lab-template/
├── AGENTS.md                        # Lab invariants and 4-phase protocol for AI agents
├── CLAUDE.md                        # Pointer to AGENTS.md (Claude Code compatibility)
├── GEMINI.md                        # Pointer to AGENTS.md (Gemini CLI compatibility)
├── JOURNAL.md                       # Lab journal: current frontier, Sparks queue, matrix & Banlist
├── pyproject.toml                   # uv project definition for the lab controller
├── uv.lock                          # Locked uv environment
├── repos.yaml                       # Manifest of external target repositories managed by the lab
├── skills-lock.json                 # Locked skill versions and hashes (managed by npx skills)
├── .agents/
│   └── skills/                      # Canonical static copies of all shared skills
├── .claude/
│   └── skills/                      # Relative symlinks (-> ../../.agents/skills/<name>)
├── skills/
│   └── experiment-lab-loop          # Symlink (-> ../.agents/skills/experiment-lab-loop)
├── scripts/
│   └── lab.py                       # Zero-dependency CLI controller for the full experiment lifecycle
├── wiki-llm/
│   ├── index.md                     # One-line-per-page catalog of the entire wiki
│   ├── purpose.md                   # Research mission, target metrics, and evaluation rules
│   ├── gap_map.md                   # Open system bottlenecks and gaps (G1, G2...)
│   ├── log.md                       # Append-only chronological operation log
│   ├── query_pack.md                # Auto-compiled pre-planning context pack (<8KB)
│   ├── systems/                     # Target repo architecture profiles, Experiment Language & Fingerprints
│   ├── findings/                    # Distilled empirical knowledge by topic
│   └── literature/                  # Paper notes and external research synthesis
├── experiments/
│   ├── _TEMPLATE/                   # Master template copied for every new experiment
│   └── EXP-000-baseline-example/    # Complete worked example of an experiment folder
└── .targets/                        # [Git-ignored] External repo clones and isolated worktrees
    ├── repos/
    └── worktrees/
```

---

## Quick Start

0. **Sync the `uv` environment (and restore locked skills if needed):**
   ```bash
   uv sync
   npx skills experimental_install
   ```
1. **Initialize the lab directories:**
   ```bash
   uv run scripts/lab.py init
   ```
2. **Register and clone/fetch external target repositories:**
   Edit `repos.yaml`, then run:
   ```bash
   uv run scripts/lab.py sync-repos
   ```
3. **Run the zero-token drift check and build the pre-planning context pack:**
   ```bash
   uv run scripts/lab.py check-drift
   uv run scripts/lab.py context-pack
   ```
4. **Scaffold a new experiment (creates `experiments/EXP-001-...` + spawns an isolated `git worktree` with shared skills):**
   ```bash
   uv run scripts/lab.py new-exp --id EXP-001 --repo example-agent-repo --title "tool-schema-pruning"
   ```
5. **Run mechanical verification (`Scope` check + `Guard` suite + `Verify` benchmark + `patch.diff` export):**
   ```bash
   uv run scripts/lab.py evaluate --exp EXP-001
   ```
6. **Record the verdict in `JOURNAL.md` and `wiki-llm/`, then clean up the temporary worktree:**
   ```bash
   uv run scripts/lab.py record-verdict --exp EXP-001 --verdict HYPOTHESIS_SUPPORTED --metric-delta "+6.2% Pass@1" --summary "Pruning unused MCP schemas reduced tool selection errors"
   uv run scripts/lab.py cleanup-worktree --exp EXP-001
   ```
