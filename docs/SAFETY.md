# Safety and Guardrails

## Default posture

Generated agents start at **Level 1 — Drafter** unless explicitly approved otherwise.

## Hard approval gates

Require explicit greenlight before:

- external send, publish, post, or comment
- email send/delete/archive/unsubscribe/mark-read
- payment, transfer, trade, account, or subscription change
- deploy, merge, push, release, or package publish
- destructive file/database/cloud changes
- credential/auth/token/permission changes
- password/secret generation, storage, transmission, or reveal
- source-of-truth rewrites, taxonomy changes, or bulk deletes
- cron/updater creation or modification
- GitHub repo creation, commit, push, tag, release, or package publish
- gateway/lane/bot setup
- irreversible commitments or decisions

## Secret and user-data exclusions

Never include `.env`, `auth.json`, memories, sessions, logs, state DBs, response stores, caches, local runtime data, profile directories, backups, browser screenshots, checkpoints, sandboxes, pid/lock files, or raw private user data in a distribution.

Approval is per action and per destination. A greenlight for one repository,
branch, release, profile, credential, or external service does not carry over to
future writes or publishes; ask for a fresh explicit greenlight before each such
action.
