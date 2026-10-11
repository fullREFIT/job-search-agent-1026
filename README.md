# job-search-agent-1026

An agent-operated job-search system, plus the research behind it. Built and run by an AI assistant for one candidate over October 2026, adapted from a friend's multi-agent job-search package after a full review.

Everything candidate-specific has been scrubbed: no resume, no live tracker rows, no compensation floor, no employer names the candidate is pursuing, no personal identifiers. What is here is the system itself and the research method.

## What is in here

| Path | What it is |
|---|---|
| `ARCHITECTURE.md` | How the running system works: sources, coverage ledger, canonical record, verification gates, decision queue, morning review, guardrails |
| `IMPROVEMENTS.md` | Full review of the original multi-agent package and what was kept, changed, or dropped, mapped to what was actually built |
| `system/workflow.md` | Operating rules: lanes, statuses and who may set them, coverage states, liveness rule, decision flow |
| `system/opportunity-record-schema.md` | The 39-column canonical opportunity record, field by field |
| `system/sweep-example.py` | The source sweep script with sample board slugs: ATS board readers, per-source checked/empty/failed ledger, title/remote/recency filters |
| `research/` | Two independent 30-day practitioner research runs on job-application tactics (Claude Code and Codex), with their prompt changelogs, scrubbed of candidate context |
| `prompts/research-execution-prompt-template.md` | The execution prompt that produced both runs, as a reusable template with placeholders |
| `prompts/runner-selection.md` | How to pick which agent runner to execute the research in |

## The short version

- Sweep public ATS feeds (Greenhouse, Ashby, Lever, Workable, SmartRecruiters, LinkedIn guest API) and record per-source coverage as checked, empty, or failed. A quiet source is never confused with a broken one, and a failed source never counts as coverage.
- Keep exactly one canonical record per role. Duplicates are rejected pointing at the canonical row.
- A listing or a 200 response is not liveness. Liveness is the employer page body containing the role and an apply control.
- Track applications and replies before sourcing more listings. One candidate profile, hard no-invention rules, and a decision queue the candidate answers in chat.
- The agent researches, ranks, verifies, and prepares. Only the candidate sets Applied, Interviewing, Offer, or Passed. Nothing goes to an employer or recruiter without the candidate's explicit per-action approval.
- The morning review is completion-driven: today's verified result, or a clearly labeled partial/failed run with the next step. Never a fresh-looking old report.

## For the original author

Start with `IMPROVEMENTS.md`. It reviews your package honestly, keeps what is genuinely good (tracking before sourcing, one canonical profile, public ATS feeds, deterministic summaries, lessons log), and maps every ranked improvement to what was built here. The pieces worth porting back first: the coverage ledger with checked/empty/failed, the completion-driven review, and the single-writer record with explicit statuses.

## What is not here, on purpose

The candidate's resume and profile, the live opportunity tracker, search criteria (including the compensation floor), the names of employers and roles in play, prep materials, and the morning review documents. Those are private and stay private. The original multi-agent package this system was adapted from is also not republished here; it was someone else's private work, and publishing it was not ours to do.
