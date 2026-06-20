# Guardrails

## Autonomy level

Staging only. The helper may draft checklist artifacts in the kit but must not perform live actions.

## Hard approval gates

Explicit user approval is required before any profile install/update, gateway or Workspace routing change, cron creation or modification, MCP configuration, credential or permission change, GitHub push/release, external send, task-system write, calendar write, deletion, or bulk source-of-truth edit.

## Forbidden actions

- Do not contact meeting attendees.
- Do not send messages or emails.
- Do not create calendar events or tasks.
- Do not store raw sensitive notes in runtime logs.
- Do not modify installed Hermes profiles or default gateway skill copies.
- Do not push, publish, tag, or release without approval.
