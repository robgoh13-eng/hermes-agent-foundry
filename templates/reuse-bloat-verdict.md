# Reuse / Bloat Verdict

## Verdict

Choose one: `reuse_existing`, `new_agent_justified`, `no_agent_needed`, `needs_user_choice`, `insufficient_intake`.

## Existing surfaces checked

| Surface | Source/path searched | Search terms | Result | Reuse candidate? | Why accepted/rejected |
|---|---|---|---|---|---|
| Profiles | | | | | |
| Skills | | | | | |
| Workspace workers | | | | | |
| Cron jobs | | | | | |
| MCP/tool coverage | | | | | |
| Knowledge docs | | | | | |

## New-agent justification threshold

A new agent is justified only if:

- no existing owner is close enough;
- the job needs isolated memory/config/tool posture;
- expected repeated use justifies maintenance overhead;
- safety gates are clearer with a separate profile/worker;
- operational ownership is clear.

## Rationale

Explain whether this is a new role or a capability extension, citing evidence above.

## Bloat avoided / coupling introduced

- Bloat avoided:
- Coupling risk:

## Recommendation

Next artifact: no-build recommendation, skill draft, existing-agent patch kit, local profile build kit, distribution build kit, or Workspace worker candidate.
