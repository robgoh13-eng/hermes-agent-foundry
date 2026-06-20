# Validation Plan

## Static checks

Run source validation with `python scripts/validate_distribution.py --mode source`. Use `--root <path>` to validate a different source tree, `--mode installed` for installed-profile checks where runtime-data hygiene is relaxed, and `--mode kit` for stage contracts plus generated-kit output headings/secret scans when real staged outputs are present.

These commands are file and deterministic replay validators. They inspect files,
contracts, headings, privacy patterns, generated-stage outputs, and fixture
metadata without calling an LLM or using credentials. `scripts/smoke_profile_replay.py`
adds a side-effect-free behavioral smoke replay against source policy anchors by
default, or against an installed profile when `--profile-root <path>` is supplied.


- YAML/frontmatter parses for generated files.
- Every numbered stage includes `CONTEXT.md`.
- Stage `CONTEXT.md` files define goal, inputs, process, outputs, allowed scope, forbidden actions, and verification.
- `.env.EXAMPLE` contains placeholders only.
- `.gitignore` and exclusion report cover known secret/runtime/user-data paths.
- Skill/tool/MCP recommendations include source URLs and verify-before-install notes.
- Existing-agent migration plans include rollback.
- Intake sufficiency is enforced: vague requests produce questions rather than generated artifacts.
- Observability has layered coverage: static validation checks the observability template/fixture hooks, and the generated build-kit validation stage requires repeated/scheduled/multi-step/status-reporting agents to include `observability-plan.md`, keep runtime logs outside distributions or gitignored, forbid secrets/raw sensitive data, and smoke-test synthetic progress/failure review.
- The generated-kit validation path also verifies required stage output files when any real outputs are present, including a validation report, gated apply plan, generated-artifacts index, fit-check outputs, and guardrail/design artifacts.
- The non-risky staged build trial uses synthetic meeting-action-checklist material only and validates as a generated kit without creating, updating, or deleting installed Hermes profiles.

## Fixture suite

1. Obvious duplicate: finance-analysis request should route to existing finance capability or skill, not new profile.
2. Skill-not-profile: repeatable checklist should become a skill draft, not a profile.
3. Justified distribution: portable research assistant with unique env/tool needs should get a distribution build kit.
4. Workspace worker candidate: durable team-member request should get staged artifacts and patch proposals only.
5. Realtime vs ICM: long reviewable reports should recommend ICM-style or hybrid and explain trade-offs.
6. Realtime-to-ICM migration: existing direct-lane worker should get a non-destructive migration plan.
7. External tool discovery: unfamiliar integration should search local skills plus web/GitHub and cite candidates.
8. Vague request: `make me an agent` should produce `I need a sharper goal before I build` plus one multiple-choice intake question, with no build artifacts.
9. Specable request: once the intended use/domain is identifiable, Agent Foundry should ask whether the user has research/notes/examples/SOPs/URLs/docs/prior specs to include, then draft a candidate spec for user review before final build/reuse/patch/no-build decision.
10. Observability request: repeated/scheduled/multi-step agents should include an observability plan and generated status-review instructions so the agent can later summarize progress, failures, blockers, and next actions from local runtime logs without leaking sensitive data.

The static validator requires all ten fixture files and verifies that fixture sections are non-empty and use exact expected classification/runtime/verdict enum values. The deterministic fixture contract harness (`python scripts/validate_fixture_contracts.py`) additionally checks intake-gate status, research/notes and candidate-spec review expectations, and forbidden-live-action expectations without making LLM or external calls. The repo-contained generated-kit evidence is validated in CI with `python scripts/validate_distribution.py --mode kit --root fixtures/generated-kits/meeting-action-checklist`, proving that real generated stage outputs satisfy the kit contract. The smoke replay harness (`python scripts/smoke_profile_replay.py`) is also CI-safe in source mode and can be run read-only against an installed profile with `--profile-root <path>` when profile evidence is needed.
