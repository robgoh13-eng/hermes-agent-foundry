# Stage CONTEXT Template

## Goal

What this stage must accomplish.

For intake/brief stages, the goal must be strong enough to support a meaningful build or improvement, include the user research/notes status, and produce a candidate spec for review. If it is not, the stage output is one focused question, not a guessed design.

## Inputs

Required source files, user answers, prior-stage artifacts, and external references.

## Process

Numbered steps the agent should follow.

## Outputs

Files/artifacts this stage must produce.

## Allowed files/tools

Explicitly permitted paths and tools.

## Forbidden actions

Actions this stage must not perform.

## Verification

Checks that prove the stage is complete.

For intake/brief stages, verification must confirm either:

- the completed brief includes problem/outcome, target surface, users/context, scope, inputs/tools/data, user research/notes status, outputs/quality bar, autonomy/greenlight gates, v1/later scope, smoke test, candidate spec, and user review record; or
- the agent stopped and asked more questions instead of proceeding.

For agents that run repeatedly, on a schedule, across multiple steps, or that will be asked for later status/failure reviews, verification must also confirm an observability plan exists, runtime logs are stored outside generated distributions or explicitly gitignored, and logs exclude secrets/raw sensitive data.
