# Meeting Action Checklist Agent Brief

## Goal

Create a synthetic, non-live skill-style assistant that turns pasted meeting notes into a reviewable action checklist with owners, due dates, confidence notes, and follow-up questions.

## Scope

### In scope

- Accept pasted sample meeting notes supplied by the user.
- Extract candidate actions, decisions, blockers, and open questions.
- Produce a Markdown checklist and a concise handoff summary.
- Keep the implementation as staged generated artifacts only until explicitly approved.

### Out of scope

- Reading private calendars, email, chat systems, drives, or task managers.
- Creating tasks in external systems.
- Editing any installed Hermes profile, gateway route, cron job, credential, or Workspace worker.

## User research / notes status

The user supplied synthetic example notes and declined external research for the fixture. No private notes, credentials, or production data are present.

## Autonomy and greenlight gates

Autonomous work is limited to drafting staged files and running deterministic local validation. Explicit approval is required before installing a skill, updating a profile, changing routing, scheduling jobs, connecting integrations, pushing to a remote, or sending anything externally.

## Done criteria / smoke test

Given a sanitized three-paragraph meeting note sample, the generated assistant returns at least three checklist items with owner, due date or `unknown`, status, confidence, and one clarification question, while refusing to create external tasks without approval.
