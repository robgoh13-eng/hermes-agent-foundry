
# Stage: 06 Apply Plan

## Goal
Separate generated artifacts from gated live follow-up actions.

## Inputs
- Validation report
- Generated artifacts

## Process
1. List what was generated.
2. List exact commands/actions required to apply.
3. Mark each action with its approval gate and rollback.

## Outputs
- `apply-plan.md`

## Allowed files/tools
- Read validated artifacts and validation reports.
- Draft apply steps, approval gates, and backout notes inside the approved build-kit or patch-kit directory.
- Do not execute apply steps or mutate live systems.

## Forbidden actions
- Do not perform the apply steps in this stage.

## Verification
- Apply plan is explicit enough for a separate greenlight decision.
