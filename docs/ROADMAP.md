# Roadmap

## Phase 0 — Spec repository

- [x] Capture canonical portable spec in `docs/SPEC.md`
- [x] Add initial decisions, safety, validation, and templates
- [x] Keep source-repo-only Workspace implementation notes outside distribution-owned docs

## Phase 1 — Prototype build-kit generator

- [x] Draft Agent Foundry `SOUL.md`
- [x] Draft `agent-foundry-core` skill
- [x] Add stage folder templates for build kits
- [x] Add fixture requests for anti-bloat, skill-only, distribution, Workspace worker, realtime-vs-ICM, migration, external-tool-discovery, intake-sufficiency, candidate-spec, and observability cases
- [x] Add validation script for frontmatter/YAML, stage contract presence, secret denylist, template completeness, fixture contracts, source/kit/installed modes, and portable-doc checks

## Phase 2 — Local distribution packaging

- [x] Turn `distribution.yaml.draft` into `distribution.yaml`
- [x] Add `.env.EXAMPLE` with required env names only
- [x] Add GitHub Actions validation workflow
- [x] Verify no cron/MCP/gateway/workspace side effects are included in the distribution
- [x] Complete one non-risky staged build trial and validate its generated kit report/apply plan before tagging `v0.1.0`

## Phase 3 — Optional Workspace integration

- [ ] Add a future live-model behavioral replay harness for representative fixtures, if release quality needs proof beyond deterministic contracts
- [ ] Decide whether Agent Foundry remains an on-demand distribution or becomes a live Workspace worker
- [ ] Draft Workspace patch proposals only
- [ ] Apply live routing only after explicit greenlight
