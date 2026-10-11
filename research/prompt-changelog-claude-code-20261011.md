# PROMPT CHANGELOG (Wrap) - job-application playbook run, 2026-10-11

## Full revised prompt (ready to paste)

```
Run the job-application playbook research in the project directory, end to end, with no planning questions.

Source of truth: the research spec and execution prompt (Part 2), plus the project directory's own agent-instructions file (decision rules, constraints, vocabulary). Where they differ, the local instructions win.

Steps:
1. Pre-flight: confirm last30days is installed, Python is 3.12+, run the skill's doctor, and report all three before any engine run.
2. Run the last30days engine once per research question (seven questions, plus one pass on the role family itself). Phrase each topic the way a real poster would. Follow the skill's SKILL.md contract. Save raw output inside this directory.
3. After every run read the per-source status. Only "no-results" means quiet. Anything else is "did not report." When a source class is down, run the dated fallback and say which trigger fired.
4. Write the deliverable to job-application-playbook-cc_101126.md with all four parts: prioritized playbook (each item with source URL, date, E1/E2 class, applicability note for the candidate, one DO or DON'T), gap list including conflicts, next actions for the live roles with gates kept open, source coverage report.
5. Verify before reporting: every URL and quote in the playbook must exist in the saved raw evidence.
6. Only after step 5 passes, send one email from the candidate's authorized account to the coordinating agent's address saying the work is done and ready for review, where the files are, what is solid, what did not report, and that it should be used for the job search. The candidate authorized this single send in this session.

Wrong looks like: a generic listicle. A recommendation missing a URL or date. "Nothing found" for a source that errored. A single anecdote classed E1. A flat list. Any invented number, quote, or fact about the candidate. A coach's claim labelled hiring-side. An email that says "done" before the playbook is verified, or that hides the coverage failures. Writing outside this directory.
```

## What was actually wrong

1. **Two names for the same spec.** The request named the file `job-application-playbook-research-spec-and-execution-prompt-oct-2026.md`, while this directory's CLAUDE.md refers to it by its title-case document name. The lowercase file is the one on disk and it was used. A fresh agent following CLAUDE.md alone would have looked for a file that is not there.
2. **"Execute this prompt" pointed at a document that says not to execute it in its own thread.** The spec's header says to run Part 2 in a fresh agent. This session is that fresh agent, so the instruction is satisfied, but a literal reader could have stopped.
3. **Three stacked meta-instructions (Wrap, AOC, Persist) and a skill invocation, with no stated order.** Wrap says improve first. The skill says run the engine first. AOC says do not stop at a plan.
4. **No output location or filename.** The spec defines four outputs and no place to put them. The directory's CLAUDE.md restricts writes to this folder, and the global rules require an agent-coded, dated filename.
5. **The email had no gate.** "Send an email informing the agent that the work is done" would be true or false depending on whether the run worked. Nothing said what to do if coverage failed.
6. **The skill's default save location is outside this directory** (`~/Documents/Last30Days`), which conflicts with the write-only-here constraint.

## What each change fixes

| Change | Fixes |
|---|---|
| Named the directory, the spec file, and the precedence rule (CLAUDE.md wins) | Items 1 and 2: one unambiguous source of truth |
| Ordered the work as numbered steps | Item 3: Wrap is applied silently, the skill governs the engine runs, AOC and Persist govern completion |
| Named the deliverable file and its four parts | Item 4 |
| Added a verification step and made the email depend on it. Required the email to state what did not report | Item 5: The coordinating agent is not told "done" about unverified or silently degraded work |
| "Save raw output inside this directory" | Item 6: `--save-dir` pointed at `raw-last30days-cc_101126/` |
| Added a role-family engine pass | The seven questions ask about tactics. None asks what hiring teams for these specific roles want, which every applicability note depends on |
| Added two "wrong looks like" lines (coach labelled hiring-side, email before verification) | The failure modes this run was most exposed to |

## Flags a rewrite cannot solve

- **X credentials.** The xAI key returned HTTP 403 on every pass. X did not report. This needs the account owner: a working `XAI_API_KEY`, or browser-cookie consent for X.
- **Reddit rate limits.** Every pass, including a slower sequential rerun, returned partial coverage (HTTP 429). Setting `LAST30DAYS_REDDIT_BACKEND=scrapecreators` would make the paid path primary. The skill says not to set that without the owner, so it was not set. Four threads were pulled directly instead.
- **The evidence base itself.** Almost no recruiter or hiring manager publicly described screening for AI enablement or non-engineering deployment roles in the window. A better prompt does not create that evidence.
- **LinkedIn truncation.** The engine returns about 200 characters per LinkedIn post, so several hiring-side posts cut off before the advice.
- **Unverified role terms.** Specific role terms (unposted pay, unverified remote terms) are the candidate's to verify. The playbook keeps them as gates.
- **Engagement duration conflict.** The spec carried two inconsistent durations for one engagement. No duration was written into any artifact; the resume is checked before one is.
- **Voice.** The playbook says what each letter and message should contain. It does not draft them, because drafting in the candidate's voice needs their source material.

## Verdict

Ready to run as-is. It was run. Rerun it after the X credential and Reddit rate-limit issues are fixed to see whether the gap list shrinks.
