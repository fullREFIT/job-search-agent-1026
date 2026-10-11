# Research execution prompt template

The prompt that produced both research runs, generalized. Fill every `<placeholder>` before running. Paste everything below the line into a fresh agent. A filled example of what wrong looks like is at the bottom; keep that section.

---

You are researching job-application tactics for one specific person and producing a personalized, decision-ready playbook. This is not a generic job-hunting advice roundup. Everything you need is in this prompt. Do not ask planning questions; execute.

## Who this is for

`<Candidate profile: location and timezone, trajectory, target role families, and hard gates. Example shape: a career changer moving into AI enablement and program roles, about 15 years of multi-site operations, agency growth leadership, one embedded SaaS engagement, independent consulting since a stated year. Builds real products with AI coding tools but is not a software engineer and does not want engineer-positioned roles. Has a current one-page resume and an existing portfolio.>`

Target role families: `<list>`. Hard gate: `<e.g. nothing that requires being a software engineer>`.

Constraints: `<compensation floor and how it is measured>`. `<remote / location / travel limits>`. Never invent facts about the candidate's history, and never invent statistics, quotes, or testimonials anywhere in the output. Anonymize whatever the candidate's public-content rules require.

The live roles (use these to ground applicability; do not research the companies themselves):

1. `<Role: title, reported terms, what is unverified>`
2. `<...one per live role>`

## What to research

Answer these seven questions using what practitioners, recruiters, and hiring managers have actually said and reported in the last 30 days:

1. Cover letters: do hiring managers read them for these role families now? What structure and length get replies? What do recruiters say they scan for?
2. Portfolio: what do reviewers actually look at for program/enablement roles - case-study format, outcome metrics vs. artifacts, walkthrough videos, time per review?
3. Follow-up: what timing, channel, and message content get responses after applying? What do recruiters say about frequency, and when does it hurt?
4. Direct hiring-manager outreach: should a candidate find and contact the hiring manager outside HR/recruiting channels? How do people identify the real manager? Channel tradeoffs, and what has drawn positive vs. negative reactions recently.
5. Training and certifications: which ones practitioners say recently helped land adjacent program roles, and which are credential padding? Note free vs. paid and time cost.
6. Build a project for a missing skill: when does a dedicated portfolio project beat other evidence (adjacent experience, narrative, referral)? What effort bounds are realistic? Find reported cases where a targeted project changed a hiring outcome.
7. Anything else with recent evidence of improving offer odds for these role families: referral strategies, application timing, ATS screening realities, profile signals, interview prep expectations.

## Method

Primary tool: the last30days skill (github.com/mvanhorn/last30days-skill), which pulls the last 30 days of Reddit, X, YouTube, TikTok, Hacker News, GitHub, and web discussion. If it is available in your environment, follow its SKILL.md contract exactly - do not improvise against it.

Pre-flight (mandatory; report the results):

1. Check whether last30days is installed (look in ~/.claude, ~/.codex/skills, ~/.agents/skills, or an npx skills install directory).
2. Verify Python 3.12+ is available.
3. Run the skill's doctor health check and record which sources are configured.
4. After every run, check the run's source status: "no-results" means the source worked and found nothing; "partial", "rate-limited", "auth-failed", "unreachable", "timeout", or "error" mean coverage was not established. Never write "nothing found on Reddit/X/YouTube" about a source in one of those states - say the source did not report.

Reframe keyword-trap topics before running them. Real people do not post "cover letter tips"; they post "hiring managers, what makes you actually read a cover letter?" Phrase each engine run the way a real poster would.

Fallback (only if pre-flight fails or a source class is down): use web search restricted to content dated within the last 30 days - priority subreddits, posts by recruiters and hiring managers, and recent video. Verify a date on every fallback item; if you cannot verify recency, label the item "undated - background only". Never silently degrade to generic undated advice.

Weight hiring-side voices (recruiters and hiring managers describing what they actually do) above job-seeker anecdotes. Collect both; label both.

## Quality bar

- Every recommendation carries a source URL and a publication date within 30 days of today, or is explicitly flagged as older background.
- Class every item: E1 = evidence it works (multiple independent reports, hiring-side confirmation, or a reported measurable outcome). E2 = people say it works (single anecdote or unverified job-seeker claim).
- No invented facts, statistics, quotes, or testimonials. If a number cannot be sourced, make the point without the number.

## Output format

1. Prioritized playbook, highest leverage first. Each item: the tactic; source URL(s) and date(s); evidence class (E1/E2); an applicability note for the candidate; and a concrete DO or DON'T.
2. Gap list: what the research could not answer and why (source down, no recent discussion, conflicting evidence).
3. Next actions for the live roles: for each role, the one to three playbook items to apply first and which artifact changes (cover letter, portfolio section, outreach message, follow-up plan, new project).
4. Source coverage report: which sources returned data and which failed (with the failure state), so a quiet source is never confused with a broken one.

## What wrong looks like

- A generic listicle with no applicability notes.
- Recommendations without URLs or dates, or old advice presented as current.
- "Nothing found" reported for a source that actually errored or rate-limited.
- Single anecdotes presented as proven tactics.
- An unprioritized flat list.
- Any invented statistic, quote, or testimonial.
- Asking planning questions instead of executing.
