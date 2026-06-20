
# Stage: 03 Design

## Goal
Design the selected artifact and its guardrails.

## Inputs
- Brief
- Fit-check outputs
- Research outputs if present

## Process
1. Define scope, refusals, handoffs, inputs, outputs, and ownership.
2. Record architecture decision: ICM, real-time, hybrid, or no runtime.
3. Draft guardrail matrix and approval gates.
4. Draft observability/run-log plan for repeated, scheduled, multi-step, or status-reporting agents.
5. Draft migration plan if editing an existing real-time agent.

## Outputs
- `blueprint.md`
- `architecture-decision.md`
- `guardrails.md`
- `observability-plan.md` when the agent needs progress/failure reviewability
- Optional `existing-agent-migration.md`

## Allowed files/tools
- Read prior-stage artifacts and repository templates.
- Write design-stage artifacts only inside the approved build-kit or patch-kit directory.
- Use local file operations and safe static inspection; do not apply generated design decisions to live profiles or Workspace surfaces.

## Forbidden actions
- Do not apply live changes.

## Verification
- Architecture decision, guardrails, and observability expectations are explicit and actionable.
