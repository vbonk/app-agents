#!/usr/bin/env python3
"""
Weather Agent - Example AI Agent Implementation

This is a complete example of an AI agent created using the agent-builder framework.
It demonstrates best practices for agent design, tool integration, and error handling.

Author: Agent-Builder Framework
Created: 2025-09-20
"""

import logging
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

# Configure logging for the agent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration class for the weather agent."""
    name: str = "weather-agent"
    description: str = "An agent that can retrieve current weather information for any location"
    version: str = "1.0.0"
    max_iterations: int = 10
    enable_human_feedback: bool = False
    log_level: str = "INFO"


class Tool:
    """Base class for agent tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        raise NotImplementedError("Subclasses must implement execute method")
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters for the tool."""
        return True
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the input/output schema for this tool."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {},
            "returns": {}
        }


class WeatherAPITool(Tool):
    """Tool for retrieving weather information from a weather API."""
    
    def __init__(self):
        super().__init__(
            name="weather_api",
            description="Retrieves current weather information for a specified location"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        """Return the input/output schema for the weather API tool."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name or location to get weather for",
                        "required": True
                    },
                    "units": {
                        "type": "string",
                        "description": "Temperature units (celsius, fahrenheit, kelvin)",
                        "default": "celsius",
                        "enum": ["celsius", "fahrenheit", "kelvin"]
                    }
                },
                "required": ["location"]
            },
            "returns": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "data": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string"},
                            "temperature": {"type": "number"},
                            "description": {"type": "string"},
                            "humidity": {"type": "number"},
                            "wind_speed": {"type": "number"}
                        }
                    },
                    "error": {"type": "string"}
                }
            }
        }
    
    def validate_input(self, **kwargs) -> bool:
        """Validate input parameters."""
        if "location" not in kwargs:
            return False
        
        location = kwargs["location"]
        if not isinstance(location, str) or len(location.strip()) == 0:
            return False
        
        units = kwargs.get("units", "celsius")
        if units not in ["celsius", "fahrenheit", "kelvin"]:
            return False
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the weather API call."""
        try:
            if not self.validate_input(**kwargs):
                return {
                    "success": False,
                    "error": "Invalid input parameters"
                }
            
            location = kwargs["location"].strip()
            units = kwargs.get("units", "celsius")
            
            self.logger.info(f"Fetching weather for {location} in {units}")
            
            # Simulate API call (in real implementation, this would call an actual weather API)
            weather_data = self._simulate_weather_api(location, units)
            
            return {
                "success": True,
                "data": weather_data,
                "metadata": {
                    "tool": self.name,
                    "timestamp": datetime.now().isoformat(),
                    "location_queried": location,
                    "units": units
                }
            }
            
        except Exception as e:
            error_msg = f"Error fetching weather data: {str(e)}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }
    
    def _simulate_weather_api(self, location: str, units: str) -> Dict[str, Any]:
        """Simulate a weather API response."""
        # In a real implementation, this would make an HTTP request to a weather service
        import random
        
        # Simulate different weather conditions based on location
        base_temp = 20  # Celsius
        if "arctic" in location.lower() or "alaska" in location.lower():
            base_temp = -10
        elif "desert" in location.lower() or "sahara" in location.lower():
            base_temp = 35
        elif "tropical" in location.lower() or "hawaii" in location.lower():
            base_temp = 28
        
        temperature = base_temp + random.randint(-5, 5)
        
        # Convert temperature based on units
        if units == "fahrenheit":
            temperature = (temperature * 9/5) + 32
        elif units == "kelvin":
            temperature = temperature + 273.15
        
        conditions = ["sunny", "cloudy", "partly cloudy", "rainy", "stormy"]
        
        return {
            "location": location,
            "temperature": round(temperature, 1),
            "description": random.choice(conditions),
            "humidity": random.randint(30, 90),
            "wind_speed": round(random.uniform(0, 25), 1),
            "units": units
        }


class AgentMemory:
    """Simple memory system for the agent."""
    
    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.tool_results: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to the conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.conversation_history.append(message)
        logger.debug(f"Added message: {role} - {content[:100]}...")
    
    def add_tool_result(self, tool_name: str, result: Dict[str, Any]):
        """Add a tool execution result to memory."""
        tool_result = {
            "tool": tool_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        self.tool_results.append(tool_result)
        logger.debug(f"Added tool result: {tool_name}")
    
    def get_context(self) -> Dict[str, Any]:
        """Get the current context for the agent."""
        return {
            "conversation_history": self.conversation_history[-5:],  # Last 5 messages
            "context": self.context,
            "recent_tool_results": self.tool_results[-3:]  # Last 3 tool results
        }


class WeatherAgent:
    """
    Weather Agent - An AI agent that provides weather information for any location.
    
    This agent demonstrates best practices for:
    - Modular tool design
    - Comprehensive logging
    - Error handling and recovery
    - Human-in-the-loop checkpoints
    - Clear documentation
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.memory = AgentMemory()
        self.tools: Dict[str, Tool] = {}
        self.iteration_count = 0
        self.is_running = False
        
        # Set up logging
        self.logger = logging.getLogger(f"{__name__}.{self.config.name}")
        self.logger.setLevel(getattr(logging, self.config.log_level))
        
        # Initialize tools
        self._initialize_tools()
        
        self.logger.info(f"Initialized {self.config.name} v{self.config.version}")
    
    def _initialize_tools(self):
        """Initialize all tools for this agent."""
        self.add_tool(WeatherAPITool())
    
    def add_tool(self, tool: Tool):
        """Add a tool to the agent's toolkit."""
        self.tools[tool.name] = tool
        self.logger.info(f"Added tool: {tool.name}")
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a specific tool with error handling."""
        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
            self.logger.error(error_msg)
            return {"error": error_msg, "success": False}
        
        tool = self.tools[tool_name]
        
        try:
            self.logger.info(f"Executing tool: {tool_name}")
            result = tool.execute(**kwargs)
            
            # Add result to memory
            self.memory.add_tool_result(tool_name, result)
            
            # Ensure result has success flag
            if "success" not in result:
                result["success"] = True
            
            self.logger.info(f"Tool '{tool_name}' executed successfully")
            return result
            
        except Exception as e:
            error_msg = f"Error executing tool '{tool_name}': {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {"error": error_msg, "success": False}
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and return a response."""
        self.logger.info(f"Processing user input: {user_input[:100]}...")
        
        # Add user message to memory
        self.memory.add_message("user", user_input)
        
        try:
            response = self._generate_response(user_input)
            
            # Add agent response to memory
            self.memory.add_message("assistant", response)
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing user input: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return f"I apologize, but I encountered an error: {error_msg}"
    
    def _generate_response(self, user_input: str) -> str:
        """Generate a response based on user input and current context."""
        user_input_lower = user_input.lower()
        
        # Handle help requests
        if any(word in user_input_lower for word in ["help", "what can you do", "commands"]):
            return self._get_help_message()
        
        # Handle weather requests
        if any(word in user_input_lower for word in ["weather", "temperature", "forecast"]):
            return self._handle_weather_request(user_input)
        
        # Handle greetings
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "Hello! I'm the Weather Agent. I can help you get current weather information for any location. Just ask me about the weather in a specific city or location!"
        
        # Default response
        return "I'm a weather agent that can provide current weather information. Try asking me something like 'What's the weather in New York?' or type 'help' for more information."
    
    def _handle_weather_request(self, user_input: str) -> str:
        """Handle weather-related requests."""
        # Simple location extraction (in a real implementation, this would be more sophisticated)
        location = self._extract_location(user_input)
        
        if not location:
            return "I'd be happy to help you with weather information! Please specify a location, for example: 'What's the weather in London?' or 'Tell me the weather in Tokyo'."
        
        # Extract units preference if mentioned
        units = "celsius"
        if any(word in user_input.lower() for word in ["fahrenheit", "°f", "f"]):
            units = "fahrenheit"
        elif any(word in user_input.lower() for word in ["kelvin", "k"]):
            units = "kelvin"
        
        # Execute weather tool
        result = self.execute_tool("weather_api", location=location, units=units)
        
        if result.get("success"):
            weather_data = result["data"]
            return self._format_weather_response(weather_data)
        else:
            error = result.get("error", "Unknown error occurred")
            return f"I'm sorry, I couldn't retrieve the weather information for {location}. Error: {error}"
    
    def _extract_location(self, user_input: str) -> Optional[str]:
        """Extract location from user input."""
        # Simple location extraction - in a real implementation, this would use NLP
        import re
        
        # Look for patterns like "weather in [location]" or "weather for [location]"
        patterns = [
            r"weather (?:in|for|at) ([^?]+)",
            r"temperature (?:in|for|at) ([^?]+)",
            r"forecast (?:in|for|at) ([^?]+)",
            r"what'?s (?:the )?weather (?:like )?(?:in|for|at) ([^?]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                location = match.group(1).strip()
                # Clean up common words
                location = re.sub(r'\b(like|today|now|currently)\b', '', location).strip()
                if location:
                    return location
        
        # If no pattern matches, look for city names (simplified approach)
        words = user_input.split()
        # This is a very basic approach - in reality, you'd use a proper NER system
        potential_locations = []
        for i, word in enumerate(words):
            if word.lower() in ["weather", "temperature", "forecast"]:
                # Look for the next few words as potential location
                if i + 1 < len(words):
                    potential_locations.extend(words[i+1:i+4])
        
        if potential_locations:
            # Join and clean up
            location = " ".join(potential_locations)
            location = re.sub(r'[?!.,]', '', location).strip()
            if len(location) > 2:  # Basic validation
                return location
        
        return None
    
    def _format_weather_response(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data into a human-readable response."""
        location = weather_data.get("location", "Unknown location")
        temp = weather_data.get("temperature", "N/A")
        description = weather_data.get("description", "N/A")
        humidity = weather_data.get("humidity", "N/A")
        wind_speed = weather_data.get("wind_speed", "N/A")
        units = weather_data.get("units", "celsius")
        
        # Format temperature unit
        temp_unit = "°C"
        if units == "fahrenheit":
            temp_unit = "°F"
        elif units == "kelvin":
            temp_unit = "K"
        
        response = f"🌤️ Weather in {location}:\n"
        response += f"Temperature: {temp}{temp_unit}\n"
        response += f"Conditions: {description.title()}\n"
        response += f"Humidity: {humidity}%\n"
        response += f"Wind Speed: {wind_speed} km/h"
        
        return response
    
    def _get_help_message(self) -> str:
        """Generate a help message listing available capabilities."""
        help_msg = f"🤖 {self.config.name} v{self.config.version}\n"
        help_msg += f"{self.config.description}\n\n"
        help_msg += "I can help you with:\n"
        help_msg += "• Current weather information for any city or location\n"
        help_msg += "• Temperature in Celsius, Fahrenheit, or Kelvin\n"
        help_msg += "• Weather conditions, humidity, and wind speed\n\n"
        help_msg += "Example commands:\n"
        help_msg += "• 'What's the weather in London?'\n"
        help_msg += "• 'Tell me the temperature in Tokyo in Fahrenheit'\n"
        help_msg += "• 'Weather forecast for New York'\n\n"
        help_msg += "Available tools:\n"
        
        for tool_name, tool in self.tools.items():
            help_msg += f"• {tool_name}: {tool.description}\n"
        
        return help_msg
    
    def run_interactive_session(self):
        """Run an interactive session with the user."""
        self.logger.info("Starting interactive session")
        self.is_running = True
        
        print(f"🌤️ Welcome to {self.config.name}!")
        print(f"{self.config.description}")
        print("Type 'quit', 'exit', or 'bye' to end the session.")
        print("Type 'help' to see what I can do.\n")
        
        try:
            while self.is_running and self.iteration_count < self.config.max_iterations:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Weather Agent: Goodbye! Stay safe and have a great day! 🌈")
                    break
                
                if not user_input:
                    continue
                
                response = self.process_user_input(user_input)
                print(f"\nWeather Agent: {response}\n")
                
                self.iteration_count += 1
                
                # Human-in-the-loop checkpoint
                if self.config.enable_human_feedback and self.iteration_count % 5 == 0:
                    feedback = input("How am I doing? (Press Enter to continue): ").strip()
                    if feedback:
                        self.memory.add_message("feedback", feedback)
                        print("Thank you for the feedback! I'll keep improving. 😊\n")
        
        except KeyboardInterrupt:
            print("\n\nWeather Agent: Session interrupted. Goodbye! 👋")
        except Exception as e:
            self.logger.error(f"Error in interactive session: {str(e)}", exc_info=True)
            print(f"An error occurred: {str(e)}")
        finally:
            self.is_running = False
            self.logger.info("Interactive session ended")
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            "name": self.config.name,
            "version": self.config.version,
            "is_running": self.is_running,
            "iteration_count": self.iteration_count,
            "tools_count": len(self.tools),
            "memory_size": len(self.memory.conversation_history)
        }
    
    def export_conversation(self) -> Dict[str, Any]:
        """Export the conversation history for analysis or debugging."""
        return {
            "agent_config": {
                "name": self.config.name,
                "version": self.config.version,
                "description": self.config.description
            },
            "conversation_history": self.memory.conversation_history,
            "tool_results": self.memory.tool_results,
            "status": self.get_status()
        }


def main():
    """Main function to run the weather agent."""
    # Create agent configuration
    config = AgentConfig()
    
    # Initialize the agent
    agent = WeatherAgent(config)
    
    # Run interactive session
    agent.run_interactive_session()
    
    # Export conversation for review
    conversation_data = agent.export_conversation()
    filename = f"{config.name}_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(conversation_data, f, indent=2)
    
    print(f"Conversation exported to {filename}")


if __name__ == "__main__":
    main()
