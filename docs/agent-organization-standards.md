# Agent Directory Organization Standards

## Overview

This document establishes the standardized organization structure for AI agents in the app-agents repository. All agents must be organized under category subdirectories to ensure consistency, discoverability, and maintainability.

## Directory Structure

```
agents/
├── category-1/
│   ├── agent-a/
│   ├── agent-b/
│   └── agent-c/
├── category-2/
│   ├── agent-d/
│   └── agent-e/
└── registry.json
```

## Category Definitions

### Core Categories

#### `support/`

**Purpose**: Agents that provide development support, tooling, and infrastructure assistance
**Examples**:

- `agent-builder/` - Framework for building new agents
- `ui-architect-agent/` - UI/UX design assistance

#### `research/`

**Purpose**: Agents focused on data collection, analysis, and research activities
**Examples**:

- `web-research-agent/` - Web scraping and research
- `data-analysis-agent/` - Data processing and analysis

#### `strategic/`

**Purpose**: Agents that handle planning, strategy, and high-level decision making
**Examples**:

- `prompt-researcher/` - Advanced prompt engineering and research
- `product-management-agent/` - Product strategy and planning

#### `operational/`

**Purpose**: Agents that handle day-to-day operations, automation, and workflow management
**Examples**:

- `crawler/` - Automated web crawling and data extraction
- `workflow-automation-agent/` - Process automation

#### `design/`

**Purpose**: Agents focused on design, creativity, and user experience
**Examples**:

- `ui-architect-agent/` - UI/UX design (if not in support)
- `creative-writing-agent/` - Content creation

#### `development/`

**Purpose**: Agents that assist with software development and coding
**Examples**:

- `code-architect-agent/` - Software architecture design
- `testing-agent/` - Automated testing and QA

#### `content/`

**Purpose**: Agents for content creation, communication, and marketing
**Examples**:

- `content-strategist-agent/` - Content strategy and planning
- `communication-agent/` - Communication and messaging

#### `automation/`

**Purpose**: Agents specialized in automation and workflow optimization
**Examples**:

- `workflow-automation-agent/` - Business process automation

#### `analysis/`

**Purpose**: Agents for data analysis, insights, and reporting
**Examples**:

- `data-analysis-agent/` - Advanced data analytics

### Domain-Specific Categories

#### `communication/`

**Purpose**: Agents for communication, messaging, and interpersonal interactions

#### `creative/`

**Purpose**: Agents for creative work, art, and innovative content generation

#### `education/`

**Purpose**: Agents for educational content, tutoring, and learning assistance

#### `finance/`

**Purpose**: Agents for financial analysis, planning, and management

#### `health/`

**Purpose**: Agents for health-related information and assistance

#### `legal/`

**Purpose**: Agents for legal research, compliance, and documentation

#### `marketing/`

**Purpose**: Agents for marketing strategy, campaigns, and analytics

#### `product/`

**Purpose**: Agents for product management and development lifecycle

#### `sales/`

**Purpose**: Agents for sales support, lead generation, and customer engagement

#### `security/`

**Purpose**: Agents for security analysis, compliance, and risk assessment

#### `testing/`

**Purpose**: Agents specialized in software testing and quality assurance

#### `utility/`

**Purpose**: General-purpose utility agents and tools

## Agent Directory Structure

Each agent directory must follow this standardized structure:

```
agent-name/
├── README.md              # Agent overview and usage
├── agents.md              # Technical specifications
├── src/                   # Source code
├── docs/                  # Documentation and datasets
├── examples/              # Usage examples
├── templates/             # Agent-specific templates
├── agent-name-system-prompt.md    # System prompt
├── agent-name-chat-prompt.md      # Chat prompt (if different)
└── tests/                 # Test files
```

## Naming Conventions

### Category Directories

- Use lowercase, kebab-case: `support/`, `research/`, `strategic/`
- Single word when possible, compound words for clarity
- Should be plural when representing a category of agents

### Agent Directories

- Use lowercase, kebab-case: `agent-builder/`, `ui-architect-agent/`
- Include `-agent` suffix for clarity
- Keep names descriptive but concise

### Files

- Use lowercase, kebab-case for file names
- Include agent name prefix for prompt files: `agent-builder-system-prompt.md`

## Registry Integration

The `agents/registry.json` file must be updated whenever agents are added, moved, or removed. The registry provides machine-readable metadata for cross-repository integration.

## Migration Guidelines

### From Flat Structure

When migrating from a flat directory structure:

1. **Identify appropriate category** based on agent functionality
2. **Create category directory** if it doesn't exist
3. **Move agent directory** to appropriate category
4. **Update all references** in documentation and code
5. **Update registry.json** with new paths
6. **Test cross-repository links** to ensure nothing breaks

### Duplicate Resolution

If duplicate agent directories exist (top-level and category):

1. **Compare contents** to ensure they're identical
2. **Keep category version** as the canonical location
3. **Remove top-level duplicate** after verification
4. **Update all references** to point to category location

## Validation Rules

### Automated Checks

- All agents must be under category subdirectories (no top-level agents)
- Each agent must have required files (README.md, agents.md)
- Category directories must contain at least one agent
- Agent names must follow naming conventions
- Registry.json must reflect actual directory structure

### Manual Review

- Category assignments should be logical and consistent
- Agent functionality should match category purpose
- Documentation should be complete and accurate
- Cross-repository references should be updated

## Maintenance

### Adding New Agents

1. Choose appropriate category (or create new if needed)
2. Create agent directory following standard structure
3. Implement agent with required files
4. Update registry.json
5. Update main README.md (via automation)
6. Test cross-repository integration

### Adding New Categories

1. Ensure category serves a distinct purpose
2. Add category definition to this document
3. Create category directory
4. Move or create agents as appropriate
5. Update documentation

### Periodic Review

- Quarterly review of category assignments
- Annual audit of directory structure compliance
- Update category definitions as agent landscape evolves

## Cross-Repository Impact

Changes to agent organization may affect:

- SaaS Ecosystem Architecture admin app
- SaaS Spec Driven Development processes
- Documentation automation scripts
- CI/CD pipelines
- Cross-repository validation checks

Always coordinate changes with other repository maintainers.
