
# Agent Foundry

Agent Foundry is an ICM-native Hermes profile distribution for designing safe, reviewable specialist agents.

It helps decide whether a requested agent should exist, checks existing-agent reuse to avoid bloat, recommends ICM-style vs real-time/hybrid/no-runtime architecture, and produces staged build/patch kits with explicit approval gates.

Generated agents that may run repeatedly, on a schedule, or across multi-step work should include a local observability/run-log plan so they can later answer how they are going, where they are failing, and what needs attention.

## Status

- Repository visibility: public-ready
- Version: `0.1.0`
- Shape: installable Hermes profile distribution
- Runtime posture: **real-time conversational shell + ICM-native build core**
- Validation posture: source/installed/kit validation modes, deterministic fixture contract harness, generated-kit fixture validation, optional installed-profile smoke replay, and GitHub Actions validation workflow
- Release posture: source/fixture/generated-kit/smoke validations pass; tag/push/release still needs explicit maintainer/reviewer approval
- Live Workspace integration: not included
- Cron/MCP/gateway changes: not included

## Install for local testing

```bash
hermes profile install github.com/<owner>/hermes-agent-foundry --name agent-foundry-test -y
# or install from a local clone:
# hermes profile install /path/to/agent-foundry --name agent-foundry-test -y
hermes profile info agent-foundry-test
```

Optional chat smoke test:

```bash
hermes -p agent-foundry-test chat -q "Classify this request only: I want a finance spending analysis agent. Should this be a new agent, existing-agent patch, skill, or no-build?"
```

Cleanup:

```bash
hermes profile delete agent-foundry-test --yes
```

## Core behavior

1. Intake the requested agent/change and enforce a sufficiency gate.
2. Run anti-bloat fit check before proposing a new agent.
3. Produce a reuse/bloat verdict.
4. Recommend runtime style: ICM, real-time/live, hybrid, or no new runtime.
5. Add observability/run-log design when the generated agent needs progress or failure reviewability.
6. Search local skills first; web/GitHub/MCP discovery only when needed and recommendation-only.
7. Generate staged build kits or patch kits.
8. Validate artifacts.
9. Produce gated apply plan.

## Intake sufficiency

Agent Foundry should not build from a vague prompt. Before generating a build kit, patch kit, migration plan, or profile/skill draft, it must be able to write a well-drafted goal covering the outcome, new-vs-existing surface, users/context, scope, inputs/tools/data, outputs/quality bar, autonomy/greenlight gates, v1/later split, and smoke test.

If those answers are missing, expected behavior is to stop with `I need a sharper goal before I build`, then ask one focused multiple-choice question at a time until the goal is sharp enough. Choices should be informed operating suggestions based on the request, not a generic fixed questionnaire. Agent Foundry also asks whether the user has research, notes, examples, SOPs, URLs, docs, prior specs, or workflow material that should shape the agent; if none exists, it records that and can offer bounded research. Agent Foundry may research local skills/docs and, when needed, web/GitHub sources before offering choices for how the agent should work. It is not limited to four options: use enough suggestions to improve the outcome, but group or narrow once the list would exceed 12. Before making the final build/reuse/patch/no-build decision, it drafts the candidate spec and asks the user to review/approve/amend it.

## Repository map

```text
.
├── distribution.yaml
├── SOUL.md
├── config.yaml
├── skills/agent-foundry-core/SKILL.md
├── templates/
│   ├── build-kit/*/CONTEXT.md
│   ├── brief.md / candidate-spec.md / user-spec-review.md
│   ├── fit-check.md / reuse-bloat-verdict.md / runtime-style-recommendation.md
│   ├── blueprint.md / architecture-decision.md / guardrails.md
│   ├── observability-plan.md / validation-report.md / apply-plan.md
│   ├── skill-tool-mcp-candidates.md
│   └── existing-agent-migration.md / existing-agent-patch-kit.md / workspace-patch-proposal.md
├── fixtures/requests/
├── fixtures/generated-kits/meeting-action-checklist/
├── .github/workflows/validate.yml
├── scripts/validate_distribution.py / validate_fixture_contracts.py / smoke_profile_replay.py
├── docs/
├── .env.EXAMPLE
└── .gitignore
```

## Validate

The validation scripts require Python plus `PyYAML`.

```bash
python -m pip install PyYAML
python scripts/validate_distribution.py --mode source
python scripts/validate_fixture_contracts.py
python scripts/validate_distribution.py --mode kit --root templates/build-kit
python scripts/validate_distribution.py --mode kit --root fixtures/generated-kits/meeting-action-checklist
python scripts/smoke_profile_replay.py
# Optional read-only installed-profile replay when a profile exists:
python scripts/smoke_profile_replay.py --profile-root <installed-profile-root>
PYTHONPYCACHEPREFIX=/tmp/agent-foundry-pycache python -m py_compile scripts/validate_distribution.py scripts/validate_fixture_contracts.py scripts/smoke_profile_replay.py
```

These checks validate repository, fixture, generated-kit, and deterministic smoke
contracts without calling an LLM, using credentials, or touching external systems.
The generated-kit fixture is sanitized source evidence from a non-risky
meeting-action-checklist staged trial, so CI validates real generated stage
outputs instead of only validating `templates/build-kit`. The smoke replay harness
checks fixture prompts against Agent Foundry policy anchors in the source tree by
default; pass `--profile-root` to run the same read-only replay against an
installed profile.

## Portability note

`config.yaml` intentionally pins a default provider/model for the
distribution's known test runtime. Treat those values as operational defaults,
not a portability promise or a recommendation for every host. Installers should
verify that the configured provider is available in the target Hermes environment
and override it with `hermes -p agent-foundry model` or by editing the installed
profile config when needed. Forks or downstream distributions may change the
default in `config.yaml`, but should not copy host-specific credentials, paths, or
personal profile settings into portable docs. Before generating real build kits,
set or confirm an explicit staging root appropriate for the host; Hermes profiles
are not filesystem sandboxes.

## Safety

Agent Foundry does not apply live profile, Workspace, cron, MCP, gateway, credential, external-send, or destructive changes without explicit greenlight. It drafts staged artifacts and apply plans first.

## Release gates

Do not tag, release, publish, push follow-up release branches, or apply generated artifacts until:

- Static source validation (`python scripts/validate_distribution.py --mode source`) passes.
- Static deterministic fixture contract validation (`python scripts/validate_fixture_contracts.py`) passes.
- Template-kit validation (`python scripts/validate_distribution.py --mode kit --root templates/build-kit`) passes.
- Sanitized generated-kit fixture validation (`python scripts/validate_distribution.py --mode kit --root fixtures/generated-kits/meeting-action-checklist`) passes, proving generated stage outputs have a validation report and gated apply plan.
- Deterministic smoke replay (`python scripts/smoke_profile_replay.py`) passes; when live/profile readiness is claimed, also run the same harness with `--profile-root <installed-profile-root>` or provide equivalent read-only smoke evidence.
- A maintainer/reviewer explicitly approves any live profile, routing, cron, MCP/auth, external publishing, GitHub, destructive, or bulk source-of-truth action.
