# Agent Portfolio Comparison: SaaSArch vs. app-agents

## Summary Table
| SaaSArch Draft Agent | Category | Purpose | Matching app-agents Asset | Notes |
| --- | --- | --- | --- | --- |
| Universal App Generator | Strategic | Generate production apps | Partially overlaps with `agent-builder` | app-agents currently scaffolds agents, not full SaaS apps. Could extend Agent Builder to deliver multi-app scaffolding. |
| Infrastructure Orchestration | Strategic | Optimize hosting + infra | None | Candidate for future agent; shared base provides foundation but no implementation. |
| Centralized Secrets | Strategic | Credential management | None | Could integrate with shared templates and Codex session artifacts. |
| Business Intelligence | Strategic | Cross-app analytics | `prompt-researcher` (partial) | Prompt Researcher gathers data but lacks BI dashboards. |
| Quality Assurance | Strategic | Automated testing/compliance | `ui-architect-agent` (subset) | UI agent focuses on design rather than full QA. |
| Customer Success | Strategic | Retention optimization | None | Missing agent category in app-agents. |
| Content Generation | Strategic | Asset creation | None | Manus documentation can seed future agent. |
| Security Monitoring | Strategic | Threat detection | None | No security agent yet. |
| Revenue Optimization | Strategic | Pricing/billing | None | Opportunity to extend `prompt-researcher` to revenue analysis. |
| Ecosystem Evolution | Strategic | Platform transformation | Partially addressed via `manus` research | app-agents lacks execution agent. |
| GitHub Operations | Operational | Repo automation | None | Could leverage shared templates for automation tasks. |
| Workflow Orchestration | Operational | CI/CD optimization | `.github/workflows/ci.yml` (partial) | Scripts/workflows exist but no agent front end. |
| Issue Intelligence | Operational | Automated issue resolution | None | Prompt Researcher could be extended. |
| Document Intelligence | Operational | Documentation generation | `agent-builder` (doc generator feature) | Already a feature—could evolve into standalone agent. |
| Repository Monitoring | Operational | Cross-repo compliance | `scripts/sync-saasarch.sh` + Codex automation | Need agent wrapper for proactive monitoring. |
| Performance Monitoring | Operational | Proactive optimization | None | No equivalent yet. |
| Deployment Intelligence | Operational | Risk-aware deployments | SaaSArch workflows (planned) | Not implemented in app-agents. |
| Ecosystem Analytics | Operational | Strategic insights | `prompt-researcher` (partial) | Data collection present; analytics dashboards absent. |

## Key Observations
- **Coverage**: app-agents currently provides four concrete agents (Agent Builder, Enhanced Crawler, Prompt Researcher, UI Architect). These map mainly to documentation/scaffolding, data gathering, and UX guidance. SaaSArch’s 18-agent roadmap spans strategy, security, revenue, and operations, leaving large functional gaps.
- **Shared Foundations**: Recent work (shared templates, prompt assets, async tool handlers) positions app-agents to serve as the canonical implementation hub once the remaining SaaSArch agents are prioritized.
- **Next Opportunities**: Candidates for immediate development include GitHub Operations (to automate repo hygiene), Document Intelligence (building on Agent Builder’s documentation engine), and Security Monitoring (leveraging existing Manus research on security posture).
- **Catalog Readiness**: The new `agents/registry.json` plus private repo credential dashboard in admin-app makes it easier to onboard additional agents and keep downstream systems synchronized.

## Recommendations
1. Use Manus research and shared templates to spin up minimal versions of high-priority SaaSArch agents, starting with operational categories where infrastructure is ready.
2. Extend `prompt-researcher` with analytics dashboards to cover Business Intelligence and Ecosystem Analytics use cases.
3. Plan future prompt libraries in SaaSArch to host the new agent system/chat prompts as they are delivered.
