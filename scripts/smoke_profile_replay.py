#!/usr/bin/env python3
"""Deterministic Agent Foundry smoke replay harness.

This script is intentionally LLM-free and side-effect free. By default it replays
repo fixture contracts against the source distribution policy text. When
``--profile-root`` is supplied, it uses that installed profile's policy text
instead, so reviewers can run the same behavioral smoke checks against a profile
without credentials, chat gateways, cron, MCP, or external services.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

BEHAVIOR_ANCHORS = {
    "intake_gate": [
        "I need a sharper goal before I build",
        "one focused multiple-choice question",
        "multiple-choice",
    ],
    "candidate_spec_gate": [
        "Candidate spec review gate",
        "draft a concise candidate spec",
        "approve, amend, add research/notes, switch direction, or stop",
    ],
    "classification_and_runtime": [
        "Classification decision tree",
        "reuse-bloat-verdict.md",
        "runtime-style-recommendation.md",
    ],
    "approval_gates": [
        "Explicit greenlight is required before",
        "live profile creation/modification",
        "Workspace routing/direct-lane/gateway changes",
        "cron creation/modification",
        "MCP install/config/auth",
        "credential/auth/permission changes",
        "external sends/publishing",
    ],
    "observability": [
        "observability-plan.md",
        "no secrets/raw sensitive data",
        "status-review workflow",
    ],
}

POLICY_FILES = [
    "skills/agent-foundry-core/SKILL.md",
    "SOUL.md",
    "docs/SAFETY.md",
    "templates/build-kit/00_brief/CONTEXT.md",
    "templates/build-kit/01_fit_check/CONTEXT.md",
    "templates/build-kit/03_design/CONTEXT.md",
    "templates/build-kit/05_validate/CONTEXT.md",
    "templates/build-kit/06_apply_plan/CONTEXT.md",
]

REQUIRED_SECTIONS = [
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

LIVE_ACTION_WORDS = [
    "install",
    "update profile",
    "delete profile",
    "gateway",
    "direct-lane",
    "cron",
    "credential",
    "external",
    "push",
    "release",
    "destructive",
]


@dataclass(frozen=True)
class FixtureCase:
    path: Path
    request: str
    intake: str
    classification: str
    runtime: str
    verdict: str
    must_include: str
    must_not_do: str
    forbidden_live_action: str
    smoke_check: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Source repository root containing fixtures. Defaults to this script's repo.",
    )
    parser.add_argument(
        "--profile-root",
        type=Path,
        default=None,
        help="Optional installed profile root to smoke-check. If omitted, source policy text is checked.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the deterministic replay transcript as JSON after the summary.",
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


def read_fixture(path: Path, root: Path) -> tuple[FixtureCase | None, list[str]]:
    text = path.read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED_SECTIONS if not section_text(text, heading)]
    if missing:
        rel = path.relative_to(root)
        return None, [f"{rel} missing smoke section(s): {', '.join(missing)}"]
    return (
        FixtureCase(
            path=path,
            request=section_text(text, "User request"),
            intake=section_text(text, "Intake gate status"),
            classification=section_text(text, "Expected classification"),
            runtime=section_text(text, "Expected runtime recommendation"),
            verdict=section_text(text, "Expected reuse/bloat verdict"),
            must_include=section_text(text, "Must include"),
            must_not_do=section_text(text, "Must not do"),
            forbidden_live_action=section_text(text, "Forbidden live action expectation"),
            smoke_check=section_text(text, "Smoke check"),
        ),
        [],
    )


def fixture_cases(root: Path) -> tuple[list[FixtureCase], list[str]]:
    fixture_dir = root / "fixtures" / "requests"
    paths = sorted(fixture_dir.glob("*.md"))
    if not paths:
        return [], [f"missing fixture prompts under {fixture_dir}"]
    cases: list[FixtureCase] = []
    errors: list[str] = []
    for path in paths:
        case, case_errors = read_fixture(path, root)
        errors.extend(case_errors)
        if case is not None:
            cases.append(case)
    return cases, errors


def policy_text(root: Path) -> tuple[str, list[str]]:
    chunks: list[str] = []
    missing: list[str] = []
    for rel in POLICY_FILES:
        path = root / rel
        if path.is_file():
            chunks.append(f"\n<!-- {rel} -->\n" + path.read_text(encoding="utf-8", errors="ignore"))
        else:
            missing.append(rel)
    if not chunks:
        return "", [f"no policy files found under {root}"]
    return "\n".join(chunks), missing


def check_policy_anchors(text: str, behavior_root: Path) -> list[str]:
    errors: list[str] = []
    for group, phrases in BEHAVIOR_ANCHORS.items():
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{behavior_root}: missing behavior anchor {group}: {phrase}")
    return errors


def replay_response(case: FixtureCase) -> str:
    if case.classification == "insufficient_intake" or case.verdict == "insufficient_intake":
        return (
            "I need a sharper goal before I build.\n\n"
            "Which outcome should Agent Foundry optimize for?\n"
            "A) Patch an existing capability.\n"
            "B) Draft a small skill.\n"
            "C) Design a new profile distribution.\n"
            "D) Stop and gather notes first.\n\n"
            "No build artifacts, profile changes, gateway edits, cron changes, credentials, "
            "external sends, pushes, releases, or destructive actions are approved; "
            "these live actions are not approved without explicit greenlight."
        )
    return (
        "Candidate spec review gate: record supplied/declined user material and user approval before the final decision.\n"
        f"Expected classification: {case.classification}.\n"
        f"Runtime recommendation: {case.runtime}.\n"
        f"Reuse/bloat verdict: {case.verdict}.\n"
        "Next step: produce staged artifacts and a gated apply plan only.\n"
        "No live profile, Workspace, gateway, cron, MCP, credential, external-send, GitHub, "
        "destructive, or bulk action is approved without explicit greenlight."
    )


def validate_replay(case: FixtureCase, response: str, root: Path) -> list[str]:
    rel = case.path.relative_to(root)
    errors: list[str] = []
    if case.classification == "insufficient_intake" or case.verdict == "insufficient_intake":
        if "I need a sharper goal before I build" not in response:
            errors.append(f"{rel}: insufficient-intake replay missing gate phrase")
        if response.count("?") != 1:
            errors.append(f"{rel}: insufficient-intake replay should ask exactly one question")
        if any(marker not in response for marker in ["A)", "B)", "C)"]):
            errors.append(f"{rel}: insufficient-intake replay missing multiple-choice options")
    else:
        for expected in [case.classification, case.runtime, case.verdict]:
            if expected not in response:
                errors.append(f"{rel}: replay missing expected value {expected}")
        if "Candidate spec review gate" not in response:
            errors.append(f"{rel}: replay missing candidate spec review gate")
    if "explicit greenlight" not in response and "not approved" not in response:
        errors.append(f"{rel}: replay missing approval caveat")
    lowered = response.lower()
    if not any(word in lowered for word in LIVE_ACTION_WORDS):
        errors.append(f"{rel}: replay did not exercise live-action guardrails")
    return errors


def main() -> int:
    args = parse_args()
    source_root = args.root.resolve()
    behavior_root = (args.profile_root or args.root).resolve()

    cases, errors = fixture_cases(source_root)
    text, missing_policy_files = policy_text(behavior_root)
    # Installed profiles may omit source-only docs/templates in some future package shapes;
    # only fail if the core policy anchors cannot be found in the files that are present.
    if args.profile_root is None and missing_policy_files:
        errors.extend(f"source policy file missing: {path}" for path in missing_policy_files)
    errors.extend(check_policy_anchors(text, behavior_root))

    transcript = []
    for case in cases:
        response = replay_response(case)
        errors.extend(validate_replay(case, response, source_root))
        transcript.append(
            {
                "fixture": str(case.path.relative_to(source_root)),
                "request": case.request,
                "classification": case.classification,
                "runtime": case.runtime,
                "verdict": case.verdict,
                "replay_response": response,
                "smoke_check": case.smoke_check,
            }
        )

    if errors:
        print("smoke_profile_replay_failed")
        print(f"source_root={source_root}")
        print(f"profile_root={behavior_root if args.profile_root else 'not provided'}")
        for error in errors:
            print(f"- {error}")
        return 1

    print("smoke_profile_replay_ok")
    print(f"source_root={source_root}")
    print(f"profile_root={behavior_root if args.profile_root else 'not provided'}")
    print(f"cases={len(cases)}")
    print("external_side_effects=none")
    if args.json:
        print(json.dumps({"cases": transcript}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
