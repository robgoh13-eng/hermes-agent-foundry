
# Stage: 05 Validate

## Goal
Run static checks and record evidence.

## Inputs
- Generated artifacts

## Process
1. Parse YAML/frontmatter.
2. Check required files.
3. Scan for secret-like content and runtime/user-data paths.
4. Verify observability plans keep runtime logs outside distributions or gitignored, forbid secrets/raw sensitive data, and define status/failure review behavior.
5. Verify candidate sources have URLs and verify-before-install notes.

## Outputs
- `validation-report.md`

## Allowed files/tools
- Read generated artifacts.
- Run safe local static validation commands.
- Inspect YAML/frontmatter, stage contracts, fixture expectations, and text files.
- Do not install packages, configure services, apply generated changes, or touch live targets.

## Forbidden actions
- Do not install or apply live changes.

## Verification
- Validation report lists commands/checks and results, including observability checks when applicable.
