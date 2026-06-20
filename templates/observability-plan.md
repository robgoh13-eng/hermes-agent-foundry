# Observability Plan Template

Use this template when an agent/profile/worker is expected to run more than once, run on a schedule, coordinate multi-step work, or be asked later "how is it going?" / "where is it failing?"

## Purpose

Explain what the agent owner needs to understand from logs: progress, blockers, recurring failures, skipped work, handoffs, and next actions.

## Runtime log location

Default to a local, profile-scoped runtime path that is excluded from distributions and git, for example:

```text
${HERMES_HOME}/local/agent-runs/<agent-id>.jsonl
${HERMES_HOME}/local/agent-runs/<agent-id>-latest.md
```

If the agent operates inside a project repo, use a clearly gitignored runtime directory such as `.runtime/agent-runs/` only when the repo already uses that convention.

## Event schema

Each run should append concise structured events. Prefer JSON Lines for machine review plus an optional latest Markdown summary for quick human review.

Required fields:

```json
{
  "schema_version": "agent-run-log.v1",
  "event_id": "unique event id",
  "timestamp": "ISO-8601 UTC timestamp",
  "agent_id": "stable-agent-id",
  "run_id": "unique run/session/job id if available",
  "phase": "intake|plan|execute|verify|handoff|blocked|failed|done",
  "status": "started|progress|skipped|blocked|failed|completed",
  "summary": "short human-readable status",
  "inputs_ref": "non-sensitive pointer to request, file, job, or task",
  "outputs_ref": "non-sensitive pointer to artifact, report, PR, or handoff",
  "failure_kind": "none|user_input_needed|tool_failure|validation_failure|auth_missing|timeout|rate_limit|external_service|unexpected",
  "next_action": "what should happen next",
  "needs_greenlight": false
}
```

## Retention and rotation

- Keep logs local and profile-scoped.
- Rotate or summarize after a configured size or age threshold.
- Prefer summaries over raw long-term event retention.
- Keep individual events concise; if output is large, store a non-sensitive artifact reference instead of embedding it.
- If multiple processes may append to the same file, prefer one file per `run_id` or atomic append-only writes; do not rewrite shared logs in place.
- If a log accidentally contains sensitive data, stop using it, move it to a private quarantine path, create a redacted replacement summary, and note that cleanup may not erase prior backups.

## Redaction examples

- Replace tokens, OAuth codes, account numbers, raw messages, and private payloads with `[REDACTED]`.
- Keep stable non-sensitive references such as issue IDs, file paths, job IDs, validation command names, or artifact paths.
- Summarize external API failures without copying full response bodies when they may include credentials or private data.

## Privacy and safety rules

- Never log raw secrets, OAuth tokens, credentials, raw private messages, raw financial transactions, or unnecessary personal data.
- Log references and summaries, not full sensitive payloads.
- Treat runtime logs as user data: do not include them in profile distributions, generated repos, commits, or public reports.
- Redact external error payloads when they may contain credentials or private data.

## Review workflow

When the user asks how the agent is going, the agent should inspect, in order:

1. Latest status summary.
2. Recent run-log events.
3. Failed validation/test/check outputs referenced by the log.
4. Open blockers, approval gates, or handoff notes.
5. Recent session/search context only if the local run log is insufficient.

The answer should include:

- current state;
- last successful milestone;
- failures grouped by failure kind;
- likely root cause when evidenced;
- next action;
- whether user approval or external intervention is needed.

## Validation checklist

- [ ] Runtime log path is outside generated distribution artifacts or explicitly gitignored.
- [ ] Event schema has schema version, event id, status, phase, summary, failure kind, and next action.
- [ ] Generated SOUL/skill tells the agent to update and inspect its run log.
- [ ] Failure categories distinguish validation, tool, auth, timeout, external service, and user-input blockers.
- [ ] Privacy rules forbid secrets and raw sensitive data in logs.
- [ ] Retention/rotation and sensitive-log quarantine guidance is included.
- [ ] Smoke test includes either a synthetic log entry or a prompt asking the agent to summarize a fixture log.
