#!/usr/bin/env python3
"""Validate the Agent Foundry profile distribution repo.

The validator is dependency-light and supports three roots:

- ``--mode source``: full source checkout/distribution validation.
- ``--mode kit``: generated build-kit validation for stage contracts.
- ``--mode installed``: installed profile validation with runtime-data hygiene relaxed.
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("ERROR: PyYAML is required for validation", file=sys.stderr)
    raise SystemExit(2) from exc

STAGE_NAMES = [
    "00_brief",
    "01_fit_check",
    "02_research",
    "03_design",
    "04_generate",
    "05_validate",
    "06_apply_plan",
]

SOURCE_STAGE_CONTEXTS = [f"templates/build-kit/{stage}/CONTEXT.md" for stage in STAGE_NAMES]
KIT_STAGE_CONTEXTS = [f"{stage}/CONTEXT.md" for stage in STAGE_NAMES]

REQUIRED_STAGE_HEADINGS = [
    "## Goal",
    "## Inputs",
    "## Process",
    "## Outputs",
    "## Allowed files/tools",
    "## Forbidden actions",
    "## Verification",
]

REQUIRED_OUTPUT_TEMPLATES = [
    "templates/brief.md",
    "templates/candidate-spec.md",
    "templates/user-spec-review.md",
    "templates/fit-check.md",
    "templates/blueprint.md",
    "templates/architecture-decision.md",
    "templates/guardrails.md",
    "templates/validation-report.md",
    "templates/apply-plan.md",
    "templates/existing-agent-patch-kit.md",
    "templates/workspace-patch-proposal.md",
]

REQUIRED_FIXTURES = [
    "fixtures/requests/duplicate-finance-agent.md",
    "fixtures/requests/skill-only-checklist.md",
    "fixtures/requests/justified-distribution-research-assistant.md",
    "fixtures/requests/workspace-worker-candidate.md",
    "fixtures/requests/realtime-vs-icm-report-agent.md",
    "fixtures/requests/realtime-to-icm-email.md",
    "fixtures/requests/external-tool-discovery.md",
    "fixtures/requests/vague-agent-request.md",
    "fixtures/requests/specable-request.md",
    "fixtures/requests/observability-status-agent.md",
]

REQUIRED_FIXTURE_HEADINGS = [
    "## User request",
    "## Intake gate status",
    "## Expected classification",
    "## Expected runtime recommendation",
    "## Expected reuse/bloat verdict",
    "## Must include",
    "## Must not do",
    "## Forbidden live action expectation",
    "## Smoke check",
]

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

BASE_REQUIRED_FILES = [
    "distribution.yaml",
    "LICENSE",
    "SOUL.md",
    "config.yaml",
    "README.md",
    ".env.EXAMPLE",
    ".gitignore",
    "docs/SAFETY.md",
    "docs/VALIDATION.md",
    "docs/ROADMAP.md",
    "docs/SPEC.md",
    "docs/DECISIONS.md",
    "scripts/validate_distribution.py",
    "scripts/validate_fixture_contracts.py",
    "skills/agent-foundry-core/SKILL.md",
    "templates/stage-context-template.md",
    "templates/reuse-bloat-verdict.md",
    "templates/runtime-style-recommendation.md",
    "templates/observability-plan.md",
    "templates/skill-tool-mcp-candidates.md",
    "templates/existing-agent-migration.md",
    *SOURCE_STAGE_CONTEXTS,
    *REQUIRED_OUTPUT_TEMPLATES,
    *REQUIRED_FIXTURES,
]

REQUIRED_INSTALLED_FILES = [path for path in BASE_REQUIRED_FILES if path not in set(REQUIRED_FIXTURES)]
REQUIRED_SOURCE_FILES = [*BASE_REQUIRED_FILES]

REQUIRED_KIT_FILES = [
    *KIT_STAGE_CONTEXTS,
]

REQUIRED_GENERATED_KIT_OUTPUTS = [
    "00_brief/brief.md",
    "00_brief/candidate-spec.md",
    "00_brief/user-spec-review.md",
    "01_fit_check/fit-check.md",
    "01_fit_check/reuse-bloat-verdict.md",
    "01_fit_check/runtime-style-recommendation.md",
    "03_design/blueprint.md",
    "03_design/architecture-decision.md",
    "03_design/guardrails.md",
    "04_generate/generated-artifacts.md",
    "05_validate/validation-report.md",
    "06_apply_plan/apply-plan.md",
]

KIT_OUTPUT_HEADINGS = {
    "00_brief/brief.md": ["## Goal", "## Scope", "## User research / notes status", "## Autonomy and greenlight gates", "## Done criteria / smoke test"],
    "00_brief/candidate-spec.md": ["## Intended use", "## Proposed classification", "## User-owned material", "## Operating model", "## Review prompt"],
    "00_brief/user-spec-review.md": ["## Review outcome", "## User decision", "## Remaining amendments"],
    "01_fit_check/fit-check.md": ["## Existing surfaces inspected", "## Classification", "## Rationale"],
    "01_fit_check/reuse-bloat-verdict.md": ["## Verdict", "## Existing surface reuse evidence", "## New surface justification"],
    "01_fit_check/runtime-style-recommendation.md": ["## Recommendation", "## Trade-offs", "## Why this style"],
    "03_design/blueprint.md": ["## Role", "## Inputs", "## Outputs", "## Handoffs"],
    "03_design/architecture-decision.md": ["## Decision", "## Alternatives considered", "## Consequences"],
    "03_design/guardrails.md": ["## Autonomy level", "## Hard approval gates", "## Forbidden actions"],
    "04_generate/generated-artifacts.md": ["## Generated artifacts", "## Files intentionally not generated", "## Validation notes"],
    "05_validate/validation-report.md": ["## Summary", "## Commands/checks run", "## Approvals still required", "## Cleanup/backout notes"],
    "06_apply_plan/apply-plan.md": ["## Purpose", "## Generated artifacts", "## Approval gates", "## Backout plan"],
}

REQUIRED_SOUL_PHRASES = [
    "ICM-native",
    "Anti-bloat fit check",
    "Runtime style decision",
    "Observability and run logs",
    "Hard gates",
]

REQUIRED_SKILL_PHRASES = [
    "Classification decision tree",
    "reuse-bloat-verdict.md",
    "runtime-style-recommendation.md",
    "observability-plan.md",
    "Agent Foundry itself should default to **hybrid with ICM-native core**",
]

REQUIRED_DOC_PHRASES = {
    "docs/SAFETY.md": [
        "Hard approval gates",
        "Secret and user-data exclusions",
        "credential/auth/token/permission changes",
    ],
    "docs/VALIDATION.md": [
        "Fixture suite",
        "Intake sufficiency",
        "deterministic fixture contract harness",
    ],
}

REQUIRED_OBSERVABILITY_PHRASES = {
    "templates/observability-plan.md": [
        "schema_version",
        "event_id",
        "Retention and rotation",
        "failure_kind",
        "Privacy and safety rules",
        "Review workflow",
    ],
    "fixtures/requests/observability-status-agent.md": [
        "observability-plan.md",
        "local run-log updates",
        "synthetic run-log",
    ],
}

FORBIDDEN_SOURCE_NAMES = {
    ".env",
    "auth.json",
    "memories",
    "sessions",
    "logs",
    "local",
    "workspace",
    "profiles",
    "backups",
    "checkpoints",
    "sandboxes",
    ".worktrees",
    "node_modules",
    "__pycache__",
    "state.db",
    "hermes_state.db",
    "response_store.db",
}

FORBIDDEN_SOURCE_PATTERNS = [
    ".env.*",
    "*_cache",
    "cache",
    "state.db*",
    "response_store.db*",
    "*.sqlite",
    "*.sqlite3",
    "*.db",
    "*.pid",
    "*.lock",
    "*.pyc",
]

SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s#<]+"),
]

SECRET_SCAN_SKIPPED_DIRS = {
    ".git",
    "__pycache__",
    "bin",
    "local",
    "logs",
    "profiles",
    "workspace",
}

ALLOWED_SECRET_WORD_CONTEXT = [
    "raw tokens",
    "API keys",
    "passwords",
    "Secret/user-data",
    "secret-like",
    "auth/token/permission",
    "tokens, API keys",
    "names/placeholders only",
]

PORTABLE_DOCS = [
    "README.md",
    "docs/SPEC.md",
    "docs/DECISIONS.md",
    "docs/SAFETY.md",
    "docs/VALIDATION.md",
    "docs/ROADMAP.md",
    "docs/USAGE.md",
]

PORTABLE_DOC_FORBIDDEN_PATTERNS = [
    re.compile(r"/home/[A-Za-z0-9_.-]+"),
    re.compile(r"github\.com/[A-Za-z0-9_.-]+/agent-foundry"),
    re.compile(r"Repository visibility:\s*private", re.IGNORECASE),
    re.compile(r"Repo visibility:\s*private", re.IGNORECASE),
    re.compile(r"private installable prototype", re.IGNORECASE),
    re.compile(r"approved private runtime", re.IGNORECASE),
    re.compile(r"private repo", re.IGNORECASE),
    re.compile(r"Latest pushed implementation commit", re.IGNORECASE),
    re.compile(r"local checkout", re.IGNORECASE),
]

NON_PUBLIC_LICENSE_VALUES = {"", "private", "proprietary", "all rights reserved"}


@dataclass(frozen=True)
class ValidationContext:
    root: Path
    mode: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--mode", choices=["source", "kit", "installed"], default="source")
    return parser.parse_args()


def read(ctx: ValidationContext, path: str) -> str:
    return (ctx.root / path).read_text(encoding="utf-8")


def generated_kit_output_present(ctx: ValidationContext) -> bool:
    return any((ctx.root / path).is_file() for path in REQUIRED_GENERATED_KIT_OUTPUTS)


def check_required_files(ctx: ValidationContext) -> list[str]:
    if ctx.mode == "kit":
        required = list(kit_stage_contexts(ctx))
        if generated_kit_output_present(ctx):
            required.extend(REQUIRED_GENERATED_KIT_OUTPUTS)
        return [path for path in required if not (ctx.root / path).is_file()]
    required_files = REQUIRED_INSTALLED_FILES if ctx.mode == "installed" else REQUIRED_SOURCE_FILES
    return [path for path in required_files if not (ctx.root / path).is_file()]


def missing_headings(ctx: ValidationContext, path: str, headings: list[str]) -> list[str]:
    text = read(ctx, path)
    return [heading for heading in headings if heading not in text]


def kit_stage_contexts(ctx: ValidationContext) -> list[str]:
    direct = [path for path in KIT_STAGE_CONTEXTS if (ctx.root / path).is_file()]
    if direct:
        return KIT_STAGE_CONTEXTS
    return SOURCE_STAGE_CONTEXTS


def source_stage_contexts(ctx: ValidationContext) -> list[str]:
    return kit_stage_contexts(ctx) if ctx.mode == "kit" else SOURCE_STAGE_CONTEXTS


def check_stage_contexts(ctx: ValidationContext) -> list[str]:
    errors: list[str] = []
    for path in source_stage_contexts(ctx):
        if not (ctx.root / path).is_file():
            continue
        for heading in missing_headings(ctx, path, REQUIRED_STAGE_HEADINGS):
            errors.append(f"{path} missing heading: {heading}")
    return errors


def check_kit_outputs(ctx: ValidationContext) -> list[str]:
    if ctx.mode != "kit" or not generated_kit_output_present(ctx):
        return []
    errors: list[str] = []
    for path, headings in KIT_OUTPUT_HEADINGS.items():
        if not (ctx.root / path).is_file():
            continue
        for heading in missing_headings(ctx, path, headings):
            errors.append(f"{path} missing heading: {heading}")
        for heading in headings:
            if not section_text(read(ctx, path), heading):
                errors.append(f"{path} has empty section: {heading}")
    return errors


def section_text(markdown: str, heading: str) -> str:
    start = markdown.find(heading)
    if start == -1:
        return ""
    start += len(heading)
    next_heading = markdown.find("\n## ", start)
    if next_heading == -1:
        return markdown[start:].strip()
    return markdown[start:next_heading].strip()


def check_fixture_contracts(ctx: ValidationContext) -> list[str]:
    if ctx.mode in {"kit", "installed"}:
        return []
    errors: list[str] = []
    for path in REQUIRED_FIXTURES:
        if not (ctx.root / path).is_file():
            continue
        text = read(ctx, path)
        missing = missing_headings(ctx, path, REQUIRED_FIXTURE_HEADINGS)
        for heading in missing:
            errors.append(f"{path} missing heading: {heading}")
        if missing:
            continue

        empty_sections = []
        for heading in REQUIRED_FIXTURE_HEADINGS:
            if not section_text(text, heading):
                errors.append(f"{path} has empty section: {heading}")
                empty_sections.append(heading)
        if empty_sections:
            continue

        classification = section_text(text, "## Expected classification")
        if classification not in ALLOWED_CLASSIFICATIONS:
            errors.append(f"{path} invalid expected classification: {classification}")

        runtime = section_text(text, "## Expected runtime recommendation")
        if runtime not in ALLOWED_RUNTIME_RECOMMENDATIONS:
            errors.append(f"{path} invalid expected runtime recommendation: {runtime}")

        verdict = section_text(text, "## Expected reuse/bloat verdict")
        if verdict not in ALLOWED_REUSE_VERDICTS:
            errors.append(f"{path} invalid expected reuse/bloat verdict: {verdict}")
    return errors


def is_forbidden_source_path(ctx: ValidationContext, path: Path) -> bool:
    rel = path.relative_to(ctx.root)
    if rel.parts and rel.parts[0] == ".git":
        return False
    if path.name == ".env.EXAMPLE":
        return False
    if any(part in FORBIDDEN_SOURCE_NAMES for part in rel.parts):
        return True
    return any(fnmatch.fnmatch(path.name, pattern) or path.match(f"**/{pattern}") for pattern in FORBIDDEN_SOURCE_PATTERNS)


def check_forbidden_source_paths(ctx: ValidationContext) -> list[str]:
    """Fail source repos that contain runtime/user-data/build-artifact paths."""
    if ctx.mode != "source":
        return []
    if not (ctx.root / ".git").exists():
        return []

    findings: list[str] = []
    for candidate in ctx.root.rglob("*"):
        if is_forbidden_source_path(ctx, candidate):
            findings.append(f"forbidden source path present: {candidate.relative_to(ctx.root)}")
    return sorted(set(findings))


def check_forbidden_kit_paths(ctx: ValidationContext) -> list[str]:
    """Fail generated kits that accidentally contain runtime/user-data artifacts."""
    if ctx.mode != "kit":
        return []
    findings: list[str] = []
    for candidate in ctx.root.rglob("*"):
        if is_forbidden_source_path(ctx, candidate):
            findings.append(f"forbidden kit path present: {candidate.relative_to(ctx.root)}")
    return sorted(set(findings))


def check_yaml(ctx: ValidationContext) -> list[str]:
    if ctx.mode == "kit":
        return []
    errors: list[str] = []
    for path in ["distribution.yaml", "config.yaml"]:
        try:
            data = yaml.safe_load(read(ctx, path))
        except Exception as exc:  # noqa: BLE001 - validation reports raw parse errors
            errors.append(f"{path}: YAML parse failed: {exc}")
            continue
        if path == "distribution.yaml":
            for key in ["name", "version", "description", "hermes_requires", "author", "license"]:
                if not data or key not in data:
                    errors.append(f"distribution.yaml missing {key}")
            if data:
                license_value = str(data.get("license", "")).strip().lower()
                if license_value in NON_PUBLIC_LICENSE_VALUES:
                    errors.append("distribution.yaml license must be public-compatible before sharing")
                author_value = str(data.get("author", ""))
                if "/" in author_value or "Workspace" in author_value:
                    errors.append("distribution.yaml author must be public, generic, and non-personal")
    return errors


def distribution_manifest(ctx: ValidationContext) -> dict:
    if not (ctx.root / "distribution.yaml").is_file():
        return {}
    data = yaml.safe_load(read(ctx, "distribution.yaml"))
    return data or {}


def check_distribution_ownership(ctx: ValidationContext) -> list[str]:
    if ctx.mode == "kit":
        return []
    data = distribution_manifest(ctx)
    owned = data.get("distribution_owned", []) if isinstance(data, dict) else []
    errors: list[str] = []
    if "docs/" in owned or "docs" in owned:
        errors.append("distribution.yaml must not own docs/ wholesale; list portable docs explicitly")
    for required_doc in PORTABLE_DOCS:
        if required_doc not in owned:
            errors.append(f"distribution.yaml distribution_owned missing portable doc: {required_doc}")
    for entry in owned:
        if str(entry).startswith("docs/internal"):
            errors.append(f"distribution.yaml must not own internal/private doc: {entry}")
    return errors


def check_skill_frontmatter(ctx: ValidationContext) -> list[str]:
    if ctx.mode == "kit":
        return []
    text = read(ctx, "skills/agent-foundry-core/SKILL.md")
    if not text.startswith("---\n"):
        return ["skills/agent-foundry-core/SKILL.md missing YAML frontmatter"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return ["skills/agent-foundry-core/SKILL.md frontmatter not closed"]
    try:
        data = yaml.safe_load(text[4:end])
    except Exception as exc:  # noqa: BLE001
        return [f"skills/agent-foundry-core/SKILL.md frontmatter parse failed: {exc}"]
    for key in ["name", "description", "version"]:
        if key not in data:
            return [f"skills/agent-foundry-core/SKILL.md frontmatter missing {key}"]
    errors: list[str] = []
    license_value = str(data.get("license", "")).strip().lower()
    if license_value in NON_PUBLIC_LICENSE_VALUES:
        errors.append("skills/agent-foundry-core/SKILL.md license must be public-compatible before sharing")
    author_value = str(data.get("author", ""))
    if "/" in author_value or "Workspace" in author_value:
        errors.append("skills/agent-foundry-core/SKILL.md author must be public, generic, and non-personal")
    return errors


def check_content(ctx: ValidationContext) -> list[str]:
    if ctx.mode == "kit":
        return []
    errors: list[str] = []
    soul = read(ctx, "SOUL.md")
    skill = read(ctx, "skills/agent-foundry-core/SKILL.md")
    for phrase in REQUIRED_SOUL_PHRASES:
        if phrase not in soul:
            errors.append(f"SOUL.md missing phrase: {phrase}")
    for phrase in REQUIRED_SKILL_PHRASES:
        if phrase not in skill:
            errors.append(f"agent-foundry-core skill missing phrase: {phrase}")
    for path, phrases in {**REQUIRED_OBSERVABILITY_PHRASES, **REQUIRED_DOC_PHRASES}.items():
        if ctx.mode == "installed" and not (ctx.root / path).is_file():
            continue
        text = read(ctx, path)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{path} missing phrase: {phrase}")
    return errors


def check_portable_docs(ctx: ValidationContext) -> list[str]:
    if ctx.mode == "kit":
        return []
    errors: list[str] = []
    for path in PORTABLE_DOCS:
        text = read(ctx, path)
        for pattern in PORTABLE_DOC_FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path} contains non-portable/private pattern: {pattern.pattern}")
    return errors


def check_env_example(ctx: ValidationContext) -> list[str]:
    if ctx.mode == "kit":
        return []
    text = read(ctx, ".env.EXAMPLE")
    active_assignments = [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#") and "=" in line]
    return [f".env.EXAMPLE contains active assignment: {line}" for line in active_assignments if line.split("=", 1)[1].strip()]


def bundled_skill_names(ctx: ValidationContext) -> set[str]:
    manifest = ctx.root / "skills" / ".bundled_manifest"
    if not manifest.is_file():
        return set()
    names: set[str] = set()
    for line in manifest.read_text(encoding="utf-8", errors="ignore").splitlines():
        name = line.split(":", 1)[0].strip()
        if name:
            names.add(name)
    return names


def bundled_skill_roots(ctx: ValidationContext, bundled_names: set[str]) -> set[Path]:
    """Return installed-profile skill roots listed in the bundled manifest."""
    roots: set[Path] = set()
    if not bundled_names:
        return roots
    skills_dir = ctx.root / "skills"
    for skill_file in skills_dir.rglob("SKILL.md"):
        rel_root = skill_file.parent.relative_to(ctx.root)
        if rel_root == Path("skills/agent-foundry-core"):
            continue
        text = skill_file.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"(?m)^name:\s*([^\n]+)$", text)
        if match and match.group(1).strip().strip('"\'') in bundled_names:
            roots.add(rel_root)
    return roots


def is_installed_profile_external_skill_path(rel: Path, bundled_roots: set[Path]) -> bool:
    return any(rel.parts[: len(root.parts)] == root.parts for root in bundled_roots)


def check_secret_like_content(ctx: ValidationContext) -> list[str]:
    findings: list[str] = []
    bundled_roots = bundled_skill_roots(ctx, bundled_skill_names(ctx))
    for path in ctx.root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ctx.root)
        if any(part in SECRET_SCAN_SKIPPED_DIRS for part in rel.parts):
            continue
        if path.suffix in {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".db", ".lock"}:
            continue
        if is_installed_profile_external_skill_path(rel, bundled_roots):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line_no, line in enumerate(text.splitlines(), 1):
            for pattern in SECRET_PATTERNS:
                if pattern.search(line) and not any(allowed in line for allowed in ALLOWED_SECRET_WORD_CONTEXT):
                    findings.append(f"{rel}:{line_no}: {line[:120]}")
    return findings


def validate(ctx: ValidationContext) -> list[str]:
    errors: list[str] = []
    errors.extend(f"missing required file: {path}" for path in check_required_files(ctx))
    errors.extend(check_stage_contexts(ctx))
    errors.extend(check_kit_outputs(ctx))
    errors.extend(check_fixture_contracts(ctx))
    errors.extend(check_forbidden_source_paths(ctx))
    errors.extend(check_forbidden_kit_paths(ctx))
    errors.extend(check_yaml(ctx))
    errors.extend(check_distribution_ownership(ctx))
    errors.extend(check_skill_frontmatter(ctx))
    errors.extend(check_content(ctx))
    errors.extend(check_portable_docs(ctx))
    errors.extend(check_env_example(ctx))
    secret_findings = check_secret_like_content(ctx)
    if secret_findings:
        errors.append("secret-like findings:\n" + "\n".join(secret_findings))
    return errors


def main() -> int:
    args = parse_args()
    ctx = ValidationContext(root=args.root.resolve(), mode=args.mode)
    errors = validate(ctx)

    if errors:
        print("validation_failed")
        print(f"mode={ctx.mode}")
        print(f"root={ctx.root}")
        for error in errors:
            print(f"- {error}")
        return 1

    print("validation_ok")
    print(f"mode={ctx.mode}")
    print(f"root={ctx.root}")
    if ctx.mode == "kit":
        required_file_count = len(REQUIRED_KIT_FILES)
        if generated_kit_output_present(ctx):
            required_file_count += len(REQUIRED_GENERATED_KIT_OUTPUTS)
    elif ctx.mode == "installed":
        required_file_count = len(REQUIRED_INSTALLED_FILES)
    else:
        required_file_count = len(REQUIRED_SOURCE_FILES)
    print(f"required_files={required_file_count}")
    if ctx.mode != "kit":
        print("distribution=agent-foundry@" + str(distribution_manifest(ctx)["version"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
