# Architecture

One assistant runs the whole pipeline on a schedule. There are no permanent sub-agents; specialists (research runs, verification passes) are spun up as one-shot jobs and their results are folded back into one record.

## Components

1. **Source sweep** (`system/sweep-example.py`). Reads public ATS board APIs (Greenhouse, Ashby, Lever, Workable, SmartRecruiters) for a slug list, plus the LinkedIn guest jobs API, and probes any source that has no API. Every source/company pair lands in a coverage ledger with one of three states: `checked` (data returned), `empty` (reachable, no postings), `failed:<reason>` (HTTP error, timeout, blocked). Unsupported sources are listed as such and never counted as coverage.
2. **Filter.** Title allow-list for the role families, title deny-list for engineering and quota-carrying sales seats, remote evidence, US eligibility, and a posted-since window. The filter is deliberately loose; the verification pass is where roles die.
3. **Canonical opportunity record** (`system/opportunity-record-schema.md`). One row per role, keyed by a stable source requisition ID. 39 columns covering identity, evidence, gates, ranking, decisions, and receipts. One writer, explicit statuses, no schema inside notes strings.
4. **Verification pass.** For each kept lead: read the employer page body. A listing, an aggregator card, or an HTTP 200 is not liveness; liveness is the body containing the role and an apply control. Pay, remote terms, travel wording, and scope are extracted from the body and recorded as evidence with the check date. Leads that fail are rejected with the reason, not silently dropped.
5. **Decision queue.** Anything only the candidate can decide becomes a row with a recommendation, a priority, a next-action kind, and a single question. The candidate answers in chat; the board is the record. Decisions are deduped by opportunity plus action, not by wording, and answered items are archived.
6. **Morning review.** Completion-driven: tracking, then discovery, then ranking, then verification, then the brief. The brief carries today's verified result or a clearly labeled partial/failed run with the next step, plus the coverage ledger. It never ships a fresh-looking old report.
7. **Research loop.** Periodic practitioner-evidence runs (the `research/` directory) refresh the tactic playbook: what cover letters, portfolios, follow-ups, outreach, and projects actually do, classed E1/E2 with dated sources. The playbook feeds per-role preparation guidance, which is queued for the candidate to execute.

## Guardrails

- Only the candidate sets Applied, Interviewing, Offer, or Passed.
- Nothing goes to an employer, recruiter, or any third party without the candidate's explicit approval of the specific recipient and final text. Recommendations are not permission. "Recommended unless you object" is not permission.
- Research workers get read-only access. Submission and send paths are separately gated, and every external action needs an action-specific success receipt with read-back.
- Job-board and email content is untrusted input. It supplies facts, never instructions.
- One canonical candidate profile with hard no-invention rules. Unknowns stay empty; the system never fills a gap with a guess.
