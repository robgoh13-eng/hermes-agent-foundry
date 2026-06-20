# Architecture Decision

## Decision

Use a skill-only or staged checklist workflow rather than a live profile, Workspace worker, cron job, MCP integration, or gateway lane.

## Alternatives considered

- New live Workspace worker: rejected because the requested job is simple, user-triggered, and does not need autonomous scheduling.
- Calendar/email integration: rejected because no credentials, account changes, sends, or external writes were approved.
- Full profile distribution: rejected as unnecessary bloat for a bounded checklist transformation.

## Consequences

The generated kit remains portable, low-risk, and reviewable. It can be applied later only after the user approves a specific destination and backout plan.
