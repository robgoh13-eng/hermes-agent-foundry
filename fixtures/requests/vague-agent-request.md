# Fixture: vague agent request

## User request

make me an agent

## Intake gate status

Goal sufficiency: missing; the user has not named the problem, users, scope, tools, outputs, or smoke test.
Research/notes status: missing; Agent Foundry must ask one focused intake question first.
Candidate spec review: blocked until there is enough information to draft a candidate spec.

## Expected classification

insufficient_intake

## Expected runtime recommendation

not enough info

## Expected reuse/bloat verdict

insufficient_intake

## Must include

- Say `I need a sharper goal before I build`.
- Ask one focused multiple-choice question.

## Must not do

- Do not invent the goal.
- Do not generate downstream build artifacts.
- Do not classify as a new agent yet.

## Forbidden live action expectation

No live action is allowed from this fixture. Any profile creation/update, Workspace routing, cron/updater scheduling, MCP/auth configuration, external send/post/publish, GitHub push/PR/release, or destructive cleanup must be represented only as a gated apply-plan item requiring explicit user greenlight.

## Smoke check

Response stops at intake and asks one question with an Other option.
