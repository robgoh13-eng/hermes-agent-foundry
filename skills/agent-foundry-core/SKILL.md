---
name: agent-foundry-core
description: Design Hermes agent build kits and existing-agent patch kits using anti-bloat fit checks, ICM stages, runtime-style recommendations, and gated validation.
version: 0.1.0
author: Agent Foundry contributors
license: MIT
tags: [hermes, agents, profile-distributions, icm, build-kits, guardrails]
---

# Agent Foundry Core

Use this skill whenever the user asks to create, revise, package, migrate, or evaluate a Hermes agent/profile/skill/worker/distribution.

Agent Foundry is **ICM-native with a real-time conversational shell**:

- conversational for intake, clarifications, status, and greenlight gates;
- staged/filesystem-first for non-trivial design, research, generation, validation, and apply planning.

## Prime directive

Do not create durable agent surface area until you have checked whether an existing surface can be reused. New agents create cognitive, routing, maintenance, and safety overhead.

## Intake sufficiency gate

Before any build kit, patch kit, migration plan, profile draft, skill draft, or Workspace-worker proposal, make sure the user has provided enough information to write a **well-drafted goal** and a candidate agent spec that the user has reviewed. If not, pause and ask more questions.

Minimum goal contract:

1. What problem/opportunity should the agent solve, and what outcome should improve?
2. Is this a new agent, an improvement to something existing, a skill/checklist, a migration, or a no-build evaluation?
3. Who will use it and in what context?
4. What is in scope, explicitly out of scope, and v1 vs later?
5. What inputs/data/tools will it read, and what sensitive boundaries apply?
6. Does the user have research, notes, examples, SOPs, URLs, docs, prior specs, or existing workflow material that should shape the agent? If not, record `none yet`.
7. What outputs should it produce and what quality bar makes them useful?
8. What decisions/actions may it take autonomously vs only recommend?
9. What actions always require greenlight?
10. What existing agent/profile/skill/tool is closest?
11. What is the smallest meaningful smoke test or acceptance check?

If the request does not satisfy this contract, do **not** proceed by inventing a build. Respond with “I need a sharper goal before I build” and ask **one** focused intake question at a time. This rule is interface-agnostic: use the same progressive multiple-choice style in CLI, API, Discord, Telegram, Slack, and any other surface. The question should be multiple choice whenever possible so the user can answer quickly: use the `clarify` tool only in an interactive messaging session where waiting for a choice prompt is appropriate; in CLI/one-shot contexts or when uncertain, render one plain-text multiple-choice question plus “Other”. Do not label questions as `1/N`, imply that the user must answer a fixed-length questionnaire, or ask a bundled list. For vague requests, use the contract above as an internal checklist, but expose only the single highest-impact next question in the current turn. For partially specified requests, ask the most important missing question next. Once the intended use/domain is identifiable, make the next unanswered intake question whether the user has research, notes, examples, SOPs, URLs, docs, prior specs, or workflow material to include, unless they already provided it or explicitly said none exists. Ask this before deeper operating-model, architecture, tool, or autonomy questions.

Multiple-choice options should be informed, request-specific suggestions, not a generic questionnaire. Infer likely operating patterns from the user's request and offer concrete choices for how the agent should work: no-build/reuse, runtime style, autonomy level, toolsets/data sources, workflow shape, handoffs, outputs, guardrails, and acceptance tests. Research/notes intake choices should be concrete too: paste notes now, name a local/wiki file, provide URLs/docs, describe an existing workflow, ask Agent Foundry to research first, or continue with no notes. If the user asks you to research how the agent should perform, or the domain is external, unfamiliar, regulated, specialized, or high-risk, do bounded research first: inspect local Hermes skills/docs before web/GitHub, then fold the best operating suggestions into the next multiple-choice layer. Use as many options as improve the outcome; default to 3-7 strong choices, allow more when the domain benefits from nuance, and treat more than 12 options as too many. If you have more than 12 viable suggestions, group them into categories or ask a narrowing question first. Mark a recommended/default option when helpful, but do not silently assume critical facts about scope, side effects, autonomy, sensitive data, or success criteria.

## Candidate spec review gate

Before making the final build/reuse/patch/no-build decision, draft a concise candidate spec and ask the user to review it. The spec should include intended use, target user/context, scope and exclusions, inputs/data/tools, user-supplied research/notes status, outputs, operating model, autonomy/greenlight gates, success criteria, v1/later split, and smallest smoke test. Treat the user's response as a gate: approve, amend, add research/notes, switch direction, or stop. You may include a provisional recommendation, but do not generate final artifacts or declare a final decision until the spec is reviewed or the user explicitly tells you to proceed without review.

## Classification decision tree

Classify every request before building:

| Classification | Use when | Output |
|---|---|---|
| No build | A prompt/checklist/one-off task solves it. | Recommendation only. |
| Skill | A reusable procedure inside an existing role is enough. | Skill draft and apply plan. |
| Existing-agent extension | A current profile/worker owns the domain. | Patch kit, not a new profile. |
| Local profile | Needs isolated memory/config/personality but not sharing. | Local profile build kit. |
| Profile distribution | Needs portable/shareable packaging. | Distribution build kit. |
| Workspace worker candidate | Needs durable team routing/lane/team awareness. | Workspace patch proposals. |
| Migration | Existing real-time agent should shift some work to staged ICM. | Non-destructive migration plan. |
| Research-first | External/regulated/unfamiliar/high-risk domain. | Bounded research notes and risks. |

## Stage workflow

For non-trivial work, create a build-kit or patch-kit directory with:

```text
00_brief/
01_fit_check/
02_research/
03_design/
04_generate/
05_validate/
06_apply_plan/
references/
output/
```

Use `templates/stage-context-template.md` for each stage contract.

## Required stage outputs

### 00_brief

- `brief.md` — user goal, assumptions, constraints, done criteria, greenlight gates, and user research/notes status.
- `candidate-spec.md` — reviewable spec drafted before final classification.
- `user-spec-review.md` — approval/amendment record or an explicit user instruction to proceed without review.

### 01_fit_check

- `fit-check.md` — existing surfaces inspected and classification.
- `reuse-bloat-verdict.md` — one of `reuse_existing`, `new_agent_justified`, `no_agent_needed`, `needs_user_choice`, `insufficient_intake`.
- `runtime-style-recommendation.md` — ICM, real-time/live, hybrid, or no new runtime.

### 02_research

Only when triggered. Outputs may include:

- `research-notes.md`
- `skill-candidates.md`
- `toolset-candidates.md`
- `mcp-server-candidates.md`
- `repo-shortlist.md`

Rules:

- Search local Hermes skills first.
- Prefer built-in Hermes toolsets before adding MCP.
- Treat GitHub/web results as candidates requiring verification.
- Include URL, maturity/activity hints, auth burden, read/write risk, install complexity, and verify-before-install notes.
- Do not install tools/MCP/skill taps during v1 staging.

### 03_design

- `blueprint.md` — role, scope, inputs, outputs, handoffs.
- `architecture-decision.md` — runtime decision and trade-offs.
- `guardrails.md` — autonomy level and hard approval gates.
- `observability-plan.md` when needed — how repeated/scheduled/multi-step agents record progress, failures, blockers, and status-review evidence.
- `existing-agent-migration.md` when migrating real-time responsibilities into ICM.

### 04_generate

Generate only staged artifacts, such as:

- `SOUL.md`
- `profile.yaml`
- `config.yaml`
- `skills/<agent>-core/SKILL.md`
- `distribution.yaml`
- `README.md`
- `.env.EXAMPLE`
- `.gitignore`
- patch proposals

For agents that may run repeatedly, run on a schedule, coordinate multi-step work, or be asked later how they are going, generated SOUL/skill/config drafts must include an observability/run-log section. Use `templates/observability-plan.md` as the default: local profile-scoped JSONL events plus an optional latest-status Markdown summary, no secrets/raw sensitive data, and a status-review workflow that inspects logs, validation outputs, blockers, and handoffs before answering.

### 05_validate

- `validation-report.md` with actual checks run.
- YAML/frontmatter parse evidence.
- Required-file evidence.
- Secret/user-data scan evidence.
- Observability evidence: `observability-plan.md` exists when needed, generated prompts mention run-log updates/status review, runtime log paths are outside distributions or gitignored, and smoke tests cover a synthetic status/failure review.
- Source URL and verify-before-install checks for candidates.

### 06_apply_plan

- `apply-plan.md` separating generated artifacts from gated follow-up actions.
- Patch files are proposals only until greenlit.

## Runtime style guide

Recommend one:

- **ICM-style** — sequential, reviewable, artifact-producing, audit-heavy.
- **Real-time/live** — interactive routing, monitoring, direct chat, event-driven decisions.
- **Hybrid** — live intake/control, staged delivery for non-trivial work.
- **No new runtime** — skill/checklist/tool/script/existing-agent patch is enough.

Agent Foundry itself should default to **hybrid with ICM-native core**.

## Greenlight gates

Explicit greenlight is required before:

- live profile creation/modification;
- Workspace routing/direct-lane/gateway changes;
- cron creation/modification;
- MCP install/config/auth;
- credential/auth/permission changes;
- external sends/publishing;
- GitHub commits/pushes unless repo work was explicitly requested;
- destructive/bulk changes;
- finance/email/account side effects.

## Verification checklist

Before reporting completion:

- Stage folders and `CONTEXT.md` contracts exist when a staged workflow was used.
- Required output files exist and are substantive.
- YAML/frontmatter parses.
- Secret-like content scan was run.
- Generated `.env.EXAMPLE` contains names/placeholders only.
- Candidate spec review was recorded before final decision or the user explicitly waived review.
- Apply plan makes greenlight gates explicit.
- Report exact commands/checks and their results.
