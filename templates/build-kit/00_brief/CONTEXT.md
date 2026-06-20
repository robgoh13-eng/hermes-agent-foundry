
# Stage: 00 Brief

## Goal
Capture a well-drafted requested agent outcome, assumptions, constraints, approval gates, and done criteria. If the available request is not sufficient to make something meaningful or improve something that already exists, stop and ask more questions before later stages proceed.

## Inputs
- User request
- Existing project/spec context

## Process
1. Restate the requested capability.
2. Check intake sufficiency: problem/outcome, new-vs-existing surface, users/context, scope/out-of-scope, inputs/tools/data, user research/notes/examples status, outputs/quality bar, autonomy, hard greenlight gates, v1/later split, and smallest smoke test.
3. If the intended use/domain is identifiable and the user has not supplied or declined supporting material, make the next unanswered question whether they have research, notes, examples, SOPs, URLs, docs, prior specs, or workflow material to include. Ask it before deeper operating-model, architecture, tool, or autonomy questions.
4. If any critical answer is missing or weak, ask one focused multiple-choice question instead of guessing. This applies in every interface, not just chat gateways. Use the full contract as an internal checklist for vague requests; ask the single highest-impact next question. Choices should be request-specific operating suggestions based on the user's request and any bounded research needed. Use enough suggestions to improve the outcome; more than 12 is too many, so group or narrow first. Do not number questions as `1/N` or imply a fixed questionnaire length.
5. Draft a candidate spec and ask the user to review, approve, amend, add research/notes, switch direction, or stop before final classification/build decisions.
6. Record assumptions only after they are explicit, low-risk, and marked as assumptions.
7. Identify sensitive data and hard approval gates.
8. Define the smallest useful test.

## Outputs
- `brief.md`
- `candidate-spec.md`
- `user-spec-review.md`
- If intake is insufficient: `I need a sharper goal before I build` plus one multiple-choice intake question instead of downstream build artifacts.

## Allowed files/tools
- Build-kit directory only
- Read-only inspection tools as needed

## Forbidden actions
- No live profile, Workspace, cron, MCP, gateway, GitHub, or external-send changes.

## Verification
- `brief.md`, `candidate-spec.md`, and `user-spec-review.md` exist and include goal, constraints, done criteria, research/notes status, completed intake-sufficiency checklist, and user review record; or an insufficient-intake question exists and later stages have not proceeded.
