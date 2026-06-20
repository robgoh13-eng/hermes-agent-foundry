
# Stage: 02 Research

## Goal
Gather bounded source-backed context only when needed for external, unfamiliar, regulated, or specialized capabilities.

## Inputs
- `01_fit_check/*`
- Local skills list
- Web/GitHub/MCP sources when triggered

## Process
1. Search local skills first.
2. Check built-in Hermes toolsets before MCP.
3. Search web/GitHub for candidate skill/tool/MCP sources only if needed.
4. Rank candidates by fit, maturity, auth burden, read/write risk, and install complexity.

## Outputs
- `research-notes.md`
- Optional `skill-candidates.md`, `toolset-candidates.md`, `mcp-server-candidates.md`, `repo-shortlist.md`

## Allowed files/tools
- Read prior-stage artifacts, local skills lists, docs, and explicitly approved source material.
- Use web/GitHub search only when the request needs external, unfamiliar, regulated, or specialized capability research.
- Write only research notes and candidate reports inside the approved build-kit or patch-kit directory.

## Forbidden actions
- Do not install skills, packages, or MCP servers.
- Do not configure credentials.

## Verification
- Candidate recommendations include source URLs and verify-before-install notes.
