
# Stage: 01 Fit Check

## Goal
Decide whether to reuse an existing surface, build a new artifact, avoid a new runtime, or ask the user to choose.

## Inputs
- `00_brief/brief.md`
- Existing profiles, skills, docs, Workspace roster, cron, toolset/MCP inventory where available

## Process
1. Inspect existing surfaces read-only.
2. Classify the request.
3. Produce a reuse/bloat verdict.
4. Recommend runtime style.

## Outputs
- `fit-check.md`
- `reuse-bloat-verdict.md`
- `runtime-style-recommendation.md`

## Allowed files/tools
- Read-only search/inspection tools
- Build-kit directory writes only

## Forbidden actions
- Do not create or edit live agents.

## Verification
- Required output files exist and include classification, reuse verdict, and runtime recommendation.
