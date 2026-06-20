
# Stage: 04 Generate

## Goal
Generate the selected build-kit or patch-kit artifacts in staging.

## Inputs
- Design outputs
- Templates

## Process
1. Generate only artifacts justified by fit check.
2. Keep secrets out of all files.
3. Add run-log/status-review instructions to generated SOUL/skill/config drafts when `03_design/observability-plan.md` exists.
4. Produce patch proposals instead of applying live changes.

## Outputs
- Generated profile/skill/distribution files or patch proposals

## Allowed files/tools
- Read prior-stage artifacts and templates.
- Write generated drafts only inside the approved build-kit or patch-kit directory.
- Use local file operations; do not write to live profile, Workspace, gateway, cron, MCP, or credential locations.

## Forbidden actions
- No writes outside the build-kit directory.

## Verification
- Generated files are present and match the classification.
- Generated prompts include observability instructions when the design requires status/failure reviewability.
