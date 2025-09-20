# agent-builder

## Agent Overview

**agent-builder** is a comprehensive, interactive framework designed to assist developers in building robust, reliable, and well-documented AI agents. It incorporates the latest best practices from leading AI research organizations including OpenAI, Anthropic, Google, and the open-source community to provide a structured and guided development experience.

- **Version**: 1.0.0
- **Author**: Manus AI
- **Created**: 2025-09-20
- **Last Updated**: 2025-09-20

## Setup Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run tests
python -m pytest tests/ -v

# Start the agent-builder
python src/agent_builder.py
```

## Agent Architecture

### Core Components

- **Conversational Interface**: LLM-powered guidance system for interactive development
- **Knowledge Base**: Curated repository of AI agent best practices from authoritative sources
- **Project Scaffolding Engine**: Generates complete project structures with boilerplate code
- **Tool Management System**: Helps define, add, and document agent tools
- **Testing Framework**: Integrated TDD support with comprehensive test templates
- **Documentation Generator**: Maintains up-to-date `agents.md` and `README.md` files

### Tools Available

#### new-agent

**Description**: Initializes a new agent project with guided setup process

**Input Parameters**:
- `agent_name` (string, required): Name of the new agent
- `description` (string, required): Brief description of the agent's purpose
- `author` (string, optional): Author name, defaults to current user

**Example Usage**:
```bash
agent-builder new-agent --name weather-agent --description "An agent that provides weather information"
```

#### design-agent

**Description**: Interactively defines the agent's architecture, roles, and tools

**Input Parameters**:
- `project_path` (string, required): Path to the agent project directory
- `interactive` (boolean, optional): Enable interactive mode, defaults to true

**Example Usage**:
```bash
agent-builder design-agent --project-path ./weather-agent
```

#### scaffold-project

**Description**: Generates the complete project structure including boilerplate code and documentation

**Input Parameters**:
- `project_path` (string, required): Path to the agent project directory
- `template` (string, optional): Template type to use, defaults to "standard"

**Example Usage**:
```bash
agent-builder scaffold-project --project-path ./weather-agent
```

#### add-tool

**Description**: Guided workflow for adding new tools to an agent, including code and documentation generation

**Input Parameters**:
- `project_path` (string, required): Path to the agent project directory
- `tool_name` (string, required): Name of the new tool
- `tool_description` (string, required): Description of the tool's functionality

**Example Usage**:
```bash
agent-builder add-tool --project-path ./weather-agent --tool-name weather-api --tool-description "Retrieves weather data"
```

#### run-tests

**Description**: Executes the test suite for an agent and provides feedback

**Input Parameters**:
- `project_path` (string, required): Path to the agent project directory
- `coverage` (boolean, optional): Generate coverage report, defaults to false
- `verbose` (boolean, optional): Verbose output, defaults to true

**Example Usage**:
```bash
agent-builder run-tests --project-path ./weather-agent --coverage
```

#### update-docs

**Description**: Automatically updates the agents.md and README.md files to reflect changes

**Input Parameters**:
- `project_path` (string, required): Path to the agent project directory
- `force` (boolean, optional): Force update even if no changes detected, defaults to false

**Example Usage**:
```bash
agent-builder update-docs --project-path ./weather-agent
```

#### publish-agent

**Description**: Provides checklist and guidance for publishing an agent to platforms like GitHub

**Input Parameters**:
- `project_path` (string, required): Path to the agent project directory
- `platform` (string, optional): Target platform (github, pypi), defaults to "github"

**Example Usage**:
```bash
agent-builder publish-agent --project-path ./weather-agent --platform github
```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code formatting
- Use type hints for all function parameters and return values
- Include comprehensive docstrings for all classes and methods
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Testing Requirements

- All new features must have corresponding unit tests
- Maintain minimum 85% code coverage
- Include integration tests for complex workflows
- Performance tests for critical paths
- Security tests for input validation

### Error Handling

- Implement comprehensive error handling with structured error responses
- Use custom exception hierarchy for different error types
- Log all errors with appropriate severity levels
- Provide actionable error messages for users
- Include error recovery mechanisms where possible

### Documentation Standards

- Maintain up-to-date `agents.md` files for all generated agents
- Include usage examples for all tools and features
- Document configuration options and environment variables
- Provide troubleshooting guides for common issues
- Keep changelog updated with version releases

## Configuration

### Environment Variables

```bash
# Required
AGENT_BUILDER_OPENAI_API_KEY=your_openai_api_key_here

# Optional
AGENT_BUILDER_LOG_LEVEL=INFO
AGENT_BUILDER_DEFAULT_AUTHOR=Your Name
AGENT_BUILDER_TEMPLATE_PATH=/path/to/custom/templates
AGENT_BUILDER_OUTPUT_PATH=/path/to/output/directory
```

### Configuration File

The agent-builder can be configured using a `config.json` file:

```json
{
  "name": "agent-builder",
  "description": "AI Agent Development Framework",
  "version": "1.0.0",
  "default_author": "Manus AI",
  "template_path": "./templates",
  "output_path": "./output",
  "log_level": "INFO",
  "best_practices": {
    "openai_guide": "enabled",
    "anthropic_patterns": "enabled",
    "agents_md_spec": "enabled",
    "security_checks": "enabled"
  },
  "tools": {
    "new_agent": {
      "enabled": true,
      "interactive_mode": true
    },
    "design_agent": {
      "enabled": true,
      "validation_checks": true
    },
    "scaffold_project": {
      "enabled": true,
      "include_tests": true,
      "include_docs": true
    }
  }
}
```

## Usage Examples

### Creating a New Agent

```python
from src.agent_builder import AgentBuilder, AgentBuilderConfig

# Create configuration
config = AgentBuilderConfig(
    default_author="Your Name",
    template_path="./templates"
)

# Initialize agent builder
builder = AgentBuilder(config)

# Create a new agent project
result = builder.new_agent(
    agent_name="weather-agent",
    description="An agent that provides weather information",
    author="Your Name"
)

if result["success"]:
    print(f"Agent created at: {result['project_path']}")
else:
    print(f"Error: {result['error']}")
```

### Interactive Agent Design

```python
# Design the agent architecture interactively
design_result = builder.design_agent(
    project_path="./weather-agent",
    interactive=True
)

# The builder will guide you through:
# - Defining the agent's primary role
# - Selecting required tools
# - Configuring human-in-the-loop checkpoints
# - Setting up error handling strategies
```

### Scaffolding Complete Project

```python
# Generate the complete project structure
scaffold_result = builder.scaffold_project(
    project_path="./weather-agent",
    template="standard"
)

# This creates:
# - src/agent.py (main agent implementation)
# - src/tools/ (tool implementations)
# - tests/ (comprehensive test suite)
# - docs/ (documentation files)
# - agents.md (agent specification)
# - README.md (project overview)
```

### Adding Tools to Existing Agent

```python
# Add a new tool to an existing agent
tool_result = builder.add_tool(
    project_path="./weather-agent",
    tool_name="weather_forecast",
    tool_description="Provides 5-day weather forecast"
)

# This generates:
# - Tool implementation file
# - Tool test file
# - Updated documentation
# - Schema validation
```

## Testing Instructions

### Running Tests

```bash
# Run all tests for the agent-builder
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_scaffolding.py -v
python -m pytest tests/test_templates.py -v
python -m pytest tests/test_integration.py -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run performance tests
python -m pytest tests/test_performance.py -v --benchmark-only
```

### Test Categories

- **Unit Tests**: `tests/test_*.py` - Test individual components and tools
- **Integration Tests**: `tests/test_integration.py` - Test end-to-end workflows
- **Template Tests**: `tests/test_templates.py` - Validate template generation
- **Performance Tests**: `tests/test_performance.py` - Test response times and resource usage
- **Security Tests**: `tests/test_security.py` - Test input validation and security measures

### Testing Generated Agents

```bash
# Test a generated agent
cd ./weather-agent
python -m pytest tests/ -v

# Run the agent-builder's validation on generated agents
agent-builder run-tests --project-path ./weather-agent --coverage
```

## Deployment

### Local Development

```bash
# Clone the repository
git clone https://github.com/vbonk/app-agents.git
cd app-agents/agents/agent-builder

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env with your settings

# Run the agent-builder
python src/agent_builder.py
```

### Production Deployment

```bash
# Build Docker image
docker build -t agent-builder:latest .

# Run container
docker run -d --name agent-builder \
  -e AGENT_BUILDER_OPENAI_API_KEY=your_key \
  -v /path/to/projects:/app/projects \
  -p 8000:8000 \
  agent-builder:latest
```

### Integration with Development Workflows

```yaml
# GitHub Actions workflow for generated agents
name: Agent CI/CD
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/ -v --cov=src
      - name: Validate agent specification
        run: agent-builder validate --project-path .
```

## Security Considerations

### Input Validation

- All user inputs are validated and sanitized before processing
- Agent names and descriptions are checked for malicious content
- File paths are validated to prevent directory traversal attacks
- Template parameters are escaped to prevent injection attacks

### Code Generation Security

- Generated code includes security best practices by default
- Input validation is built into all generated tools
- Error messages are sanitized to prevent information disclosure
- Generated agents include security testing templates

### API Security

- OpenAI API keys are stored securely and never logged
- Rate limiting is implemented for all external API calls
- Timeout mechanisms prevent hanging requests
- API responses are validated before processing

### Data Privacy

- No user code or agent implementations are transmitted to external services
- Local processing ensures privacy of proprietary agent designs
- Generated agents include privacy-by-design principles
- User data can be exported or deleted on request

## Troubleshooting

### Common Issues

**Agent-builder won't start**:
- Check that Python 3.8+ is installed
- Verify that all dependencies are installed correctly
- Ensure OpenAI API key is set in environment variables
- Check the logs for specific error messages

**Template generation fails**:
- Verify that template files are present in the templates directory
- Check file permissions for the output directory
- Ensure agent name follows naming conventions (lowercase, hyphens only)
- Review template syntax for any errors

**Generated agent tests fail**:
- Run the agent-builder's validation tool on the generated project
- Check that all required dependencies are installed in the agent project
- Verify that the agent's configuration is valid
- Review the test output for specific failure reasons

**Performance issues**:
- Monitor memory usage during large project generation
- Check network connectivity for API calls
- Consider using local templates for faster generation
- Enable caching for frequently used patterns

### Debug Mode

Enable debug logging to get more detailed information:

```bash
export AGENT_BUILDER_LOG_LEVEL=DEBUG
python src/agent_builder.py
```

### Validation Tools

```bash
# Validate a generated agent project
agent-builder validate --project-path ./weather-agent

# Check template syntax
agent-builder check-templates --template-path ./templates

# Verify best practices compliance
agent-builder audit --project-path ./weather-agent
```

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-template`
3. Implement your changes with comprehensive tests
4. Run the full test suite: `python -m pytest tests/ -v`
5. Update documentation as needed
6. Submit a pull request with detailed description

### Adding New Templates

1. Create template files in `templates/` directory
2. Follow the existing template structure and naming conventions
3. Add template validation tests in `tests/test_templates.py`
4. Update the template registry in `src/template_manager.py`
5. Document the new template in this `agents.md` file

### Adding New Tools

1. Implement the tool in `src/tools/` directory
2. Follow the existing tool interface and patterns
3. Add comprehensive unit and integration tests
4. Update the tool registry and documentation
5. Include usage examples and error handling

### Code Review Guidelines

- All code must pass the comprehensive test suite
- New features require documentation updates and examples
- Security implications must be thoroughly reviewed
- Performance impact should be measured and documented
- Generated code quality must meet framework standards

## Changelog

### Version 1.0.0 (2025-09-20)
- Initial release of the agent-builder framework
- Implemented core scaffolding and template system
- Added comprehensive best practices from OpenAI, Anthropic, and Google
- Created interactive agent design workflow
- Implemented automatic documentation generation
- Added comprehensive testing framework
- Included security and performance testing templates
- Created example weather-agent implementation
- Established integration with GitHub workflows

---

*This file is automatically maintained by the agent-builder framework. Manual edits may be overwritten during updates.*
