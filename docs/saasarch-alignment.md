# SaaSArch Alignment Guide

This guide explains how the `app-agents` workspace connects to the wider SaaS Ecosystem Architecture project and how to keep assets synchronized.

## Canonical Sources
- **Templates**: `shared/templates/agent_templates/` hosts the agent, agents.md, test, and tool scaffolding shared by all agents and Manus documentation.
- **Standards**: `manus/schemas-and-specs/agent_standards_and_specifications.md` extends SaaSArch standards. The crosswalk in `codex/reports/saasarch_alignment.md` tracks remaining deltas.
- **Session Records**: `codex/` contains session snapshots and audit reports. Use these when updating the SaaSArch documentation so context is preserved.
- **Prompt Library**: Each agent now exposes canonical system/chat prompts in its directory (e.g., `agents/support/agent-builder/agent-builder-system-prompt.md`). Port these into SaaSArch when creating the centralized prompt catalog.
- **Agent Registry**: `agents/registry.json` exports a machine-readable catalog (category, prompts, paths). SaaSArch and admin-app should ingest this file instead of duplicating metadata.

## Update Workflow
1. **Run Tooling**: Activate the local virtual environment (`source .venv/bin/activate`) and install dependencies with `pip install -r requirements.txt`.
2. **Refresh Documentation**:
   - `python .github/scripts/update_readme.py` updates the root README with the latest agent catalog.
   - `scripts/update-readme.sh` provides a convenience wrapper that installs dependencies if needed.
3. **Sync with SaaSArch**:
   - Export relevant updates (template changes, new agent specs) into `saas-ecosystem-architecture` under the matching standard or docs section.
   - Run `scripts/sync-saasarch.sh [path-to-saas-ecosystem-architecture]` to copy canonical agent templates into the SaaSArch `standards/templates/agent/` directory.
   - Commit the updated `agents/registry.json` alongside documentation updates so downstream systems stay aligned.
   - Reference the crosswalk to ensure every Manus artifact has a home in SaaSArch and admin-app.
4. **Preserve the Session**: Log major changes in `codex/session-overview.md` and add detailed notes under `codex/reports/`.

## Pending Actions
- Publish a `docs/agents/` section inside SaaSArch summarising each agent with links back to the canonical specs in this repo.
- Incorporate Codex session preservation guidance into SaaSArch `AUTOMATION.md`.
- Promote the new CI workflow (`.github/workflows/ci.yml`) to a reusable SaaSArch workflow once stabilized.
- Surface repository credential status inside the SaaSArch admin-app page (`Dashboard → Settings → Repository Access`) so operations can monitor token health.

Keeping these steps in sync ensures that both repositories speak the same language and prevents drift between Manus research, code templates, and the SaaSArch ecosystem documentation.
