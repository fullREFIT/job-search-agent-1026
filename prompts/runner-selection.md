# Picking a runner for the research prompt

Run the pre-flight first in whichever tool is open and pick the one with the healthiest last30days source coverage. If it is a tie:

- **Claude Code** is last30days' native home and the most likely to be fully configured (X cookie access, API keys, yt-dlp), so it gives the widest practitioner-voice coverage.
- **A general assistant thread** is the zero-setup option when the skill is already installed there; good when you want to fire it from a phone and read results in chat, but coverage depends on which API keys are configured, which the pre-flight will tell you.
- **Codex** is equivalent to Claude Code if the skill is installed under `~/.codex/skills`; pick it when that is the tool already open.

Whichever you choose, the pre-flight report is the check that you are not silently getting generic web search dressed up as last-30-days research.

## Running the same prompt twice pays off

The two runs in `research/` came from the same assignment executed independently in Claude Code and Codex. They disagreed usefully: different engine coverage, different classification strictness, and different process critiques. The comparison itself was the audit - where both runs agreed, confidence went up; where they diverged, the gap list told you why. If you only run once, you lose that check.
