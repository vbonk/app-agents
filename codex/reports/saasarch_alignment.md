# SaaSArch Alignment Crosswalk (app-agents vs. Manus Artifacts)

## Overview
This document maps the key documentation and asset types in `app-agents/manus` against the canonical sources inside `saas-ecosystem-architecture`. It highlights where content already exists, where material diverges, and the gaps that must be closed before declaring first-class SaaSArch alignment.

## Crosswalk Table
| Category | Manus / app-agents Source | SaaSArch Source | Gap / Action |
| --- | --- | --- | --- |
| Agent Standards | `manus/schemas-and-specs/agent_standards_and_specifications.md` | `standards/documentation/standards.md`, `standards/planning/agentic-planning-standards.md` | SaaSArch docs are higher-level; need to fold Manus-specific requirements (tool registry, memory expectations) into SaaSArch standards or link reciprocally. |
| API & Schema Specs | `manus/schemas-and-specs/api_specification.md`, `manus/schemas-and-specs/prisma_schema.md` | None (SaaSArch references platform schemas only) | Determine whether these specs belong in SaaSArch or remain agent-local; if adopted, place under `standards/` with versioning. |
| Agent Templates | `manus/templates-and-tools/agent_template.py`, `agents_md_template.md`, `test_template.py`, `tool_template.py` | No packaged templates (guidance only) | Package templates as a shared module or sync to SaaSArch `standards/templates/`; update docs to cite the shared source. |
| Documentation Guides | `manus/documentation/*.md` | `DEVELOPMENT.md`, `ARCHITECTURE.md`, strategy docs | Decide whether to migrate Manus guides into a SaaSArch `docs/agents/` hierarchy and link from Manus back to canonical copies. |
| Prompt Libraries | `agents/*/*-system-prompt.md`, `agents/*/*-chat-prompt.md` | None | Add prompt repositories to SaaSArch (e.g., `docs/agents/prompts/`) and reference them from agent briefs so orchestration layers can access the official wording. |
| Agent Registry | `agents/registry.json` | None | Import the registry JSON into SaaSArch/admin-app to drive dashboards and avoid manual duplication. |
| Repository Credentials | admin-app `src/app/dashboard/settings/repository-access` | None | Document the admin-app workflow so operators know how to rotate/validate GitHub tokens used for private repositories. |
| Research Findings | `manus/research-data/*.md` | `RESEARCH_SUMMARY_AND_STRATEGIC_RECOMMENDATIONS.md` | Condense Manus findings into SaaSArch research or cross-link sections so insights stay aligned. |
| Directory Listings | `manus/directory-listing.txt`, `manus/Agents.md` | `README.md`, `standards/integration/project-hierarchy.md` | Align naming conventions and ensure both repos list the same agent catalog with matching metadata. |
| Automation Workflows | `.github/workflows/update-readme.yml`, `.github/workflows/ci.yml` | `standards/workflows/*.yml` | Document the new workflows in SaaSArch automation guides and consider promoting them to reusable templates. |
| Session Preservation | `codex/session-overview.md`, `codex/reports/*.md` | None | Add “session preservation” guidance to SaaSArch documentation (e.g., in `AUTOMATION.md`) and reference Codex templates. |

## Immediate Documentation Tasks
1. Produce a shared template package (or git submodule) so both repositories draw from one source of truth for agent scaffolding.
2. Update SaaSArch `README.md` and documentation index to reference the enhanced agent base, codex preservation process, and dependency manifest expectations.
3. Create a SaaSArch `docs/agents/` section summarising each agent with links back to `app-agents` specs, ensuring the catalog stays synchronized.
4. Document the new CI workflow (`.github/workflows/ci.yml`) within SaaSArch automation standards and evaluate promoting it to `standards/workflows/testing-workflow.yml`.

## Notes
- Manus research artifacts are detailed; consider extracting executive summaries for SaaSArch while keeping the full texts in app-agents.
- Several Manus documents duplicate SaaSArch content (e.g., testing guidelines); during consolidation default to SaaSArch as the canonical source and link to it from Manus/app-agents.
