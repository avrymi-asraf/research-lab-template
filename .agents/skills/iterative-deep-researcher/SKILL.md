---
name: iterative-deep-researcher
description: "Run research as a repeating loop of gathering, thinking, and updating findings - with an open, creative, skeptical mind. Use whenever the user asks for deep research, a thorough investigation, uncovering hidden or non-obvious information, testing a hypothesis against evidence, cross-referencing sources across languages, reading full primary documents to find new leads, or vetting source credibility on any topic."
---
# Iterative Deep Researcher

Research is not one search and an answer. It is a loop: **gather -> read -> think -> update findings -> ask the next, sharper question**, repeated many times. Each cycle should change what you know, what you believe, and what you look for next. Stay open-minded and creative throughout: the goal is to discover what is actually there, not to confirm what you expected.

## When to Use

  - Deep-dive investigations where first-page search results or snippets are not enough.
  - Questions where the answer is unclear, contested, or likely to change as evidence comes in.
  - Uncovering subsurface facts, raw data, or non-obvious connections across complex topics.
  - Topics whose ground truth sits in several languages, archives, or technical sources.
  - Evaluating conflicting claims that need source provenance and full-document inspection.

## Core Operational Mandates

### 1. The Research Loop: Gather -> Read -> Think -> Update Findings -> Re-Query

**Never treat research as a single pass.** Run a continuous multi-cycle loop until the goal and every new angle it opened are exhausted:

1.  **Gather & Save (a separate stage - see section 3):** Search broadly and in a targeted way for primary sources, raw data, filings, and full documents - and save them to disk. Delegate this to subagents whenever possible.
2.  **Read the Full Sources:** Do not settle for snippets or abstracts. Read the saved full text and look for what summaries hide: footnotes, bibliographies, docket numbers, exact dates, minor names, technical terms, contradictions.
3.  **Think:** Stop and reason about what you just read. *What does this change? Which hypothesis does it support or break? What is surprising? What would explain it? What is still missing?*
4.  **Update Findings:** Write the result into your working findings document: new facts (with their source), revised beliefs, hypotheses gained or dropped, and confidence levels. When a finding changes, record what changed and why - do not silently overwrite.
5.  **Re-Query (Pivot & Deepen):** Turn the new names, terms, citations, and open questions into the next round of sharper searches and gathering briefs.
6.  **Repeat:** Keep cycling as long as each round still produces new questions or changes your understanding.

### 2. Open Mind & Creative Thinking (Crucial Mandate)

**Act as a curious, independent investigator - not a summarizer, and not an advocate for your first guess.**

  - **Hold several hypotheses at once:** Keep competing explanations alive in your findings document. Do not lock onto the first plausible answer.
  - **Look for evidence against yourself:** In every cycle, deliberately search for what would prove your current view wrong. A finding that survived a real attempt to refute it is worth far more than one that was only confirmed.
  - **Let the evidence move you:** When a source contradicts what you believed, update - and note it. Changing your mind is the loop working, not failing.
  - **Generate original angles:** Ask *"Why does this pattern exist?"*, *"Who benefits?"*, *"What happens if I look at this from the opposite direction?"*, *"What would I expect to see if this were false?"*
  - **Follow the unexpected thread:** An odd detail, footnote, name, date, or number inside a document is a lead. Log it and open a branch for it.
  - **Connect across cycles:** Combine data points from different rounds, documents, and languages into insights that no single source contains.

### 3. Gathering Is Its Own Stage - Delegate It and Give It Attention (Crucial Mandate)

**Thinking is only as good as the raw material under it.** When an agent searches, reads, and reasons in one pass, it sees a snippet, recognizes the rough shape, and completes the rest from memory - plausible-sounding facts, quotes that were never said, and links that do not exist. To prevent this, **separate gathering from thinking.**

  - **Delegate gathering to subagents - mandatory when available:** Search, download, text extraction, and organizing go to subagents. Do not spend your own context on paging through search results or fighting downloads; keep it for thinking, judging evidence, and connecting the dots. Give each subagent a narrow brief (one lead, language, archive, or document set), a folder to save into, and ask it to return a **manifest of what it actually obtained** - exact URL fetched, local path, title, date, language, type - plus a list of what it could not get. Never ask it for "a summary of what is out there".
  - **Keep a source library on disk:** raw files (`sources/raw/`), extracted full text (`sources/text/`), and an index (`sources/INDEX.md`) with one row per source and its status (obtained / partial / not obtained). Use domain data-source skills and APIs where they exist (e.g. `library-data-sources`).
  - **Verify the manifest:** spot-check saved files - do they exist, contain the claimed content, and match the claimed URL?
  - **Reason only on top of saved material:** every link you cite is one that was fetched, and every quote is copied from a saved text. If a source could not be obtained, say so - do not reconstruct it.
  - **Gather every iteration:** each new question from thinking becomes the next gathering brief. Gathering is not a one-time step at the start; it is the first part of every cycle.

### 4. Long-Horizon Patience & Active Attention Management (Crucial Mandate)

**Deep research is a long mission - DO NOT rush to finish it.** Premature conclusions destroy research quality.

  - **Resist premature closure:** Do not cut the loop short to produce a fast answer. Keep going until the open leads are worked through.
  - **Externalize your working memory:** Maintain a working findings document and a **To-Do list** that track:
    - Open questions and the competing hypotheses being tested.
    - Documents waiting to be gathered and read.
    - New leads, footnotes, and names extracted from sources.
    - Current findings, their sources, confidence levels, and what changed in each cycle.
  - **Edit on the fly:** Update, reorganize, and check off items in real time as the loop runs.
  - **Leverage parallelism:** Whenever subagents or parallel tool calls are available, gathering always goes to them (section 3); also use them to explore independent leads or process long documents in parallel.

### 5. Strict Source Credibility & Provenance

**Treat every claim with skepticism until its origin is verified.**

  - **Trace the chain of custody:** Is the source primary (raw data, official records, filings, original papers, direct testimony) or an echo (aggregators, PR, blogs quoting blogs)? Push past echoes to the root document.
  - **Keep direct links and raw artifacts:** Preserve the exact URLs and the saved full texts for everything you rely on.
  - **Evaluate authority and bias:** Who created this, with what expertise and what incentives?
  - **Grade and surface conflicts:** State how reliable each key source is. Show conflicts between sources instead of smoothing them over, and flag single-source claims.

### 6. Subsurface Excavation & Multi-Lingual Search

**Do not stop at the obvious sources or a single language.**

  - **Search in multiple languages:** Translate key concepts, names, and terms into the languages relevant to the topic and region. Primary discussions and local archives often exist only in another language.
  - **Use indirect channels:** When direct queries come back thin or sanitized, pivot to raw datasets, footnotes, bibliographies, archived versions, regulatory filings, niche forums, technical repositories, local press, and contrarian critiques.
  - **Read between the lines:** Notice what is omitted, sudden changes in terminology, statistical anomalies, and peripheral details.

## Execution Principles

  - **Every cycle must change something:** new evidence, a revised belief, a dropped hypothesis, or a sharper question. If a cycle changed nothing, change the approach.
  - **Gather before thinking:** Each cycle starts by gathering and saving raw sources (delegated when possible); reasoning happens on saved material only.
  - **Think before re-querying:** Do not chain searches mechanically. Pause after reading to reason and update findings.
  - **Unhurried looping:** Keep iterating while reading still yields new questions or angles.
  - **Cross-verification:** Check claims across independent primary sources and record links and reliability.

## Gotchas

  - **Anchoring on the first answer:** Searching only for support of an early guess. Keep competing hypotheses and look for disconfirming evidence every cycle.
  - **Looping without thinking:** Running search after search without stopping to update findings. The loop is research -> think -> update, not just search.
  - **Rushing to finish:** Treating deep research like quick Q&A leads to shallow results.
  - **Relying on snippets:** Snippets hide the best leads. Read the full source.
  - **Losing track of leads:** Without a live findings document and To-Do list, footnotes and branches are forgotten.
  - **Language lock-in:** Searching only in the prompt's language misses local primary sources.
  - **Treating repetition as truth:** Ten articles repeating one press release are one weak source. Trace back to the root.
  - **Completing from memory:** Writing what a source "probably says", or a URL that "should" exist. Every link must have been fetched and every quote copied from a saved file; otherwise mark it "not obtained".
  - **Gathering in your own context:** Doing search and download yourself when subagents are available wastes the attention you need for thinking. Delegate it, and check the manifest that comes back.
