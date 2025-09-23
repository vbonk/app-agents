# weather-agent

## Agent Overview

**weather-agent** is an AI agent that can retrieve current weather information for any location worldwide. It provides temperature, weather conditions, humidity, and wind speed data in a user-friendly format.

- **Version**: 1.0.0
- **Author**: Agent-Builder Framework
- **Created**: 2025-09-20
- **Last Updated**: 2025-09-20

## Setup Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Start the agent
python src/agent.py
```

## Agent Architecture

### Core Components

- **Main Agent**: `src/agent.py` - The primary agent logic and conversation loop
- **Weather API Tool**: Integrated tool for retrieving weather data
- **Memory System**: Built-in conversation and context management
- **Natural Language Processing**: Simple location extraction from user queries

### Tools Available

#### weather_api

**Description**: Retrieves current weather information for a specified location

**Input Parameters**:
- `location` (string, required): The city name or location to get weather for
- `units` (string, optional): Temperature units (celsius, fahrenheit, kelvin), defaults to celsius

**Example Usage**:
```python
result = agent.execute_tool("weather_api", location="London", units="celsius")
```

**Sample Response**:
```json
{
  "success": true,
  "data": {
    "location": "London",
    "temperature": 18.5,
    "description": "partly cloudy",
    "humidity": 65,
    "wind_speed": 12.3,
    "units": "celsius"
  },
  "metadata": {
    "tool": "weather_api",
    "timestamp": "2025-09-20T10:30:00",
    "location_queried": "London",
    "units": "celsius"
  }
}
```

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

- All tools implement proper error handling and return structured error responses
- Uses custom exception hierarchy for tool-specific errors
- Logs all errors with appropriate severity levels
- Provides helpful error messages for users

### Documentation Standards

- Update this `agents.md` file when adding new tools or changing functionality
- Include usage examples for all tools
- Document any environment variables or configuration requirements
- Maintain a changelog for version updates

## Configuration

### Environment Variables

```bash
# Optional configuration
WEATHER_AGENT_LOG_LEVEL=INFO
WEATHER_AGENT_MAX_ITERATIONS=10
WEATHER_AGENT_ENABLE_HUMAN_FEEDBACK=false
```

### Configuration File

The agent can also be configured using a `config.json` file:

```json
{
  "name": "weather-agent",
  "description": "An agent that can retrieve current weather information for any location",
  "version": "1.0.0",
  "max_iterations": 10,
  "enable_human_feedback": false,
  "log_level": "INFO",
  "tools": {
    "weather_api": {
      "enabled": true,
      "timeout_seconds": 30,
      "retry_attempts": 3
    }
  }
}
```

## Usage Examples

### Basic Interaction

```python
from src.agent import WeatherAgent, AgentConfig

# Create configuration
config = AgentConfig(
    name="weather-agent",
    max_iterations=5,
    enable_human_feedback=False
)

# Initialize agent
agent = WeatherAgent(config)

# Process user input
response = agent.process_user_input("What's the weather in Tokyo?")
print(response)
```

### Using Tools Directly

```python
# Execute the weather tool directly
result = agent.execute_tool("weather_api", 
                          location="New York",
                          units="fahrenheit")

if result["success"]:
    weather_data = result["data"]
    print(f"Temperature in {weather_data['location']}: {weather_data['temperature']}°F")
else:
    print("Error:", result["error"])
```

### Interactive Session

```python
# Run an interactive session
agent.run_interactive_session()
```

**Example Conversation**:
```
🌤️ Welcome to weather-agent!
An agent that can retrieve current weather information for any location
Type 'quit', 'exit', or 'bye' to end the session.
Type 'help' to see what I can do.

You: What's the weather in London?

Weather Agent: 🌤️ Weather in London:
Temperature: 18.5°C
Conditions: Partly Cloudy
Humidity: 65%
Wind Speed: 12.3 km/h

You: Tell me the temperature in Tokyo in Fahrenheit

Weather Agent: 🌤️ Weather in Tokyo:
Temperature: 77.2°F
Conditions: Sunny
Humidity: 58%
Wind Speed: 8.1 km/h
```

## Testing Instructions

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_weather_agent.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run performance tests
python -m pytest tests/test_performance.py -v
```

### Test Categories

- **Unit Tests**: `tests/test_weather_agent.py` - Test individual components
- **Integration Tests**: `tests/test_integration.py` - Test component interactions
- **Performance Tests**: `tests/test_performance.py` - Test response times and resource usage
- **Security Tests**: `tests/test_security.py` - Test input sanitization and security measures

## Deployment

### Local Development

```bash
# Clone the repository
git clone <repository_url>
cd weather-agent

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
docker build -t weather-agent:latest .

# Run container
docker run -d --name weather-agent \
  -e WEATHER_AGENT_LOG_LEVEL=INFO \
  -p 8000:8000 \
  weather-agent:latest
```

## Security Considerations

### Input Validation

- All user inputs are validated before processing
- Location names are sanitized to prevent injection attacks
- Input length limits are enforced

### API Security

- Weather API calls include timeout mechanisms
- Rate limiting prevents abuse of external services
- Error messages don't expose internal system details

### Data Privacy

- Conversation history is stored locally only
- No personal data is transmitted to external services
- User data can be exported or deleted on request

## Troubleshooting

### Common Issues

**Agent won't start**:
- Check that Python 3.7+ is installed
- Verify that all dependencies are installed correctly
- Check the logs for specific error messages

**Weather data not available**:
- Verify internet connectivity
- Check if the location name is spelled correctly
- Try using a more specific location (e.g., "London, UK" instead of "London")

**Performance issues**:
- Monitor memory usage and adjust `max_iterations` if needed
- Check for network latency issues
- Consider enabling caching for frequently requested locations

### Debug Mode

Enable debug logging to get more detailed information:

```bash
export WEATHER_AGENT_LOG_LEVEL=DEBUG
python src/agent.py
```

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Implement your changes with tests
4. Run the test suite: `python -m pytest tests/ -v`
5. Update documentation as needed
6. Submit a pull request

### Adding New Features

1. Create new tool files in `src/tools/` if needed
2. Update the agent logic in `src/agent.py`
3. Add comprehensive tests in `tests/`
4. Update this `agents.md` file with new functionality
5. Add usage examples

### Code Review Guidelines

- All code must pass the test suite
- New features require documentation updates
- Security implications must be considered
- Performance impact should be evaluated

## Changelog

### Version 1.0.0 (2025-09-20)
- Initial release
- Implemented weather API tool
- Added natural language processing for location extraction
- Created comprehensive test suite
- Added interactive conversation interface
- Implemented memory system for conversation history

---

*This file is automatically maintained by the agent-builder framework. Manual edits may be overwritten during updates.*
