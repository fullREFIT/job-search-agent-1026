# Canonical opportunity record schema

One row per role, keyed by `req_id` (source + board + requisition ID). 39 columns. One writer. Unknowns stay empty.

| Column | Field | Notes |
|---|---|---|
| A | req_id | Stable key: source slug + ATS board + requisition ID |
| B | employer | |
| C | title | |
| D | lane | employment or contract |
| E | status | Lead, Verified, Rejected, Closed (system); Applied, Interviewing, Offer, Passed (candidate only) |
| F | canonical_url | Employer page, not an aggregator |
| G | first_source | Where first seen |
| H | posted_date | |
| I | first_seen | |
| J | last_live_check | Date of the most recent body read |
| K | live_check_method | e.g. board API live; body read |
| L | remote_evidence | From the posting, not inferred |
| M | ca_eligible | Location eligibility |
| N | travel_wording | Verbatim when present |
| O | pay_string | Posted range as written |
| P | pay_min | |
| Q | pay_max | |
| R | pay_state | e.g. Clears, Straddles, Below, Undisclosed - only against posted numbers |
| S | employment_type | |
| T | req_map | Fit mapping: direct and adjacent evidence |
| U | hard_screens | Gate failures |
| V | tier | |
| W | lead_proof | Why this lead is real |
| X | why_ranks | Ranking rationale |
| Y | employer_fit_screen | Verified fit notes |
| Z | evidence_gaps | What is unknown and blocking |
| AA | package_link_version | Real links only; a placeholder is worse than empty |
| AB | next_action | |
| AC | next_action_due | Real dates only |
| AD | decision_owner | The pending or recorded candidate decision |
| AE | submission_receipt | Action-specific receipt after any authorized external action |
| AF | flags | |
| AG | rejection_reason | Required on Rejected |
| AH | notes_never_overwrite | Free notes owned by the candidate; the system never writes here |
| AI | recommendation | The system's current recommendation with reasoning |
| AJ | decision_priority | Queue order |
| AK | next_action_kind | |
| AL | next_action_timezone | |
| AM | decision_question | Exactly one question per open decision |

## Rules

- Duplicates of the same requisition are rejected pointing at the canonical row.
- `package_link_version` and `next_action_due` hold real links and real dates only. A research deadline is not an interview.
- The never-overwrite notes column belongs to the candidate. The system writes nowhere near it; a mis-write there is treated as an incident and repaired immediately.
- Status transitions are explicit. Applied, Interviewing, Offer, and Passed are set by the candidate alone.
