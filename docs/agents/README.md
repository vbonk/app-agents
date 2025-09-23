# Agent Documentation Index

This directory contains detailed documentation for each agent in the repository, organized by category.

## Directory Structure

```
docs/agents/
├── README.md                    # This index file
├── support/                     # Development support agents
│   ├── agent-builder.md        # Agent Builder documentation
│   └── ui-architect-agent.md   # UI Architect Agent documentation
├── research/                    # Research and analysis agents
├── strategic/                   # Strategic planning agents
│   └── prompt-researcher.md    # Prompt Researcher documentation
├── operational/                 # Operational automation agents
│   └── crawler.md              # Crawler Agent documentation
└── [other-categories]/         # Additional agent categories
```

## Agent Categories

### Support Agents

Agents that provide development support, tooling, and infrastructure assistance.

- **[Agent Builder](support/agent-builder.md)**: Framework for building new AI agents
- **[UI Architect Agent](support/ui-architect-agent.md)**: UI/UX design assistance

### Research Agents

Agents focused on data collection, analysis, and research activities.

_(Documentation forthcoming)_

### Strategic Agents

Agents that handle planning, strategy, and high-level decision making.

- **[Prompt Researcher](strategic/prompt-researcher.md)**: Advanced prompt engineering and research

### Operational Agents

Agents that handle day-to-day operations, automation, and workflow management.

- **[Crawler](operational/crawler.md)**: Automated web crawling and data extraction

## Documentation Standards

Each agent documentation file should include:

1. **Overview**: Purpose and capabilities
2. **Features**: Key functionality and specializations
3. **Usage**: How to interact with the agent
4. **Configuration**: Setup and customization options
5. **Examples**: Sample interactions and use cases
6. **Technical Details**: Implementation specifics
7. **Dependencies**: Required resources and integrations

## Contributing

When adding new agents:

1. Create appropriate category subdirectory if needed
2. Add agent documentation following the standards above
3. Update this index file with the new agent entry
4. Ensure cross-references are maintained

## Maintenance

This documentation is automatically synchronized with the main README through the documentation automation system. Manual updates to individual agent docs should be made here, and the automation will handle integration with the main repository documentation.

See [AUTOMATION.md](../AUTOMATION.md) for details on the documentation automation system.
