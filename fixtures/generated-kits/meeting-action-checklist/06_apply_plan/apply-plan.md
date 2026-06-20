# Apply Plan

## Purpose

Provide a gated, reviewable plan for applying the meeting action checklist helper if a user later approves it. This fixture itself performs no application step.

## Generated artifacts

- Candidate spec and user review gate.
- Fit check, reuse-bloat verdict, and runtime recommendation.
- Blueprint, architecture decision, and guardrails.
- Generated-artifacts index and validation report.

## Approval gates

Before applying, obtain explicit approval for the exact target surface and destination. Separate approvals are required for any installed profile update, skill installation, Workspace/gateway routing, cron schedule, MCP or credential setup, external send, GitHub push/release, destructive edit, or bulk source-of-truth change.

## Backout plan

If applied as a skill or profile patch, preserve a timestamped backup of changed files, record the target path and checksum, and restore the backup to revert. If no apply approval is granted, leave the generated kit in staging only and make no runtime changes.
