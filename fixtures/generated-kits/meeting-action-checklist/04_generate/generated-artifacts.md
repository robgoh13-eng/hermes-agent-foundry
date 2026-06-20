# Generated Artifacts

## Generated artifacts

- `00_brief/brief.md` — scoped user brief for the synthetic meeting-action checklist request.
- `00_brief/candidate-spec.md` — candidate spec for user review.
- `01_fit_check/fit-check.md` — fit classification and rationale.
- `01_fit_check/reuse-bloat-verdict.md` — anti-bloat decision.
- `01_fit_check/runtime-style-recommendation.md` — runtime recommendation.
- `03_design/blueprint.md` — role, inputs, outputs, and handoffs.
- `03_design/architecture-decision.md` — selected architecture and rejected alternatives.
- `03_design/guardrails.md` — approval gates and forbidden actions.
- `05_validate/validation-report.md` — deterministic validation evidence.
- `06_apply_plan/apply-plan.md` — gated application and backout plan.

## Files intentionally not generated

- No installed profile files.
- No credentials or environment files.
- No cron jobs, MCP configuration, gateway routing, or external-send scripts.
- No GitHub release/tag artifacts.

## Validation notes

This fixture is sanitized and deterministic. It exists so CI can validate real generated stage outputs instead of only checking the static `templates/build-kit` stage contracts.
