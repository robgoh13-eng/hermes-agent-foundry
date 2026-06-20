#!/usr/bin/env python3
"""Validate deterministic Agent Foundry fixture behavior contracts.

The fixture harness is intentionally LLM-free for CI. It checks that each
fixture encodes enough expected behavior to catch intake-gate contradictions,
classification drift, and accidental live-action expectations before a human or
future live-chat harness evaluates the same prompts against a model.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALLOWED_CLASSIFICATIONS = {
    "insufficient_intake",
    "no_build",
    "skill",
    "existing_agent_extension",
    "local_profile",
    "profile_distribution",
    "workspace_worker_candidate",
    "migration",
    "research_first",
}

ALLOWED_REUSE_VERDICTS = {
    "reuse_existing",
    "new_agent_justified",
    "no_agent_needed",
    "needs_user_choice",
    "insufficient_intake",
}

ALLOWED_RUNTIME_RECOMMENDATIONS = {
    "ICM-style",
    "real-time/live",
    "hybrid",
    "no new runtime",
    "not enough info",
}

REQUIRED_HEADINGS = [
    "User request",
    "Intake gate status",
    "Expected classification",
    "Expected runtime recommendation",
    "Expected reuse/bloat verdict",
    "Must include",
    "Must not do",
    "Forbidden live action expectation",
    "Smoke check",
]

FORBIDDEN_LIVE_ACTION_WORDS = [
    "apply live",
    "create live profile",
    "modify workspace routing",
    "create cron",
    "enable cron",
    "configure mcp credentials",
    "send externally",
    "publish externally",
    "post externally",
    "push to github",
    "tag release",
]

INTAKE_APPROVED_PATTERN = re.compile(
    r"research/notes\s+status:\s+(supplied|declined|not applicable).*"
    r"candidate spec review:\s+(approved|not applicable)",
    re.IGNORECASE | re.DOTALL,
)

INTAKE_MISSING_PATTERN = re.compile(
    r"missing|insufficient|must ask|not enough info|candidate spec review:\s+blocked",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Distribution/source root to validate. Defaults to this script's repo.",
    )
    return parser.parse_args()


def section_text(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    start = markdown.find(marker)
    if start == -1:
        return ""
    start += len(marker)
    next_heading = markdown.find("\n## ", start)
    return markdown[start : next_heading if next_heading != -1 else None].strip()


def fixture_paths(root: Path) -> list[Path]:
    return sorted((root / "fixtures" / "requests").glob("*.md"))


def check_fixture(path: Path, root: Path) -> list[str]:
    rel = path.relative_to(root)
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for heading in REQUIRED_HEADINGS:
        body = section_text(text, heading)
        if not body:
            errors.append(f"{rel} missing or empty section: ## {heading}")

    if errors:
        return errors

    classification = section_text(text, "Expected classification")
    runtime = section_text(text, "Expected runtime recommendation")
    verdict = section_text(text, "Expected reuse/bloat verdict")
    intake = section_text(text, "Intake gate status")
    must_not_do = section_text(text, "Must not do")
    forbidden_expectation = section_text(text, "Forbidden live action expectation")

    if classification not in ALLOWED_CLASSIFICATIONS:
        errors.append(f"{rel} invalid expected classification: {classification}")
    if runtime not in ALLOWED_RUNTIME_RECOMMENDATIONS:
        errors.append(f"{rel} invalid expected runtime recommendation: {runtime}")
    if verdict not in ALLOWED_REUSE_VERDICTS:
        errors.append(f"{rel} invalid expected reuse/bloat verdict: {verdict}")

    if classification == "insufficient_intake" or verdict == "insufficient_intake":
        if not INTAKE_MISSING_PATTERN.search(intake):
            errors.append(f"{rel} insufficient-intake fixture must explicitly say which intake gate is missing")
    else:
        if not INTAKE_APPROVED_PATTERN.search(intake):
            errors.append(
                f"{rel} final-decision fixture must record research/notes status and approved/not-applicable candidate spec review"
            )

    combined_forbidden = f"{must_not_do}\n{forbidden_expectation}".lower()
    if "no live action" not in combined_forbidden and "greenlight" not in combined_forbidden:
        errors.append(f"{rel} must explicitly forbid live actions or require greenlight")
    for phrase in FORBIDDEN_LIVE_ACTION_WORDS:
        if phrase in combined_forbidden and "do not" not in combined_forbidden and "without approval" not in combined_forbidden:
            errors.append(f"{rel} appears to permit forbidden live action phrase: {phrase}")

    return errors


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    fixtures = fixture_paths(root)
    errors: list[str] = []
    if not fixtures:
        errors.append("missing fixture directory or no fixture files under fixtures/requests")
    for path in fixtures:
        errors.extend(check_fixture(path, root))

    if errors:
        print("fixture_contracts_failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("fixture_contracts_ok")
    print(f"fixtures={len(fixtures)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
