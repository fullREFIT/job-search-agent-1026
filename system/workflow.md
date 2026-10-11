# Operating rules

## Lanes

Two lanes in one record: `employment` and `contract`. Same fields, same gates, ranked together by evidence of fit, cash, likely time to paid work, remote/travel constraints, and warm access.

## Statuses and who may set them

System-set: `Lead`, `Verified`, `Rejected`, `Closed`.
Candidate-only: `Applied`, `Interviewing`, `Offer`, `Passed`. The agent never sets these, and never applies or contacts anyone.

`Verified` means the role passed the liveness rule and the evidence gates below. `Rejected` always carries the reason. Duplicates of the same requisition are rejected pointing at the canonical row.

## Coverage states

Every source/company pair on every sweep is recorded as:

- `checked` - reachable, postings returned
- `empty` - reachable, no postings
- `failed:<reason>` - HTTP error, timeout, blocked, auth failure
- `unsupported` - no usable route exists yet

A failed source never counts as coverage. A quiet source is never reported as "no jobs" unless it is `checked` or `empty`. The morning review carries the ledger.

## Liveness rule

A listing, an aggregator card, or an HTTP 200 is not liveness. Liveness is the employer page body containing the role and an apply control. Bodies are read on every verification pass; the check date and method are recorded on the row.

## Evidence gates per role

- Remote and location eligibility, from the posting body or a stated rule
- Travel wording, recorded verbatim when present
- Pay: posted range, or "undisclosed" - never guessed; a pay floor is checked only against posted numbers
- Scope: any engineering bar, quota, or mis-fit with the candidate's hard gates
- Role family match against the title filters

Unknowns stay empty. The system never fills a gap by inference.

## Decision queue

Anything only the candidate can decide becomes a queue row with: a recommendation, a priority, a next-action kind, and exactly one question. At most three recommended decisions surface at a time, with exact artifact links. Answered items are archived; duplicate asks are deduped by opportunity plus action, not wording.

## Morning review

Order: tracking (replies, existing applications) -> discovery (sweep) -> ranking -> verification -> brief. The brief is today's verified result or a clearly labeled partial/failed run with the next step. It includes the coverage ledger and the open decisions. It never ships a fresh-looking old report.

## External actions

Research and drafting are read-only against the outside world. Any send, application, share, or booking requires the candidate's explicit approval bound to the specific recipient and final text, and produces a success receipt with read-back. Recommendations and defaults are never permission.
