
# Using Agent Foundry

## Install locally for testing

From this repo:

```bash
hermes profile install github.com/<owner>/hermes-agent-foundry --name agent-foundry-test -y
# or install from a local clone:
# hermes profile install /path/to/agent-foundry --name agent-foundry-test -y
hermes profile info agent-foundry-test
hermes -p agent-foundry-test chat -q "Design a small skill-only agent build kit for a weekly reading checklist. Do not write outside a temp staging directory."
```

Delete the test profile when done:

```bash
hermes profile delete agent-foundry-test --yes
```

## Expected first behavior

Agent Foundry should not immediately create a new agent. It should first check whether the request is specific enough to support a meaningful build or improvement. If the goal is weak, it should ask more questions instead of guessing.

Minimum expected behavior for vague prompts:

1. Say `I need a sharper goal before I build`.
2. Ask one focused multiple-choice question at a time in every interface, using the goal contract internally to cover outcome, new-vs-existing surface, users/context, scope, inputs/tools/data, outputs/quality bar, autonomy/greenlight gates, v1/later split, and smoke test over successive turns. Do not label questions as `1/N` or imply a fixed questionnaire length.
3. Make the choices request-specific operating suggestions. If the user asks for research on how the agent should perform, or the domain needs external/specialized judgment, research local Hermes skills/docs first and web/GitHub when needed, then include the best suggestions in the multiple-choice layer. Use enough choices to improve the outcome; more than 12 is too many, so group or narrow first.
4. Do not produce a build kit, patch kit, profile draft, or skill draft until those answers are satisfactory.

Once the goal is sufficient, it should classify the request, produce/recommend a reuse-bloat verdict, and recommend a runtime style.

## Safe test prompts

```text
make me an agent
```

Expected: ask one multiple-choice intake question and do not proceed to generation.

```text
I want a finance analysis agent that summarizes my spending.
```

Expected: existing-agent extension or skill, because this Workspace already has finance capability.

```text
I want a portable research assistant for reading academic PDFs and creating literature review notes.
```

Expected: likely profile distribution build kit, with research/tool/MCP candidate notes.

```text
Make my current email agent less chatty and more auditable.
```

Expected: realtime-to-ICM migration plan, not live edits.
```
