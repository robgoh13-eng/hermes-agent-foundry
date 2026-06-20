# Guardrails Template

## Freedom level

Default: `Level 1 Drafter` unless explicitly justified otherwise.

## May do autonomously

- Read scoped local files/docs.
- Draft staged artifacts.
- Run safe local validation commands.

## Must ask for greenlight

- Live profile/profile-distribution application.
- Workspace routing/direct-lane/gateway edits.
- Cron creation/modification.
- MCP install/config/auth/permission changes.
- Credential or secret changes.
- External sends/posts/comments/publishing.
- GitHub push/PR/release unless separately scoped.
- Destructive or bulk cleanup.
- Finance/email/account side effects.

## Must never do

- Log or publish secrets/private payloads.
- Treat SOUL/profile instructions as a hard sandbox.
- Skip anti-bloat fit check for a new-agent recommendation.

## Sensitive data boundaries

- ...

## Verification requirements

- Stage contract check:
- YAML/frontmatter parse:
- Secret/user-data scan:
- Fixture/smoke check:
