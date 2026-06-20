# Decisions

## D1 — V1 is staging-only

Agent Foundry v1 is an Agent Build Kit Generator. It may write staged artifacts and patch proposals, but it does not directly mutate live Hermes profiles, Workspace routing, cron jobs, MCP credentials/config, gateway lanes, GitHub releases, or existing agents.

## D2 — Anti-bloat comes before building

Every request must verify whether an existing agent, profile, skill, cron job, MCP server, or routing rule already covers the capability. If yes, Agent Foundry produces an existing-agent patch kit rather than a new-agent build kit.

## D3 — ICM is the build workflow, not a universal runtime

Agent Foundry uses ICM-style folders and `CONTEXT.md` contracts for the agent-building process. Generated agents are not forced to run as ICM pipelines. Their runtime style is selected by fit check.

## D4 — Runtime style must be explicit

Each candidate gets one recommendation:

- ICM-style staged workflow
- real-time/live agent
- hybrid
- no new runtime

The recommendation must explain trade-offs in latency, auditability, overhead, context hygiene, recovery, tools/MCP, and approval gates.

## D5 — External tool discovery is recommendation-only

Agent Foundry can search local skills, GitHub skill repos/taps, tool libraries, and MCP server indexes. It may recommend candidates with citations and risk notes, but it must not install or configure them without explicit greenlight.

## D6 — Agent Foundry is ICM-native with a real-time shell

Agent Foundry may design ICM-style agents, real-time agents, hybrid agents, or no-runtime solutions. Agent Foundry itself should use a hybrid posture: conversational for intake, status, and greenlight gates; ICM-native for the actual build/research/design/generation/validation/apply-plan workflow.

## D7 — Intake sufficiency is a hard gate

Agent Foundry must not proceed from a vague query into build-kit, patch-kit, profile, skill, or migration artifact generation. It first needs enough answers to write a well-drafted goal and make something meaningful or improve something that already exists.

If critical answers are missing, it should ask one focused multiple-choice question at a time rather than silently filling gaps. This is a platform-neutral intake style, not a Discord-specific behavior. For vague requests, use the goal contract as an internal checklist but expose only the single highest-impact next question. Do not label questions as `1/N` or imply a fixed questionnaire length.

## D8 — Intake choices should be informed operating suggestions

Agent Foundry should not present multiple choice as a generic form. It should infer plausible operating models from the user's request and offer concrete choices for how the agent should work: no-build/reuse, runtime style, autonomy level, toolsets/data, workflow shape, handoffs, outputs, guardrails, and acceptance tests. If the user asks for research on how the agent should perform, or the domain is unfamiliar, external, regulated, specialized, or high-risk, Agent Foundry should do bounded local-skill/docs-first research before asking the next question, then fold the best suggestions into that multiple-choice layer.

There is no fixed four-option limit. Use as many options as improve the outcome; default to 3-7 strong choices, allow more for nuanced domains, and treat more than 12 options as too much. If more than 12 viable suggestions exist, group them or ask a narrowing question. A recommended/default option is allowed, but facts about scope, side effects, autonomy, sensitive data, and success criteria must not be guessed. Once the intended use/domain is identifiable, Agent Foundry should ask whether the user has research, notes, examples, SOPs, URLs, docs, prior specs, or workflow material that should shape the agent, unless already supplied or explicitly declined. Before the final build/reuse/patch/no-build decision, Agent Foundry must draft a candidate spec and ask the user to review, approve, amend, add notes/research, or switch direction.

## D9 — Generated agents need reviewable runtime evidence when they run repeatedly

For repeated, scheduled, multi-step, or status-reporting agents, Agent Foundry should include an observability/run-log plan in the build kit. The default is local-first, profile-scoped runtime evidence: concise JSONL events plus an optional latest-status Markdown summary. Generated agents should be able to answer “how is it going?” and “where is it failing?” by inspecting those logs, validation outputs, blockers, and handoffs before relying on conversational memory.

Runtime logs are user data, not distribution artifacts. They must be excluded from generated repos/distributions or explicitly gitignored, and they must summarize or reference sensitive evidence rather than copying secrets, credentials, raw private messages, raw financial transactions, unnecessary personal data, or full sensitive payloads.
