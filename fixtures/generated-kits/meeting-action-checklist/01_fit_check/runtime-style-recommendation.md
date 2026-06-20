# Runtime Style Recommendation

## Recommendation

`ICM-style` staged workflow.

## Trade-offs

- ICM-style improves auditability and lets the user review checklist drafts before any action.
- Real-time/live behavior would add unnecessary operational overhead for pasted-note transformation.
- Hybrid behavior is unnecessary because no live event listener or external task creation is in scope.
- No new runtime is viable if this remains a prompt pattern; a skill is useful only if the checklist schema should be reusable.

## Why this style

The assistant should produce deterministic Markdown from supplied text and stop at a review handoff. The design intentionally avoids external credentials, background jobs, and live side effects.
