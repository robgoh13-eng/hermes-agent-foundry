# Apply Plan Template

## Purpose

Explain what applying these staged artifacts would change.

## Generated artifacts

| Artifact | Source path | Target path if approved | Notes |
|---|---|---|---|

## Approval gates

Group approvals into one table where possible. Every row must name the exact target, command/API/patch, blast radius, rollback, verification, and approver before execution.

| Gate | Target path/API | Proposed command or patch | Blast radius | Rollback/backout | Verification after apply | Approver |
|---|---|---|---|---|---|---|
| Profile creation/update |  |  |  |  |  |  |
| Workspace routing/direct lane |  |  |  |  |  |  |
| Cron/updater scheduling |  |  |  |  |  |  |
| MCP/tool/auth/permission configuration |  |  |  |  |  |  |
| Credential/secret changes |  |  |  |  |  |  |
| External send/post/publish |  |  |  |  |  |  |
| GitHub push/PR/release |  |  |  |  |  |  |
| Destructive/bulk cleanup |  |  |  |  |  |  |

## Exact apply steps

Use commands or patch descriptions, but keep them inactive until approved.

## Verification after apply

- ...

## Backout plan

- What to disable/remove:
- Source-of-truth paths:
- Verification after rollback:
- Caveats about retained local logs/data/credentials:
