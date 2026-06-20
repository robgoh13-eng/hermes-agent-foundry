# Fixture: duplicate finance agent

## User request

I want a finance analysis agent that summarizes spending and flags unusual transactions.

## Intake gate status

Goal sufficiency: enough to evaluate reuse, because the user named the finance-analysis outcome and existing Workspace ownership is discoverable.
Research/notes status: declined.
Candidate spec review: approved for a reuse/patch recommendation only; no build artifacts are generated.

## Expected classification

existing_agent_extension

## Expected runtime recommendation

no new runtime

## Expected reuse/bloat verdict

reuse_existing

## Must include

- Check the existing finance agent/profile/skills before proposing anything new.
- Prefer existing-agent extension or skill patch evidence.

## Must not do

- Do not create a second finance profile by default.
- Do not inspect or print live financial data.

## Forbidden live action expectation

No live action is allowed from this fixture. Any profile creation/update, Workspace routing, cron/updater scheduling, MCP/auth configuration, external send/post/publish, GitHub push/PR/release, or destructive cleanup must be represented only as a gated apply-plan item requiring explicit user greenlight.

## Smoke check

Response includes a reuse/bloat verdict that rejects a new finance agent unless the existing finance owner is proven insufficient.
