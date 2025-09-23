# {{agent_name}}

## Agent Overview

**{{agent_name}}** is {{agent_description}}

- **Version**: {{agent_version}}
- **Author**: {{author_name}}
- **Created**: {{creation_date}}
- **Last Updated**: {{last_updated}}

## Setup Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run tests
python -m pytest tests/ -v

# Start the agent
python src/agent.py
```

## Agent Architecture

### Core Components

- **Main Agent**: `src/agent.py` - The primary agent logic and conversation loop
- **Tools**: `src/tools/` - Individual tool implementations
- **Memory**: Built-in conversation and context management
- **Configuration**: Environment-based configuration system

### Tools Available

{{#each tools}}
#### {{name}}

**Description**: {{description}}

**Input Parameters**:
{{#each parameters}}
- `{{name}}` ({{type}}{{#if required}}, required{{/if}}): {{description}}
{{/each}}

**Example Usage**:
```python
result = agent.execute_tool("{{name}}", {{example_params}})
```

{{/each}}

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code formatting
- Use type hints for all function parameters and return values
- Include docstrings for all classes and methods
- Maximum line length: 100 characters

### Testing Requirements

- All new tools must have corresponding unit tests
- Maintain minimum 80% code coverage
- Run the full test suite before committing changes
- Include integration tests for complex workflows

### Error Handling

- All tools must implement proper error handling and return structured error responses
- Use the `ToolError` exception hierarchy for tool-specific errors
- Log all errors with appropriate severity levels
- Provide helpful error messages for users

### Documentation Standards

- Update this `agents.md` file when adding new tools or changing functionality
- Include usage examples for all tools
- Document any environment variables or configuration requirements
- Maintain a changelog for version updates

## Configuration

### Environment Variables

```bash
# Required
{{agent_name_upper}}_API_KEY=your_api_key_here

# Optional
{{agent_name_upper}}_LOG_LEVEL=INFO
{{agent_name_upper}}_MAX_ITERATIONS=10
{{agent_name_upper}}_ENABLE_HUMAN_FEEDBACK=false
```

### Configuration File

The agent can also be configured using a `config.json` file:

```json
{
  "name": "{{agent_name}}",
  "description": "{{agent_description}}",
  "version": "{{agent_version}}",
  "max_iterations": 10,
  "enable_human_feedback": false,
  "log_level": "INFO",
  "tools": {
    {{#each tools}}
    "{{name}}": {
      "enabled": true,
      "timeout_seconds": 30,
      "retry_attempts": 3
    }{{#unless @last}},{{/unless}}
    {{/each}}
  }
}
```

## Usage Examples

### Basic Interaction

```python
from src.agent import {{agent_class_name}}, AgentConfig

# Create configuration
config = AgentConfig(
    name="{{agent_name}}",
    max_iterations=5,
    enable_human_feedback=False
)

# Initialize agent
agent = {{agent_class_name}}(config)

# Process user input
response = agent.process_user_input("Hello, can you help me?")
print(response)
```

### Using Tools Directly

```python
# Execute a specific tool
result = agent.execute_tool("{{example_tool_name}}", 
                          parameter1="value1",
                          parameter2="value2")

if result["success"]:
    print("Tool executed successfully:", result["data"])
else:
    print("Tool execution failed:", result["error"])
```

### Interactive Session

```python
# Run an interactive session
agent.run_interactive_session()
```

## Testing Instructions

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_agent.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run performance tests
python -m pytest tests/test_performance.py -v
```

### Test Categories

- **Unit Tests**: `tests/test_*.py` - Test individual components
- **Integration Tests**: `tests/test_integration.py` - Test component interactions
- **Performance Tests**: `tests/test_performance.py` - Test response times and resource usage
- **Security Tests**: `tests/test_security.py` - Test input sanitization and security measures

## Deployment

### Local Development

```bash
# Clone the repository
git clone <repository_url>
cd {{agent_name}}

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the agent
python src/agent.py
```

### Production Deployment

```bash
# Build Docker image
docker build -t {{agent_name}}:latest .

# Run container
docker run -d --name {{agent_name}} \
  -e {{agent_name_upper}}_API_KEY=your_key \
  -p 8000:8000 \
  {{agent_name}}:latest
```

## Security Considerations

### Input Validation

- All user inputs are validated before processing
- Malicious content is sanitized or rejected
- File uploads are scanned and restricted by type and size

### API Security

- API keys are stored securely and never logged
- Rate limiting is implemented for all external API calls
- Timeout mechanisms prevent hanging requests

### Data Privacy

- Conversation history is stored locally only
- No sensitive data is transmitted to external services without explicit consent
- User data can be exported or deleted on request

## Troubleshooting

### Common Issues

**Agent won't start**:
- Check that all required environment variables are set
- Verify that dependencies are installed correctly
- Check the logs for specific error messages

**Tool execution fails**:
- Verify that API keys are valid and have necessary permissions
- Check network connectivity for external API calls
- Review tool-specific documentation for parameter requirements

**Performance issues**:
- Monitor memory usage and adjust `max_iterations` if needed
- Check for infinite loops in agent logic
- Consider enabling caching for frequently used tools

### Debug Mode

Enable debug logging to get more detailed information:

```bash
export {{agent_name_upper}}_LOG_LEVEL=DEBUG
python src/agent.py
```

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-tool`
3. Implement your changes with tests
4. Run the test suite: `python -m pytest tests/ -v`
5. Update documentation as needed
6. Submit a pull request

### Adding New Tools

1. Create a new tool file in `src/tools/`
2. Implement the tool following the template pattern
3. Add comprehensive tests in `tests/`
4. Update this `agents.md` file with tool documentation
5. Add usage examples

### Code Review Guidelines

- All code must pass the test suite
- New features require documentation updates
- Security implications must be considered
- Performance impact should be evaluated

## Changelog

### Version {{agent_version}} ({{creation_date}})
- Initial release
- Implemented core agent framework
- Added basic tool system
- Created comprehensive test suite

---

*This file is automatically maintained by the agent-builder framework. Manual edits may be overwritten during updates.*
