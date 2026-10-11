# Review of the original package, and what changed

The starting point was a friend's multi-agent job-search package: ten named agent specs, sweep and dashboard scripts, guards, and a lessons log. Full review verdict: a thoughtful personal workflow with documented repairs, not a tested, portable product. Its ten named components are not ten always-running agents; the daily scan and live operator are the same main session, the tailor is a skill, the specialists are ad hoc. The right move was to adapt its operating discipline, not clone the platform.

## What was genuinely good, and kept

- Track existing applications and recruiter replies before finding more listings.
- One canonical candidate profile with explicit no-invention rules; research and drafting separated from submissions.
- Public ATS feeds, verified board identity, capped deep packages, parallel workers for independent jobs.
- Deterministic summaries and counts, inbox/calendar cross-checks, backups, private views, and a candid lessons log.

## Ranked improvements, and what was built

1. **Replace the objective.** The original optimizes expected equity and deprioritizes services and contract work. Built instead: distinct employment and contract lanes in one opportunity record, ranked by evidence of fit, cash compensation, likely time to paid work, remote/travel constraints, and warm access. Equity is secondary upside, not invented odds. The blanket screening answers and the original owner's career facts were not copied.
2. **Fix coverage before more UI.** The original sweep required both a senior-title and a function regex match, so useful IC roles vanished before review; every fetch error was swallowed, so a quiet result could not distinguish "no jobs" from "failed source." Built: the coverage ledger with checked/empty/failed/unsupported per source, bounded requests with timeouts, and deliberate contract-source coverage. This is implemented in `system/sweep-example.py` and was the first repair shipped.
3. **One record and one decision surface.** Built: the 39-column canonical record (`system/opportunity-record-schema.md`) with stable requisition IDs, canonical URLs, last-live-check, lane, evidence and gaps, next action, decision, and submission receipt. Explicit statuses, allowed transitions, one writer.
4. **Completion-driven morning review.** The original brief could ship before the scan finished, and its watchdog checked only that a dated digest file existed. Built: the brief reports last successful scan plus the coverage ledger, and a partial or failed run is labeled as such with the next step.
5. **Actionable decision surface, not a second dashboard.** Built: a decision queue fed from the same record, surfacing at most three recommended decisions with exact artifact links. Decisions are answered in chat; the record is the board. Answered items archive; duplicates dedupe by opportunity plus action.
6. **Truth and permissions.** The original's hooks were tripwires, not a boundary; approval was prompt/classifier based. Built here: only the candidate sets pipeline statuses, every send needs explicit approval bound to recipient and final text, external content is treated as untrusted, and external actions require success receipts with read-back.
7. **Portable and testable replication.** The original shipped an accumulated permissions file, platform-specific document conversion, a placeholder test, and missing imports. Built: minimal footprint (one script, one record, one queue), no broad permissions, and honest "not ready" labeling instead of deploy claims.
8. **Learn from outcomes without premature experiments.** Built: outcome fields on the record (reply, interview, offer, reason lost where known) and a rule to establish a baseline before testing one change at a time.

## What was deliberately not built

No second assistant, no analytics dashboard, no A/B experiment arms, no improvement-watch system. Those add reconciliation work before they add income.
