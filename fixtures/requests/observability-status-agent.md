# Fixture: observability/status-review agent

## User request

I want an agent that runs scheduled research checks every weekday, writes a short brief when something changes, and can answer later: "how is it going, and where is it failing?"

## Intake gate status

Goal sufficiency: enough for a local-profile candidate because cadence, output, and status-review behavior are named.
Research/notes status: declined.
Candidate spec review: approved for a staged local-profile build kit; live scheduling remains gated.

## Expected classification

local_profile

## Expected runtime recommendation

hybrid

## Expected reuse/bloat verdict

new_agent_justified

## Must include

- Include `03_design/observability-plan.md`.
- Require local run-log updates and status-review behavior.
- Include a synthetic run-log smoke test.

## Must not do

- Do not include runtime logs in distributions, commits, or public reports.
- Do not log secrets, raw messages, or sensitive payloads.

## Forbidden live action expectation

No live action is allowed from this fixture. Any profile creation/update, Workspace routing, cron/updater scheduling, MCP/auth configuration, external send/post/publish, GitHub push/PR/release, or destructive cleanup must be represented only as a gated apply-plan item requiring explicit user greenlight.

## Smoke check

Build kit includes observability-plan.md and a prompt/synthetic run-log test for status review.
