---
title: Agent Foundry Profile Distribution
project_name: Agent Foundry
working_name: Agent Foundry
alternative_names: [SoulForge, ProfileForge, AgentSmithy, SwarmSmith, RoleForge]
type: project
status: active
review_state: prototype-built
live_project_usage: used
confidence: high
created: 2026-05-31
updated: 2026-06-01
tags: [hermes, profiles, profile-distributions, agents, workspace, guardrails]
sources:
  - https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
  - https://hermes-agent.nousresearch.com/docs/user-guide/profiles
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
  - https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profile-distributions.md
  - https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/profiles.md
  - https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/cron.md
  - https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md
  - https://github.com/modelcontextprotocol/servers
  - https://github.com/punkpeye/awesome-mcp-servers
  - https://github.com/wong2/awesome-mcp-servers
  - https://www.anthropic.com/research/building-effective-agents
  - https://developers.openai.com/cookbook/examples/partners/agentic_governance_guide/agentic_governance_cookbook
  - https://openai.github.io/openai-agents-python/guardrails/
  - https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
---

# Agent Foundry Profile Distribution

## One-line concept

**Agent Foundry** is an ICM-native Hermes profile distribution with a real-time conversational shell. It helps a user decide whether a requested agent should exist, then produces a reviewed, validated **agent build kit** or **existing-agent patch kit** for a Hermes profile, skill, profile distribution, migration, or Workspace worker candidate.

V1 is deliberately **not** an autonomous live-agent factory. The built prototype is an installable profile distribution that stages designs and apply plans. It does not create live profiles, modify Workspace routing, create cron jobs, configure MCP credentials, publish externally, or mutate existing agents unless the user gives a later explicit greenlight for that specific apply step.

Agent Foundry must also be **intake-strict**: if the user has not provided enough information to draft a meaningful goal or concrete improvement plan, it should not proceed into design or generation. It should ask one focused multiple-choice question at a time until the goal is satisfactory. Those choices should be informed operating suggestions based on the user's request and any bounded research needed to understand how that kind of agent should perform. Once the intended use/domain is identifiable, Agent Foundry should ask whether the user has research, notes, examples, SOPs, URLs, docs, prior specs, or workflow material to include. Before making its final build/reuse/patch/no-build decision, it should draft the candidate spec and have the user review, approve, or amend it.


## Current implementation status

Agent Foundry is a public-ready installable prototype, not a tagged release.

- Current version: `0.1.0`
- Repo visibility: public-ready
- Runtime posture: **ICM-native build core + real-time conversational shell**
- Included portable artifacts: `distribution.yaml`, `SOUL.md`, `config.yaml`, `skills/agent-foundry-core/SKILL.md`, seven ICM build-kit stage `CONTEXT.md` templates, portable docs, templates, validators, and CI fixture contracts.
- Required validation:
  - `python scripts/validate_distribution.py --mode source`
  - `python scripts/validate_fixture_contracts.py`
  - `python scripts/validate_distribution.py --mode kit --root templates/build-kit`
  - `python scripts/validate_distribution.py --mode kit --root fixtures/generated-kits/meeting-action-checklist`
  - `python scripts/smoke_profile_replay.py`
  - Optional installed-profile smoke replay: `python scripts/smoke_profile_replay.py --profile-root <installed-profile-root>`
  - `PYTHONPYCACHEPREFIX=/tmp/agent-foundry-pycache python -m py_compile scripts/validate_distribution.py scripts/validate_fixture_contracts.py scripts/smoke_profile_replay.py`
- Release posture: prototype-hardened with source, fixture, generated-kit, and deterministic smoke validation evidence; do not tag or publish until a reviewer approves the exact release step. The installed-profile smoke replay is read-only and optional unless profile readiness is claimed.

No live Workspace worker, cron job, MCP config, gateway lane, or existing-agent mutation is part of this distribution.


## Naming recommendation

Recommended name: **Agent Foundry**.

Why:

- Plain-English and immediately understandable: it builds agents.
- Works as a GitHub repo name: `agent-foundry` or `hermes-agent-foundry`.
- Broad enough for a future product, not limited to Hermes internals.
- Avoids overloading Hermes terms like `SOUL.md` in the public name while still supporting them internally.

Alternatives:

| Name | Feel | Notes |
|---|---|---|
| **SoulForge** | cooler / more brandable | Strong tie to `SOUL.md`; slightly less obvious to new users. |
| **ProfileForge** | Hermes-specific | Accurate but less exciting. |
| **SwarmSmith** | multi-agent themed | Good if Workspace swarm integration is the main pitch. |
| **RoleForge** | role-design focused | Good but less product-like. |
| **AgentSmithy** | playful | Memorable, but may feel gimmicky. |

Working title: **Agent Foundry — the Hermes agent-builder agent**.

## Problem statement

Building a useful Hermes specialist agent currently requires many coupled decisions across profile setup, `SOUL.md`, skills, config, cron, MCP, Workspace routing, guardrails, knowledge capture, verification, and team awareness.

A weak agent can duplicate an existing role, miss safety gates, leak secrets into a distribution, write vague instructions, create stale Workspace surfaces, run cron in the wrong profile, or ship as an unreviewed bundle that cannot be reproduced or safely shared.

The user wants this converted into an intelligent repeatable process shared as a Hermes profile distribution, then tested safely before any live Workspace integration.

## Product decision after grill

The original draft conflated three different products:

1. A portable Hermes profile distribution for agent design.
2. A live Workspace worker that edits this Workspace.
3. An autonomous factory that researches, builds, integrates, schedules, documents, and publishes other agents.

These have different blast radii. V1 should be **distribution-first and staging-only**.

### V1 thesis

Agent Foundry v1 is an **ICM-native Agent Build Kit / Patch Kit Generator** with a real-time conversational shell.

It may:

- interview the user;
- inspect existing local profiles, skills, docs, and Workspace roster read-only;
- classify the request as no-build, skill, existing-agent extension, local profile, distribution, or Workspace worker candidate;
- run bounded research when needed;
- generate a staged build kit in an explicitly scoped output directory;
- validate generated artifacts;
- produce an apply plan, patch proposals, handoff notes, and approval gates.

It must not in v1:

- write into a live Hermes profile directory;
- modify the user's live Hermes config file;
- modify a live Workspace checkout or routing configuration;
- modify existing agents' `SOUL.md`, skills, or profile configs;
- create or enable cron jobs;
- configure MCP servers or credentials;
- create Discord/gateway lanes;
- initialize, commit, push, or create GitHub repos unless repo work is explicitly scoped by the user;
- send or publish externally;
- perform destructive cleanup/backout operations.

Those are post-build application steps and require separate explicit greenlight.

## Source research summary

### Hermes profiles

Hermes profiles are separate Hermes home directories. Each profile has its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, state database, gateway state, and logs. Profiles create command aliases such as `coder chat` and are selected via `hermes -p <name>` or profile aliases.

Important constraints:

- Profiles isolate Hermes state, not the filesystem. A profile is **not** a sandbox.
- Tool execution starts from `terminal.cwd` or launch cwd, not automatically from the profile directory.
- `SOUL.md` guides the model but does not enforce hard boundaries.
- Profile changes normally take effect on a new session.
- If the profile should operate in a specific project, set explicit absolute `terminal.cwd` in that profile's `config.yaml`.
- `hermes update` updates Hermes code and bundled skills across profiles; `hermes profile update <name>` updates a profile distribution from its recorded git/local source.

### Hermes profile distributions

A profile distribution packages a whole Hermes agent as a git repository. It can include personality, skills, cron jobs, MCP connections, config, distribution metadata, and supporting files while excluding user data and secrets.

Typical repo shape:

```text
agent-foundry/
├── distribution.yaml
├── README.md
├── SOUL.md
├── config.yaml
├── skills/
├── cron/
├── scripts/              # only if cron/no_agent jobs need bundled scripts
├── templates/
├── docs/
├── mcp.json
├── .env.EXAMPLE
└── .gitignore
```

Distribution facts that matter for this spec:

- Install command: `hermes profile install <repo-or-path> --alias`.
- Local smoke install: `hermes profile install /path/to/agent-foundry --name agent-foundry-test --alias`.
- Update command: `hermes profile update agent-foundry`.
- Installed profiles are not ordinary source checkouts; updates re-clone from the recorded source.
- `config.yaml` is copied on fresh install but preserved on update unless `--force-config` is used.
- `distribution.yaml` needs at minimum `name`; other fields have defaults, but v1 should still emit explicit `version`, `description`, `hermes_requires`, `author`, `license`, `env_requires`, and ownership/exclusion notes.
- Use a simple single-comparator `hermes_requires`, such as `>=0.12.0`.
- Git tags are release markers; install/update currently tracks the recorded source/default branch unless Hermes adds ref pinning.
- Distribution installers exclude user data such as `.env`, `auth.json`, memories, sessions, logs, state DBs, caches, workspaces, local data, and related runtime files. The spec should treat this as installer protection, not as protection for the author's git history.
- Do not use symlinks in distribution repos.

### Secret and git-history risk

Distribution excludes help installers. They do **not** protect the author if they run `git add .` before `.gitignore` and secret scanning. Agent Foundry must generate and validate:

- `.gitignore` before any publishing handoff;
- a denylist report for `.env`, `auth.json`, `memories/`, `sessions/`, `state.db*`, `hermes_state.db`, `response_store.db*`, `logs/`, `*_cache/`, `local/`, `workspace/`, `profiles/`, `backups/`, `.worktrees/`, `node_modules/`, browser screenshots, checkpoints, sandboxes, history files, gateway state, pid/lock files, and similar runtime artifacts;
- a pre-publish checklist that includes `git status --short`, `git diff --cached --name-only`, and a secret-pattern scan.

### Hermes cron and profile pinning

Cron details to encode correctly:

- Cron jobs run in fresh sessions; prompts must be self-contained or attach skills/context explicitly.
- Cron tools are disabled inside cron runs to prevent recursive scheduling.
- Use `profile=<agent>` or `--profile <agent>` to pin runtime profile.
- Use `workdir=<absolute path>` or `--workdir <path>` separately for project context.
- A cron job may be stored in the scheduler profile's `cron/jobs.json` while executing under `profile: <agent>`. Verify both storage owner and runtime profile.
- Pinned profile scripts resolve under the runtime profile's `HERMES_HOME/scripts/`: for a named profile, `~/.hermes/profiles/<agent>/scripts/`; for default, `~/.hermes/scripts/`.
- If the named profile disappears, stale pins can fall back to the scheduler profile; verify the pinned profile exists before enabling/running.
- Script-only jobs should use `no_agent: true`; empty stdout means silent success.
- Use `deliver`/auto-delivery rather than `send_message` for ordinary scheduled output.
- Shipping `cron/` files in a distribution does not mean they are scheduled automatically after install; the installer must review and enable intentionally.
- Hermes has no general cron dry-run mode. Use list/inspect for read-only checks; manually trigger only after approval and only when side effects are safe.

### External agent-design research

Findings applied from external sources:

- Anthropic: successful agentic systems usually use simple, composable patterns; add complexity only when it demonstrably improves outcomes. Agent Foundry should prefer a build kit or workflow before a fully autonomous meta-agent.
- Microsoft Azure architecture guidance: choose the lowest level of complexity that reliably meets requirements. Multi-agent orchestration adds latency, cost, coordination overhead, and new failure modes.
- OpenAI governance guidance: governance should be built as infrastructure: policies as code, automated guardrails, tracing, evaluations, red-teaming, and feedback loops.
- OpenAI Agents SDK guardrails: guardrails need explicit workflow placement. Input/output guardrails are not enough for side-effecting tools; tool-call validation matters.
- ICM / Model Workspace Protocol: for sequential, human-reviewed, artifact-producing work, numbered folders, Markdown stage contracts, plain-text outputs, and local scripts can replace heavier orchestration. Its evidence base is practitioner-oriented rather than controlled performance science, so treat it as a workflow-design pattern, not proof that all agents should be filesystem pipelines.

Implication: V1 should optimize for staged artifacts, validation, and explicit apply gates, not broad live autonomy.

### ICM decision for Agent Foundry

Use ICM as Agent Foundry's **own build/research/design/generation/validation workflow**, not as a universal runtime requirement for every generated agent.

Recommended decision:

- **Yes**: Agent Foundry itself should be ICM-native for build work, with a real-time shell for intake/status/greenlight gates.
- **Yes**: Every generated build kit should contain ICM-like stage contracts and plain-text review artifacts so humans and other agents can inspect the reasoning.
- **No**: Do not require every generated agent to operate via ICM at runtime. Runtime architecture should still be chosen by fit check: skill, local profile, profile distribution, cron job, Workspace worker, MCP-backed operator, or simple prompt/checklist.
- **No**: Do not replace Hermes Workspace dispatch, cron, subagent delegation, or profile distributions with ICM. ICM should sit one layer above them as a transparent design/build/review process.

Why this fits:

- Agent creation is sequential: intake → fit check → research → design → generate → validate → apply plan.
- Human review between stages is valuable because bad agent specs create durable prompt/config/cron/workspace drift.
- Plain Markdown artifacts map cleanly to Hermes skills, `SOUL.md`, `distribution.yaml`, `.env.EXAMPLE`, verification reports, and wiki handoffs.
- Layer 3 / Layer 4 separation prevents a common failure: mixing durable agent rules with transient user requests and one-off build notes.
- It keeps V1 simple and auditable while preserving later handoff to Builder/KM/Orchestrator when live application is approved.

Where ICM should not be used:

- real-time or highly concurrent multi-agent coordination;
- production jobs needing queues, retries, telemetry, and robust recovery;
- complex automated branching where code/framework orchestration is clearer;
- quick one-shot agent tweaks where a staged workspace would be ceremony.

### Local Workspace pattern

The current Workspace agent system keeps each durable worker aligned across multiple surfaces:

- Hermes profile: `~/.hermes/profiles/<worker-id>/`
- Profile soul: `~/.hermes/profiles/<worker-id>/SOUL.md`
- Profile metadata: `~/.hermes/profiles/<worker-id>/profile.yaml`
- Profile config: `~/.hermes/profiles/<worker-id>/config.yaml`
- Role skill: `~/.hermes/skills/workspace-agents/<worker-id>-core/SKILL.md`
- Profile-local role skill: `~/.hermes/profiles/<worker-id>/skills/...`
- Workspace roster: `<workspace-root>/swarm.yaml`
- Workspace contract: `<workspace-root>/AGENTS.md`
- Direct lane prompts: `~/.hermes/config.yaml` where applicable
- Cron jobs pinned to the correct `profile`
- Durable wiki page: `<knowledge-root>/wiki/agents/<worker-id>.md`
- Operations map: `<knowledge-root>/wiki/operations/workspace-agent-operations.md`

Agent Foundry should encode these as checklists and patch proposals. V1 should not apply those patches directly.

## Product goals

1. Help users decide whether a new agent is justified.
2. Prevent duplicate or overlapping roles by checking existing agents, profiles, skills, docs, and distributions first.
3. Convert rough user ideas into explicit, testable profile/distribution artifacts.
4. Produce a staged build kit with guardrails, validation, and apply instructions.
5. Keep portability by default; Workspace-specific integration is optional and proposed, not assumed.
6. Make risky follow-up actions visible as approval gates before they happen.
7. Package Agent Foundry itself as a shareable profile distribution and verify local/remote smoke installs.
8. Minimize agent bloat by explicitly checking whether the request should update an existing agent, role skill, or routing rule before proposing a new agent.
9. Recommend whether each candidate should operate as an ICM-style staged workflow, a real-time/live agent, a hybrid, or no new agent at all, then show the trade-offs so the user can decide.
10. Support staged migration plans for existing agents, including converting a real-time/live agent into an ICM-style workflow when the job is mostly sequential, reviewable, and artifact-producing.

## Non-goals for v1

- Fully autonomous agent creation or live profile mutation.
- Live Workspace roster/direct-lane/source-of-truth edits.
- GitHub repo creation, commits, pushes, or public/private publishing.
- Cron job creation/enabling/modification.
- MCP credential or paid-service setup.
- Gateway/Discord lane creation.
- Updating existing agents' SOUL/skills/configs.
- Automatic durable wiki writes beyond this spec; output KM handoffs instead.
- Hard OS/container sandboxing.
- Sharing secrets, `.env`, auth, memories, sessions, logs, state DBs, or user data.

## Fit-check decision tree

Before proposing any build, classify the request:

| Classification | Use when | Output |
|---|---|---|
| **No build** | A prompt, checklist, or one-off task solves it. | Recommendation only. |
| **Skill** | Reusable procedure inside an existing role is enough. | `SKILL.md` draft and install/apply plan. |
| **Existing-agent extension** | An active worker already owns the domain. | Patch proposal for that worker, not a new profile. |
| **Local profile** | Needs isolated memory/config/personality but not sharing. | Local profile build kit and apply plan. |
| **Profile distribution** | Needs portable/shareable agent packaging. | Distribution build kit and local install test plan. |
| **Workspace worker candidate** | Needs durable routing/team-awareness in this Workspace. | Workspace patch proposals and greenlight gates. |
| **Needs research first** | Domain is external, regulated, safety-sensitive, or unfamiliar. | Bounded research notes and risk checklist. |

Default recommendation: prefer the simplest artifact that works. Do not create a profile when a skill or routing rule is enough.

### Anti-bloat existing-agent check

Agent Foundry must treat “new agent” as the expensive option. Before creating a new profile/distribution/worker candidate, it must ask or verify:

1. Is this really a new role, or is it a capability missing from an existing agent?
2. Which existing profile, Workspace worker, skill, cron job, MCP server, or routing rule already owns adjacent work?
3. Would a skill, prompt patch, tool/MCP addition, schedule, or handoff rule solve the request with less durable surface area?
4. If an existing agent should be edited, which exact surfaces would change: `SOUL.md`, role skill, profile config, toolsets, MCP config, cron, Workspace roster/routing, docs, tests, or wiki?
5. What bloat risk is avoided by reusing the existing agent, and what coupling risk is introduced by expanding it?

If the likely answer is “extend existing agent,” the output should be an **existing-agent patch kit**, not a new-agent build kit. It should still be staged and approval-gated; v1 drafts patch proposals only.

### Runtime architecture recommendation

After the fit check, Agent Foundry must recommend one operating style and show the difference for the user to decide:

| Style | Prefer when | Avoid when | Typical output |
|---|---|---|---|
| **ICM-style staged workflow** | Work is sequential, reviewable, artifact-producing, audit-heavy, or benefits from explicit stage contracts. | Work needs low-latency interaction, high concurrency, queues/retries, or constant event handling. | Numbered folders, `CONTEXT.md` contracts, review artifacts, apply plan. |
| **Real-time/live agent** | Work needs interactive routing, continuous monitoring, direct lane conversation, frequent tool use, or quick decisions. | Work mostly produces long-lived artifacts that should be reviewed before use. | Hermes profile/worker, live lane/routing, toolsets, optional cron, runtime guardrails. |
| **Hybrid** | Intake/triage is real-time but delivery should be staged and reviewable. | The workflow is simple enough for one mode. | Live profile or worker that writes ICM-style mission folders for non-trivial jobs. |
| **No new runtime** | A skill, checklist, cron script, MCP server, or existing-agent patch solves it. | Distinct memory/personality/routing is required. | Skill or patch kit, no profile. |

The report should state: “Recommended style: `<style>`,” then list user-visible differences in latency, auditability, operational overhead, context hygiene, failure recovery, required tools/MCP, and approval gates.

### Existing-agent realtime → ICM migration mode

Agent Foundry should be able to generate a migration plan for an existing real-time/live agent when ICM is a better fit. The migration plan must be non-destructive and staged:

1. Inventory current live surfaces: profile, `SOUL.md`, skills, config, cron, MCP, Workspace routing, direct lane, docs, wiki, and known jobs.
2. Identify which responsibilities stay real-time and which become staged ICM workflows.
3. Draft stage contracts and folder templates for the staged parts.
4. Draft patches to the agent's `SOUL.md`/skills telling it when to switch from direct handling to ICM mission folders.
5. Draft cron/routing changes only as proposals.
6. Define rollback: remove the ICM handoff rule and keep the previous live behavior.
7. Require explicit greenlight before applying any live profile, cron, MCP, Workspace, or gateway changes.

## Operating model

V1 follows an ICM-inspired staged workflow. The stage folders and contracts are part of the generated artifact, not a live profile:

```text
1. Intake with recommended defaults and a hard sufficiency gate
2. Anti-bloat / existing-agent verification
3. Read-only fit check
4. Runtime-style recommendation: ICM, real-time, hybrid, or no new runtime
5. Bounded web/GitHub research when triggered, including skill/tool/MCP candidates
6. Candidate spec draft and user review gate
7. Final classification decision
8. Build-kit or existing-agent patch-kit generation in staging directory
8. Artifact validation
9. Apply plan with gates
10. Optional handoff to Builder/KM/Orchestrator after approval
```

Recommended staging root:

```text
<staging-root>/<agent-name>/
```

This path is a generated-artifact workspace, not a live Hermes profile.

## Stage details

### Stage 1 — Intake grill

Ask enough questions to resolve the role, but offer them one at a time with multiple-choice defaults so the user does not have to answer everything in one bundle. This is a hard sufficiency gate: Agent Foundry must be able to write a well-drafted goal before it proceeds. If the goal is vague, weak, or missing critical answers, stop and ask the single highest-impact next question rather than creating a speculative build kit.

The choices in that question should be request-specific operating suggestions. Agent Foundry should infer or research plausible agent behavior patterns, then offer options such as reuse/no-build, real-time vs staged vs hybrid, autonomy level, data/tool access, handoff style, output format, guardrails, and smoke tests. It may use more than four choices when useful; default to 3-7, keep the list below 13, and group or narrow if there would be more than 12. Once the intended use/domain is identifiable, make the next unanswered question the research/notes question unless the user already supplied or declined such material; ask it before deeper operating-model, architecture, tool, or autonomy questions. Useful choices include paste notes now, point to a local/wiki file, provide URLs/docs, describe an existing workflow, ask Agent Foundry to research first, or continue with no notes.

Minimum goal contract:

- problem/opportunity and desired outcome;
- new agent vs existing-agent improvement vs skill/checklist vs migration vs no-build evaluation;
- target users and operating context;
- in-scope and out-of-scope tasks;
- expected inputs, data sources, tools, and sensitive data boundaries;
- user-owned research, notes, examples, SOPs, URLs, docs, prior specs, or an explicit `none yet`;
- expected outputs and quality bar;
- autonomy level, forbidden actions, and greenlight gates;
- v1 vs later scope;
- smallest meaningful smoke test or acceptance check.

For vague requests, use the full goal contract as an internal checklist, but ask only one question per turn. This applies across interfaces, not just Discord or any one chat gateway. For partially specified requests, ask the single most important missing high-impact question next. Prefer multiple-choice format, but do not force a four-choice limit: default to 3-7 strong suggestions, allow more for nuanced domains, and group or narrow before listing more than 12. Do not number questions as `1/N`, imply a fixed questionnaire length, or silently assume scope, side effects, autonomy, sensitive-data handling, or success criteria. After intake is sufficient, draft a candidate spec covering the goal, intended use, scope, inputs, research/notes status, outputs, operating model, guardrails, and smoke test. Ask the user to approve, amend, add research/notes, switch direction, or stop before final classification/build decisions.

Core questions:

1. What is the agent's primary job in one sentence?
2. Are we creating a new agent, editing an existing agent, or not sure yet?
3. Do you have research, notes, examples, SOPs, URLs, docs, prior specs, or workflow material that should shape the agent?
4. Which existing agent/profile/skill feels closest to this job?
4. Who uses this agent: just you, the Workspace team, clients, or public users?
5. What decisions should it make vs only recommend?
6. What inputs will it read: files, web, email, finance, repos, APIs, Discord, other?
7. What outputs should it produce: reports, code, tasks, drafts, data updates, messages?
8. Which actions are explicitly forbidden?
9. Which actions can it do autonomously without approval?
10. Which actions require greenlight every time?
11. Which toolsets and MCP servers does it need, and can it work without them?
12. Should it be ICM-style, real-time/live, hybrid, or should Agent Foundry recommend the style after fit check?
13. If it is an existing real-time agent, should any part be migrated to an ICM-style staged workflow?
14. Does it need schedules, gateway lanes, or Workspace routing?
15. Which existing agents should it hand off to or receive work from?
16. Should Agent Foundry search GitHub/web for matching skills, tool libraries, or MCP servers?
17. What is the smallest successful smoke test?
18. What is v1 vs later?
19. Should the output be no-build, skill, existing-agent patch, local profile, distribution, or Workspace worker candidate?

### Stage 2 — Read-only fit check

Inspect before proposing a new build:

- active Workspace roster;
- retired/support workers;
- local profiles;
- profile descriptions;
- role skills;
- existing profile distributions if available;
- Hermes skills that may already cover the need;
- relevant knowledgebase project/system/agent pages.

Report one classification from the decision tree before implementation. The report must include a **reuse/bloat verdict**:

- `reuse_existing`: patch an existing agent/skill/profile instead of creating a new one;
- `new_agent_justified`: the role is distinct enough to deserve a new profile/distribution/worker candidate;
- `no_agent_needed`: a checklist, prompt, direct tool use, or one-off task is enough;
- `needs_user_choice`: two or more options are genuinely close;
- `insufficient_intake`: the request is not ready for fit-check/build output yet and needs one focused question or candidate-spec review first.

Also report one runtime-style recommendation: ICM-style, real-time/live, hybrid, or no new runtime. If the user asked for a new agent but fit check suggests an existing-agent edit, explicitly ask/verify before drafting a new-agent build kit.

### Stage 3 — Bounded research

Research is required only when the role is external, regulated, safety-sensitive, operationally risky, unfamiliar, or likely to need specialized tools.

Bounded research policy:

- Prefer 3 to 5 high-quality sources.
- Capture source URLs and dates.
- Extract risks, best practices, tool/data requirements, failure modes, and tests.
- Keep research notes concise.
- Produce a KM handoff for durable capture unless the user explicitly asks Agent Foundry to edit the wiki.

Skill/tool/MCP discovery policy:

- When the role may benefit from reusable procedures, search local Hermes skills first, then web/GitHub for candidate `SKILL.md` repos, Hermes skill taps, or agent-skill repositories.
- When the role needs external systems, search current MCP server indexes and GitHub repos, including official/reference MCP servers and curated awesome-MCP lists.
- Also suggest built-in Hermes toolsets before MCP; do not recommend an MCP server where a built-in toolset already safely covers the need.
- Rank candidates by fit to the agent's mode of operation (MO): required capabilities, maturity/activity, auth burden, privacy/blast radius, install complexity, license, and whether read-only operation is possible.
- Treat web results as candidates, not truth. Include source URLs and note what must be verified before installation.
- Never install a skill tap, tool, package, or MCP server in v1; produce a recommendation and gated apply plan only.

Typical discovery outputs:

```text
02_research/skill-candidates.md
02_research/toolset-candidates.md
02_research/mcp-server-candidates.md
02_research/repo-shortlist.md
```

Seed sources discovered during spec review:

- Hermes skills can be shared as GitHub skill taps via `hermes skills tap add <owner/repo>`; candidate skill repos should be inspected before install.
- `modelcontextprotocol/servers` is the official/reference MCP server collection.
- `punkpeye/awesome-mcp-servers` and `wong2/awesome-mcp-servers` are broad curated MCP indexes useful for discovery, but each candidate still needs individual verification.

### Stage 4 — Guardrail and freedom-level design

Default for generated agents: **Level 1 — Drafter**.

| Level | Name | Agent may do | Requires greenlight |
|---|---|---|---|
| 0 | Observer | Read approved sources and report. | Any write, send, schedule, external side effect. |
| 1 | Drafter | Draft plans, replies, code, configs, patches, and build kits. | Applying writes outside staging; external sends. |
| 2 | Local Operator | Make scoped local reversible changes and run verification. | Deploy/push/publish, credentials, destructive/bulk changes. |
| 3 | Scheduled Operator | Run bounded scheduled jobs in its profile. | Creating/modifying cron, cloud writes, external sends, permissions. |
| 4 | Trusted Specialist | Execute approved classes of tasks inside a written policy. | Anything outside policy or high-risk categories. |

Universal hard gates:

- external send/publish/post/comment;
- email send/delete/archive/unsubscribe/mark read;
- payment, transfer, trade, account or subscription change;
- deploy, merge, push, release, package publish;
- destructive file/database/cloud changes;
- credential/auth/token/permission changes;
- password/secret generation, storage, transmission, or reveal;
- source-of-truth rewrites, large taxonomy changes, bulk deletes;
- cron/updater creation or modification;
- GitHub repo creation/commit/push;
- gateway/lane/bot setup;
- irreversible commitments or decisions.

### Stage 5 — Build-kit generation

Generate staged artifacts only:

```text
agent-build-kits/<agent-name>/
├── 00_brief/
│   ├── CONTEXT.md
│   └── brief.md
├── 01_fit_check/
│   ├── CONTEXT.md
│   ├── fit-check.md
│   ├── reuse-bloat-verdict.md
│   └── runtime-style-recommendation.md
├── 02_research/
│   ├── CONTEXT.md
│   ├── research-notes.md           # optional / only when triggered
│   ├── skill-candidates.md         # optional / web+GitHub candidates
│   ├── toolset-candidates.md       # optional / built-in Hermes toolsets
│   ├── mcp-server-candidates.md    # optional / MCP candidates
│   └── repo-shortlist.md           # optional / source URLs and verification notes
├── 03_design/
│   ├── CONTEXT.md
│   ├── blueprint.md
│   ├── architecture-decision.md    # ICM vs real-time vs hybrid vs no runtime
│   ├── observability-plan.md       # progress/failure/status review design when needed
│   ├── existing-agent-migration.md # optional / realtime → ICM patch plan
│   └── guardrails.md
├── 04_generate/
│   ├── CONTEXT.md
│   ├── SOUL.md
│   ├── profile.yaml
│   ├── config.yaml
│   ├── skills/<agent>-core/SKILL.md
│   ├── distribution.yaml
│   ├── README.md
│   ├── .env.EXAMPLE
│   └── .gitignore
├── 05_validate/
│   ├── CONTEXT.md
│   ├── verification.md
│   └── validation-report.md
├── 06_apply_plan/
│   ├── CONTEXT.md
│   ├── apply-plan.md
│   └── workspace-patches/
│       ├── orchestrator-routing.patch.md
│       ├── operations-map.patch.md
│       └── agent-doc.patch.md
├── references/                    # stable reusable context for this build
└── output/                        # final packaged review bundle
```

Each stage `CONTEXT.md` must define goal, inputs, process, outputs, allowed files/tools, forbidden actions, and verification. Stable guidance belongs in `references/`; run-specific artifacts belong in numbered stage folders or `output/`.

### Stage 6 — Validation

Validation before handoff:

- YAML/frontmatter parses for generated files.
- `distribution.yaml` includes explicit metadata and simple `hermes_requires`.
- `.env.EXAMPLE` contains only names/placeholders, no secrets.
- `.gitignore` and exclusion report cover known runtime/user-data paths.
- No generated artifact includes raw secrets, tokens, auth files, sessions, logs, or state DBs.
- Skill frontmatter and Markdown structure parse.
- `reuse-bloat-verdict.md` explicitly states whether an existing agent/skill/profile should be reused.
- `runtime-style-recommendation.md` compares ICM-style, real-time/live, hybrid, and no-runtime options where relevant.
- `observability-plan.md` exists for repeated, scheduled, multi-step, or status-reporting agents; it keeps runtime logs outside distributions or gitignored, forbids secrets/raw sensitive data, and defines how the agent reviews progress and failures when asked.
- Web/GitHub skill/tool/MCP recommendations include source URLs and “verify before install” notes.
- MCP recommendations identify required auth/env vars, read/write risk, and whether built-in Hermes tools can replace them.
- Existing-agent migration plans include rollback and do not apply live changes.
- Workspace patch files are proposals, not applied changes.
- Apply plan lists exact commands and approval gates.
- Verification plan includes a throwaway local install when distribution packaging is approved.

### Stage 7 — Apply plan and handoff

The output report must separate safe generated artifacts from gated follow-up actions:

- **Generated now:** staged build kit paths and validation results.
- **Requires Builder greenlight:** creating a live profile, copying files into `~/.hermes/profiles`, running Hermes CLI mutations, applying Workspace patches.
- **Requires KM greenlight:** durable wiki/index/operations edits if not explicitly scoped.
- **Requires Orchestrator greenlight:** adding routing/team-awareness for a live worker.
- **Requires GitHub greenlight:** repo initialization, commits, pushes, tags, releases.
- **Requires Ops/security greenlight:** cron, MCP credentials, gateway/lane setup, external sends, permissions.

## Current Agent Foundry v0.1 prompt contract

```md
You are Agent Foundry, a Hermes profile-distribution architect and agent-design steward.

Mission: help the user decide whether a requested agent should exist and produce a reviewed, validated agent build kit or existing-agent patch kit. You are ICM-native for build work with a real-time conversational shell for intake, status, and greenlight gates. Prefer the simplest artifact that works: no-build, skill, existing-agent extension, local profile, profile distribution, or Workspace worker candidate. Avoid agent bloat by verifying reuse before proposing a new runtime.

Operating loop:
1. Intake: ask focused questions and offer recommended defaults, including whether this is a new agent or an edit to an existing agent.
2. Anti-bloat fit check: inspect existing profiles, skills, Workspace roster, cron jobs, MCP/tool coverage, and knowledge docs read-only.
3. Reuse verdict: state whether to reuse/patch an existing agent, build a new one, avoid a new runtime, or ask the user to choose.
4. Runtime style: recommend ICM-style, real-time/live, hybrid, or no new runtime; highlight the differences and let the user decide when trade-offs are close.
5. Research: when triggered, perform bounded sourced research. Search web/GitHub for candidate skills, built-in Hermes toolsets, and MCP servers that fit the agent's mode of operation, but do not install anything.
6. Classify: explain whether this should be no-build, skill, existing-agent extension, local profile, distribution, Workspace worker candidate, migration, or research-first.
7. Design: draft stage contracts plus SOUL.md, role skill, config, env requirements, tool/MCP needs, handoff rules, guardrail matrix, runtime architecture decision, observability/run-log plan, migration plan if relevant, and verification plan.
8. Generate: write only to the explicit ICM-style staging/build-kit directory.
9. Validate: parse YAML/frontmatter, check exclusions, scan for secret-like content, verify stage outputs, verify skill/tool/MCP candidate citations, and report evidence.
10. Handoff: produce an apply plan with exact greenlight gates before any live profile, Workspace, cron, MCP, gateway, GitHub, existing-agent edit, or external-send action.

Default safety posture: generated agents start as Level 1 Drafter unless the user explicitly grants more freedom.

Never include `.env`, `auth.json`, memories, sessions, logs, state DBs, raw secrets, private user data, or runtime caches in a distribution or generated artifact.
```

### Observability and run-log requirement

Agent Foundry should include a logging/observability system in generated agents when they may run repeatedly, on a schedule, across multiple steps, or whenever the owner expects to ask later “how is it going?” or “where is it failing?”

V1 default is local-first and low overhead:

- create `03_design/observability-plan.md` from `templates/observability-plan.md`;
- recommend profile-local runtime files such as `${HERMES_HOME}/local/agent-runs/<agent-id>.jsonl` and `${HERMES_HOME}/local/agent-runs/<agent-id>-latest.md`;
- require generated prompts/skills to append concise events for phase, status, summary, non-sensitive input/output references, failure kind, next action, and greenlight needs;
- define failure kinds including user-input blocker, validation failure, tool failure, missing auth, timeout, rate limit, external service, and unexpected error;
- make “how is it going?” answers inspect latest status, recent run events, failed validation outputs, blockers, and handoffs before using less structured session context;
- keep runtime logs out of distributions, commits, and public reports except synthetic fixtures.

Observability must not become surveillance or data dumping. Logs should summarize and reference evidence, not copy raw secrets, OAuth tokens, credentials, raw private messages, raw financial transactions, unnecessary personal data, or full sensitive payloads.

## Agent Blueprint Questionnaire template

### A. Identity

- Working name?
- One-sentence mission?
- Who is the user/customer?
- What personality should it have?
- What should it never sound like?

### B. Scope

- What tasks should it own?
- What tasks should it refuse?
- What tasks should it hand off?
- What is v1 vs later?
- Is this a new role, or should an existing agent/skill/profile be edited?
- Which existing agent is closest, and what bloat would a new agent create?

### B2. Runtime style

- Should this operate as ICM-style staged workflow, real-time/live agent, hybrid, or no new runtime?
- If Agent Foundry should recommend the style, what matters most: latency, auditability, low overhead, context hygiene, recovery, or user review?
- For existing real-time agents, should any responsibilities be migrated to ICM folders and stage contracts?
- What behavior should remain real-time even if some work becomes ICM-style?

### C. Inputs and tools

- What data can it read?
- What tools/toolsets does it need?
- Does it need web, terminal, files, browser, MCP, Discord, email, finance, GitHub, cron?
- Can built-in Hermes toolsets cover the need before adding MCP?
- Should Agent Foundry search web/GitHub for skill taps, `SKILL.md` repos, tool libraries, or MCP servers that fit the role?
- What credentials would be needed, and can it operate without them?

### D. Outputs

- What should it produce?
- Should it write files, create tasks, send messages, update docs, run scripts, or only draft?
- What format should final reports use?

### E. Team awareness

- Which existing agents should it know about?
- Which agents should know about it?
- What are the handoff triggers?
- What context should be passed in each handoff?

### F. Guardrails

- Choose freedom level: Observer, Drafter, Local Operator, Scheduled Operator, Trusted Specialist.
- What actions always need approval?
- What actions are allowed autonomously?
- What data is sensitive?
- What logs/artifacts must not contain secrets?

### F2. Observability and status review

- Will this agent run repeatedly, on a schedule, or across multi-step work?
- When asked “how is it going?”, what evidence should it inspect first?
- Where should local runtime logs/status summaries live, and how are they excluded from distributions/git?
- What failure categories should it report?
- What should be logged as a reference only rather than copied into logs?

### G. Scheduling and persistence

- Does it need cron jobs?
- What cadence?
- Where should outputs be delivered?
- Should successful runs be silent?
- Which profile should each job run under?
- Are cron prompts self-contained?
- Are scripts located under the runtime profile's `scripts/` directory?

### H. Distribution

- Local-only or GitHub distribution?
- Source distribution channel and release cadence?
- Required env vars for `.env.EXAMPLE`?
- License and author?
- Versioning and release policy?
- Which files are distribution-owned vs user-owned?

### I. Verification

- What is the smallest successful smoke test?
- What fixtures should prove fit-check behavior?
- What files/surfaces must be inspected after build?
- What would make you trust the agent?
- What cleanup/backout plan is needed?

## Implementation phases and status

### Phase 0 — Spec review — complete

- Review this spec.
- Keep final name as Agent Foundry unless user chooses otherwise.
- Confirm V1 scope: staged build-kit generator, not live Workspace worker.
- Confirm default freedom level: Level 1 Drafter.
- Confirm staging root.

### Phase 1 — Build-kit generator prototype — complete

- Create a safe prototype directory, not a live profile.
- Draft `SOUL.md` for Agent Foundry.
- Draft `agent-foundry-core` skill.
- Add ICM-style stage contracts for brief, fit-check, research, design, generation, validation, and apply-plan stages.
- Add templates for questionnaire, fit-check, reuse/bloat verdict, runtime-style recommendation, guardrail matrix, build plan, existing-agent patch kit, realtime-to-ICM migration plan, validation report, apply plan, Workspace patch proposals, and stage `CONTEXT.md` files.
- Add skill/tool/MCP discovery templates that record web/GitHub source URLs, candidate ranking, auth burden, read/write risk, and verify-before-install notes.
- Configure minimal safe tool assumptions: file, terminal, web, skills, session_search; no cronjob writes in v1.
- Smoke test against synthetic agent requests without touching live Workspace surfaces.

Example future profile command, only after approval:

```bash
hermes profile create agent-foundry \
  --description "Designs reviewed Hermes agent build kits and profile-distribution artifacts."
agent-foundry config set terminal.cwd <staging-root>
hermes profile show agent-foundry
```

### Phase 2 — Distribution packaging — complete for v0.1.0

- Add explicit `distribution.yaml`.
- Add `README.md`, `.env.EXAMPLE`, `.gitignore`, and `docs/`.
- Ensure no user-owned data is included.
- Install from local directory into a throwaway profile after approval:

```bash
hermes profile install /path/to/agent-foundry --name agent-foundry-test --alias
hermes profile info agent-foundry-test
hermes -p agent-foundry-test chat
hermes profile delete agent-foundry-test --yes
```

- GitHub repo has been initialized and pushed after user-scoped repo work.
- Tag `v0.1.0` remains pending until the next trial confirms behavior beyond install/chat smoke tests.

### Phase 3 — Workspace integration, post-v0.1

Only if the user wants Agent Foundry as a live worker:

- Apply a reviewed profile under `~/.hermes/profiles/agent-foundry/`.
- Add Agent Foundry to Workspace roster only after approval.
- Update orchestrator routing so agent-building requests route to Agent Foundry.
- Update operations map and agent index.
- Add direct lane prompt only if it gets a Discord lane.
- Verify Workspace UI/API surfaces.

### Audit hardening follow-up — 2026-06-01

An external repository audit found the architecture strong but the validator, fixtures, concrete generated-output templates, CI, and status wording under-hardened for release. The remediation added static enforcement for all stage contexts, required generated-output templates, fixture shape, forbidden source runtime/user-data paths, richer observability schema/retention guidance, stronger anti-bloat evidence capture, generated-kit output validation, and GitHub Actions validation. A non-risky synthetic meeting-action-checklist staged build trial now provides repo-contained generated-kit fixture evidence and validates as a generated kit without touching installed profiles. A deterministic smoke replay harness now checks fixture prompts against source policy anchors and can run read-only against an installed profile with `--profile-root <path>`; tag/push/release still requires explicit reviewer or user approval.

### Phase 4 — Real build trial — completed locally

- Used Agent Foundry's staged contracts to design one small non-risky skill/checklist candidate using synthetic meeting-action material.
- Required review gate before any file writes outside staging.
- Verified generated stage outputs, validation report, gated apply plan, secret/user-data hygiene, and no installed-profile changes.
- Revised validation to inspect generated-kit outputs when present.

## Fixture-based evaluation plan

V1 should be tested against at least three fixtures:

1. **Obvious duplicate:** user asks for a finance-analysis agent when `finance` already exists. Expected: classify as existing-agent extension or skill, not new profile.
2. **Skill-not-profile:** user asks for a repeatable checklist/procedure. Expected: draft skill build kit, no profile.
3. **Justified distribution:** user asks for a portable research assistant with unique env/tool needs. Expected: distribution build kit and local install test plan.
4. **Workspace worker candidate:** user asks for a durable team member with routing/lane needs. Expected: staged artifacts plus Workspace patch proposals, no live edits.
5. **Realtime vs ICM choice:** user asks for an agent that produces long reviewable reports. Expected: recommend ICM-style or hybrid, explain differences from real-time, and let user decide if trade-offs are close.
6. **Realtime-to-ICM migration:** user asks to make an existing direct-lane worker less chatty and more auditable. Expected: produce a non-destructive migration plan and patch proposals, not live edits.
7. **External tool discovery:** user asks for an agent with unfamiliar external integrations. Expected: search local skills plus web/GitHub for candidate skills, built-in toolsets, and MCP servers; cite sources and mark candidates verify-before-install.
8. **Vague request:** user says only “make me an agent.” Expected: say `I need a sharper goal before I build`, ask one multiple-choice intake question, and do not generate artifacts.

## Acceptance criteria

Current v0.1 status: criteria 1, 4, 5, 7, 8, 10, 11, 14, 15, 16, 17, and the distribution install/chat smoke-test portion of 18 have initial proof from the profile-distribution prototype. The deterministic fixture suite is contract/static, and `scripts/smoke_profile_replay.py` adds a commandable read-only smoke replay that can target source policy anchors or an installed profile path without external credentials.

Agent Foundry v1 is successful when:

1. It completes structured intake and records assumptions/defaults.
2. It classifies requests as no-build, skill, existing-agent extension, local profile, distribution, Workspace worker candidate, migration, or research-first.
3. It performs a read-only fit check against profiles, skills, Workspace roster, cron jobs, tool/MCP coverage, and relevant docs.
4. It produces a reuse/bloat verdict before proposing a new agent.
5. It recommends ICM-style, real-time/live, hybrid, or no new runtime and highlights trade-offs for the user.
6. It can produce an existing-agent realtime-to-ICM migration plan without applying live changes.
7. It generates a complete ICM-style staged build kit or existing-agent patch kit under a non-live output directory.
8. Every numbered stage has a `CONTEXT.md` defining goal, inputs, process, outputs, allowed scope, forbidden actions, and verification.
9. Stable reference material is separated from run-specific artifacts.
10. Generated YAML/frontmatter parses.
11. Generated distribution manifest includes name, version, description, env requirements, Hermes compatibility, and ownership/exclusion notes.
12. Generated `.gitignore` and exclusion report prevent obvious secret/user-data paths.
13. It produces a guardrail matrix with default Level 1 Drafter posture.
14. It suggests local skills, GitHub/web skill candidates, built-in Hermes toolsets, and MCP server candidates when useful, with source URLs and verify-before-install notes.
15. It produces an apply plan listing exact actions requiring approval.
16. It does not modify live profiles, Workspace files, cron, MCP, gateway config, GitHub, or existing agents in v1.
17. It passes the fixture suite above.
18. If distribution packaging is approved, it can install into a throwaway profile and verify with `hermes profile info`, `hermes -p <test> cron list`, and a safe chat smoke test.
19. It refuses to proceed from vague or under-specified requests and asks enough questions to complete the minimum goal contract before generating artifacts.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Agent duplicates an existing role | Mandatory fit check, reuse/bloat verdict, and explicit existing-agent verification before build. |
| Agent over-promises autonomy | Freedom-level matrix; default Level 1 Drafter. |
| Meta-agent blast radius is too large | V1 writes only to staging/build-kit directory. |
| Profile mistaken for sandbox | Explicit warning; set `terminal.cwd`; do not rely on SOUL for enforcement. |
| Secrets leak into distribution | `.gitignore`, denylist, secret scan, inclusion/exclusion report before publish. |
| Git history contains secrets | Create ignore/scan before first commit; never rely only on installer excludes. |
| Workspace routing drifts | Generate patch proposals; apply only after review and UI/API verification. |
| Cron job runs under wrong profile | Verify storage owner, runtime `profile`, profile existence, script path, and prompt self-containment. |
| Distribution cron files assumed active | State that installers must review/enable; no auto scheduling assumption. |
| Knowledgebase pollution | Produce KM handoff unless wiki edits are explicitly in scope. |
| User fatigue from too many questions | Offer defaults and progressive disclosure. |
| Over-complex multi-agent design | Prefer simplest artifact that works; add complexity only when evidence supports it. |
| ICM ceremony slows small agent tweaks | Use ICM only for non-trivial, repeatable, reviewable builds; answer or patch directly for small one-shot changes. |
| ICM mistaken for runtime architecture | State that ICM governs the build/review process; generated agents choose runtime architecture through fit check. |
| Real-time agent converted to ICM loses responsiveness | Split responsibilities: keep urgent/interactive routing real-time and move only reviewable artifact work to ICM. |
| Web-sourced skills/tools/MCP servers are stale or unsafe | Treat as candidates only; cite sources, rank risk, verify repo activity/license/auth/read-write scope, and require approval before install. |
| MCP added where built-in tools suffice | Check built-in Hermes toolsets first and prefer lower-blast-radius native tools. |

## Open review questions

1. Confirm V1 scope: staged build-kit generator only?
2. Staging root: user-selected `<staging-root>` or another explicit generated-artifact directory?
3. Should Agent Foundry be a live Workspace worker later, or remain an on-demand distribution?
4. Should v1 generate patch proposal files only, or may it create throwaway local test profiles after approval?
5. Should GitHub publishing be handled by Builder/GitHub workflow rather than Agent Foundry itself?
6. Which agents must know about it on day one: orchestrator only, or all active workers?
7. Should the first real trial build a toy agent, a skill-only artifact, an existing-agent patch, or a realtime-to-ICM migration plan?
8. Confirm the ICM boundary: stage the agent-building process with ICM, but do not force generated agents to use ICM at runtime?
9. When should Agent Foundry stop and ask the user to choose between ICM-style, real-time/live, hybrid, or no-runtime if the trade-off is close?
10. Which GitHub skill taps, MCP indexes, or tool registries are trusted enough to search by default?

## Cleanup / backout plan

If the project is abandoned before live use:

- Remove staged build kits under the chosen staging root if no longer useful.
- Remove or archive any local `agent-foundry` profile if one was later approved and created.
- Remove or archive the source repository if created, after confirming no useful templates remain.
- Remove Agent Foundry from Workspace roster and direct-lane config if it was later added.
- Remove or pause any cron jobs pinned to `agent-foundry`.
- Keep this spec as historical/proposed unless superseded.
- Do not remove unrelated agent docs or existing Workspace operations maps.

If implemented and later superseded:

- Mark this page `live_project_usage: superseded`.
- Link the replacement project/distribution.
- Preserve non-secret lessons learned and guardrail templates.

## Related

- [[wiki/projects/index]]
- [[wiki/projects/workspace-agent-system]]
- [[wiki/systems/hermes-profiles]]
- [[wiki/operations/workspace-agent-operations]]
- [[wiki/agents/orchestrator]]
- [[wiki/agents/builder]]
- [[wiki/agents/km-agent]]
- [[wiki/concepts/interpretable-context-methodology]]
- [[wiki/runbooks/wiki-lint]]
