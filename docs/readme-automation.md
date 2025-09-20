# README Automation System

**Automatic Documentation Updates for Agent Repository**

This system automatically maintains the main README.md file with current information about all agents in the repository. It ensures that the documentation stays synchronized with the actual codebase without manual intervention.

## How It Works

The README automation system consists of three main components that work together to keep documentation current and accurate.

### Automatic GitHub Action

The primary automation runs via GitHub Actions whenever changes are made to the `agents/` directory. The workflow is triggered by pushes or pull requests that modify agent files, ensuring that documentation updates happen immediately when agents are added, modified, or removed.

The GitHub Action performs several key operations including scanning all agent directories for metadata, extracting information from `agents.md` and `README.md` files, detecting datasets and configuration files, and automatically updating the main README.md with current information.

### Python Update Script

The core logic resides in `.github/scripts/update_readme.py`, which provides comprehensive agent discovery and documentation generation capabilities. This script intelligently parses agent metadata from multiple sources and generates consistent, well-formatted documentation sections.

The script performs sophisticated analysis including automatic category inference based on agent names and descriptions, dataset detection across multiple file formats, use case generation based on agent capabilities, and performance metrics extraction from agent specifications.

### Manual Update Option

For local development and testing, a manual update script is available at `scripts/update-readme.sh`. This allows developers to preview documentation changes before committing and provides a fallback option when the GitHub Action is not available.

## Agent Information Sources

The system extracts agent information from multiple sources to create comprehensive documentation:

### Primary Sources

**agents.md File**: The preferred source for agent metadata, following the standardized agent specification format. This file should contain structured information about the agent's capabilities, tools, usage examples, and performance metrics.

**README.md File**: Used as a fallback when `agents.md` is not available. The system extracts description and overview information from the agent's README file.

### Automatic Detection

**Dataset Files**: The system automatically scans for dataset files in common formats (Excel, CSV, JSON, YAML) within agent directories and subdirectories.

**Directory Structure**: Agent organization and file structure provide hints about agent categories and capabilities.

**Naming Patterns**: Agent names and file names help infer functionality and appropriate categorization.

## Generated Documentation Sections

The automation system generates several key sections in the main README.md:

### Available Agents Section

Each agent receives a dedicated subsection with comprehensive information including a cleaned display name, descriptive subtitle, detailed description and overview, special functions and capabilities, dataset information with descriptions, and inferred use cases based on functionality.

### Agent Categories Table

A structured table organizing agents by category with agent names listed by category, focus area descriptions, and placeholder entries for future categories.

### Performance Metrics

Standardized performance tracking information that applies to all agents, ensuring consistency in how agent quality and effectiveness are measured.

## Configuration and Customization

### Category Mapping

The system uses intelligent category inference based on keywords and patterns:

- **Research & Analysis**: Agents focused on data extraction, web crawling, and analysis
- **Design & UX**: Agents providing interface design and user experience guidance  
- **Development**: Agents supporting code generation and architecture
- **Content & Communication**: Agents for content creation and documentation

### Use Case Generation

Use cases are automatically inferred from agent names, descriptions, and capabilities. The system maintains a knowledge base of common patterns and generates relevant use cases for each agent type.

### Dataset Descriptions

Dataset files are automatically categorized and described based on naming patterns and file types. The system provides meaningful descriptions that help users understand the purpose and content of each dataset.

## Workflow Integration

### Automatic Updates

The GitHub Action integrates seamlessly with the development workflow:

1. **Trigger**: Any push or pull request affecting the `agents/` directory
2. **Scan**: Comprehensive analysis of all agent directories
3. **Generate**: Updated documentation sections with current information
4. **Commit**: Automatic commit and push of updated README.md
5. **Summary**: Detailed summary of changes made

### Manual Updates

For local development and testing:

```bash
# Run the manual update script
./scripts/update-readme.sh

# Or run the Python script directly
python3 .github/scripts/update_readme.py
```

### Continuous Integration

The system includes safeguards and best practices:

- **Skip CI**: Automatic commits include `[skip ci]` to prevent infinite loops
- **Change Detection**: Only commits when actual changes are made
- **Error Handling**: Graceful handling of missing files or malformed metadata
- **Rollback Safety**: Git history preserves all changes for easy rollback if needed

## Best Practices for Agent Developers

To ensure optimal documentation generation, follow these guidelines when creating new agents:

### Agent Metadata

Create a comprehensive `agents.md` file following the standard specification format. Include detailed descriptions of capabilities, tools, and usage examples. Provide clear performance metrics and success criteria.

### Directory Organization

Use consistent directory structure with `src/`, `docs/`, `tests/`, and `examples/` subdirectories. Place datasets in the `docs/` directory with descriptive filenames. Include comprehensive README.md files with clear descriptions.

### Naming Conventions

Use descriptive agent names that clearly indicate functionality. Follow kebab-case naming for consistency (e.g., `ui-architect-agent`). Include relevant keywords in descriptions for proper categorization.

### Dataset Documentation

Provide clear dataset descriptions and metadata. Use descriptive filenames that indicate content and purpose. Include sample data or examples where appropriate.

## Troubleshooting

### Common Issues

**Missing Agent Information**: Ensure `agents.md` or `README.md` exists in the agent directory with proper formatting and content.

**Incorrect Categorization**: Review agent name and description for category keywords, or manually specify category in agent metadata.

**Dataset Not Detected**: Verify dataset files are in supported formats and located in agent directory or `docs/` subdirectory.

**GitHub Action Failures**: Check Python dependencies and file permissions in the workflow configuration.

### Manual Intervention

If automatic updates fail or produce incorrect results:

1. Run the manual update script locally to test changes
2. Review generated output and adjust agent metadata as needed
3. Commit manual corrections with descriptive commit messages
4. Monitor subsequent automatic updates to ensure proper operation

## Future Enhancements

The README automation system is designed for extensibility and improvement:

### Planned Features

- **Performance Metrics Integration**: Automatic extraction of quantitative performance data
- **Usage Statistics**: Integration with agent usage analytics and metrics
- **Cross-References**: Automatic linking between related agents and shared resources
- **Validation**: Automated validation of agent metadata and documentation quality

### Customization Options

- **Template System**: Configurable templates for different agent types
- **Category Management**: Dynamic category creation and management
- **Formatting Options**: Customizable output formatting and styling
- **Integration Hooks**: Extensible system for additional data sources and outputs

This automation system ensures that the repository documentation remains accurate, comprehensive, and useful for all users while minimizing the maintenance burden on developers.
