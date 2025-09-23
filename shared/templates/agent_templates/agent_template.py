#!/usr/bin/env python3
"""
{{agent_name}} - AI Agent Template

This is a template for creating AI agents using the agent-builder framework.
It incorporates best practices from OpenAI, Anthropic, Google, and the agents.md specification.

Author: {{author_name}}
Created: {{creation_date}}
"""

import logging
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


# Configure logging for the agent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration class for the agent."""
    name: str = "{{agent_name}}"
    description: str = "{{agent_description}}"
    version: str = "1.0.0"
    max_iterations: int = 10
    enable_human_feedback: bool = {{enable_human_feedback}}
    log_level: str = "INFO"


class Tool(ABC):
    """Abstract base class for agent tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        pass
    
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
            "timestamp": self._get_timestamp(),
            "metadata": metadata or {}
        }
        self.conversation_history.append(message)
        logger.debug(f"Added message: {role} - {content[:100]}...")
    
    def add_tool_result(self, tool_name: str, result: Dict[str, Any]):
        """Add a tool execution result to memory."""
        tool_result = {
            "tool": tool_name,
            "result": result,
            "timestamp": self._get_timestamp()
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
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


class {{agent_class_name}}:
    """
    {{agent_description}}
    
    This agent follows best practices for:
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
        # TODO: Add your tools here
        # Example:
        # self.add_tool(ExampleTool())
        pass
    
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
            # Validate input
            if not tool.validate_input(**kwargs):
                error_msg = f"Invalid input for tool '{tool_name}'"
                self.logger.error(error_msg)
                return {"error": error_msg, "success": False}
            
            # Execute tool
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
            # TODO: Implement your agent's main logic here
            # This is where you would:
            # 1. Analyze the user input
            # 2. Decide which tools to use
            # 3. Execute tools as needed
            # 4. Generate a response
            
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
        # TODO: Implement your response generation logic
        # This is a placeholder implementation
        
        context = self.memory.get_context()
        
        # Example response logic
        if "help" in user_input.lower():
            return self._get_help_message()
        
        return f"I received your message: '{user_input}'. This is a template response."
    
    def _get_help_message(self) -> str:
        """Generate a help message listing available tools and capabilities."""
        help_msg = f"I am {self.config.name} - {self.config.description}\n\n"
        help_msg += "Available tools:\n"
        
        for tool_name, tool in self.tools.items():
            help_msg += f"- {tool_name}: {tool.description}\n"
        
        if not self.tools:
            help_msg += "No tools are currently available.\n"
        
        return help_msg
    
    def run_interactive_session(self):
        """Run an interactive session with the user."""
        self.logger.info("Starting interactive session")
        self.is_running = True
        
        print(f"Welcome to {self.config.name}!")
        print(f"{self.config.description}")
        print("Type 'quit' or 'exit' to end the session.\n")
        
        try:
            while self.is_running and self.iteration_count < self.config.max_iterations:
                user_input = input("> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                response = self.process_user_input(user_input)
                print(f"\n{response}\n")
                
                self.iteration_count += 1
                
                # Human-in-the-loop checkpoint
                if self.config.enable_human_feedback and self.iteration_count % 5 == 0:
                    feedback = input("How am I doing? (Press Enter to continue): ").strip()
                    if feedback:
                        self.memory.add_message("feedback", feedback)
                        print("Thank you for the feedback!\n")
        
        except KeyboardInterrupt:
            print("\nSession interrupted by user.")
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
    """Main function to run the agent."""
    # Create agent configuration
    config = AgentConfig()
    
    # Initialize the agent
    agent = {{agent_class_name}}(config)
    
    # Run interactive session
    agent.run_interactive_session()
    
    # Export conversation for review
    conversation_data = agent.export_conversation()
    with open(f"{config.name}_conversation.json", "w") as f:
        json.dump(conversation_data, f, indent=2)
    
    print(f"Conversation exported to {config.name}_conversation.json")


if __name__ == "__main__":
    main()
