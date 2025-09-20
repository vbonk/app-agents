#!/usr/bin/env python3
"""
{{tool_name}} - Tool Template

This is a template for creating tools for AI agents using the agent-builder framework.
It follows best practices for tool design, documentation, and error handling.

Author: {{author_name}}
Created: {{creation_date}}
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


@dataclass
class ToolConfig:
    """Configuration for the tool."""
    name: str = "{{tool_name}}"
    description: str = "{{tool_description}}"
    version: str = "1.0.0"
    timeout_seconds: int = 30
    retry_attempts: int = 3


class ToolError(Exception):
    """Custom exception for tool-related errors."""
    pass


class ToolValidationError(ToolError):
    """Exception raised when tool input validation fails."""
    pass


class ToolExecutionError(ToolError):
    """Exception raised when tool execution fails."""
    pass


class {{tool_class_name}}:
    """
    {{tool_description}}
    
    This tool follows best practices for:
    - Clear input/output schemas
    - Comprehensive error handling
    - Detailed logging
    - Input validation
    - Retry logic for transient failures
    """
    
    def __init__(self, config: Optional[ToolConfig] = None):
        self.config = config or ToolConfig()
        self.logger = logging.getLogger(f"{__name__}.{self.config.name}")
        self.execution_count = 0
        self.success_count = 0
        self.error_count = 0
        
        self.logger.info(f"Initialized {self.config.name} v{self.config.version}")
    
    def get_schema(self) -> Dict[str, Any]:
        """
        Return the input/output schema for this tool.
        
        This schema is used by the agent to understand how to use the tool
        and by documentation generators to create API docs.
        """
        return {
            "name": self.config.name,
            "description": self.config.description,
            "version": self.config.version,
            "parameters": {
                "type": "object",
                "properties": {
                    # TODO: Define your input parameters here
                    # Example:
                    # "query": {
                    #     "type": "string",
                    #     "description": "The search query to process",
                    #     "required": True
                    # },
                    # "limit": {
                    #     "type": "integer",
                    #     "description": "Maximum number of results to return",
                    #     "default": 10,
                    #     "minimum": 1,
                    #     "maximum": 100
                    # }
                },
                "required": [
                    # TODO: List required parameters here
                    # Example: "query"
                ]
            },
            "returns": {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "description": "Whether the tool execution was successful"
                    },
                    "data": {
                        "type": "object",
                        "description": "The main result data from the tool"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Additional metadata about the execution"
                    },
                    "error": {
                        "type": "string",
                        "description": "Error message if execution failed"
                    }
                }
            },
            "examples": [
                # TODO: Add usage examples here
                # {
                #     "input": {"query": "example search", "limit": 5},
                #     "output": {
                #         "success": True,
                #         "data": {"results": []},
                #         "metadata": {"execution_time": 0.5}
                #     }
                # }
            ]
        }
    
    def validate_input(self, **kwargs) -> bool:
        """
        Validate input parameters against the tool's schema.
        
        Args:
            **kwargs: Input parameters to validate
            
        Returns:
            bool: True if validation passes
            
        Raises:
            ToolValidationError: If validation fails
        """
        schema = self.get_schema()
        required_params = schema["parameters"].get("required", [])
        properties = schema["parameters"].get("properties", {})
        
        # Check required parameters
        for param in required_params:
            if param not in kwargs:
                raise ToolValidationError(f"Missing required parameter: {param}")
        
        # Validate parameter types and constraints
        for param_name, param_value in kwargs.items():
            if param_name in properties:
                param_schema = properties[param_name]
                
                # Type validation
                expected_type = param_schema.get("type")
                if expected_type == "string" and not isinstance(param_value, str):
                    raise ToolValidationError(f"Parameter '{param_name}' must be a string")
                elif expected_type == "integer" and not isinstance(param_value, int):
                    raise ToolValidationError(f"Parameter '{param_name}' must be an integer")
                elif expected_type == "number" and not isinstance(param_value, (int, float)):
                    raise ToolValidationError(f"Parameter '{param_name}' must be a number")
                elif expected_type == "boolean" and not isinstance(param_value, bool):
                    raise ToolValidationError(f"Parameter '{param_name}' must be a boolean")
                
                # Range validation for numbers
                if expected_type in ["integer", "number"]:
                    if "minimum" in param_schema and param_value < param_schema["minimum"]:
                        raise ToolValidationError(f"Parameter '{param_name}' must be >= {param_schema['minimum']}")
                    if "maximum" in param_schema and param_value > param_schema["maximum"]:
                        raise ToolValidationError(f"Parameter '{param_name}' must be <= {param_schema['maximum']}")
        
        return True
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with the given parameters.
        
        Args:
            **kwargs: Input parameters for the tool
            
        Returns:
            Dict[str, Any]: Result dictionary with success, data, metadata, and error fields
        """
        self.execution_count += 1
        start_time = self._get_timestamp()
        
        try:
            # Validate input
            self.validate_input(**kwargs)
            
            self.logger.info(f"Executing {self.config.name} with parameters: {kwargs}")
            
            # Execute the main tool logic with retry
            result_data = self._execute_with_retry(**kwargs)
            
            # Prepare successful result
            result = {
                "success": True,
                "data": result_data,
                "metadata": {
                    "tool_name": self.config.name,
                    "tool_version": self.config.version,
                    "execution_time": self._get_timestamp() - start_time,
                    "execution_count": self.execution_count,
                    "parameters": kwargs
                }
            }
            
            self.success_count += 1
            self.logger.info(f"Successfully executed {self.config.name}")
            return result
            
        except ToolValidationError as e:
            self.error_count += 1
            error_msg = f"Validation error in {self.config.name}: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_result(error_msg, kwargs, start_time)
            
        except ToolExecutionError as e:
            self.error_count += 1
            error_msg = f"Execution error in {self.config.name}: {str(e)}"
            self.logger.error(error_msg)
            return self._create_error_result(error_msg, kwargs, start_time)
            
        except Exception as e:
            self.error_count += 1
            error_msg = f"Unexpected error in {self.config.name}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return self._create_error_result(error_msg, kwargs, start_time)
    
    def _execute_with_retry(self, **kwargs) -> Any:
        """
        Execute the main tool logic with retry mechanism.
        
        Args:
            **kwargs: Input parameters for the tool
            
        Returns:
            Any: The result data from the tool execution
            
        Raises:
            ToolExecutionError: If all retry attempts fail
        """
        last_error = None
        
        for attempt in range(self.config.retry_attempts):
            try:
                return self._execute_main_logic(**kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.config.retry_attempts - 1:
                    self.logger.warning(f"Attempt {attempt + 1} failed, retrying: {str(e)}")
                else:
                    self.logger.error(f"All {self.config.retry_attempts} attempts failed")
        
        raise ToolExecutionError(f"Failed after {self.config.retry_attempts} attempts: {str(last_error)}")
    
    def _execute_main_logic(self, **kwargs) -> Any:
        """
        Main execution logic for the tool.
        
        This method should be implemented by subclasses or modified for specific tools.
        
        Args:
            **kwargs: Input parameters for the tool
            
        Returns:
            Any: The result data from the tool execution
            
        Raises:
            ToolExecutionError: If execution fails
        """
        # TODO: Implement your tool's main logic here
        # Example:
        # if "query" in kwargs:
        #     return self._process_query(kwargs["query"])
        # else:
        #     raise ToolExecutionError("No query provided")
        
        # Placeholder implementation
        self.logger.info("Executing placeholder logic")
        return {
            "message": "This is a template tool. Please implement the _execute_main_logic method.",
            "parameters_received": kwargs
        }
    
    def _create_error_result(self, error_msg: str, parameters: Dict[str, Any], start_time: float) -> Dict[str, Any]:
        """Create a standardized error result."""
        return {
            "success": False,
            "data": None,
            "error": error_msg,
            "metadata": {
                "tool_name": self.config.name,
                "tool_version": self.config.version,
                "execution_time": self._get_timestamp() - start_time,
                "execution_count": self.execution_count,
                "parameters": parameters
            }
        }
    
    def _get_timestamp(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics for this tool."""
        return {
            "tool_name": self.config.name,
            "total_executions": self.execution_count,
            "successful_executions": self.success_count,
            "failed_executions": self.error_count,
            "success_rate": self.success_count / max(self.execution_count, 1) * 100
        }
    
    def reset_statistics(self):
        """Reset execution statistics."""
        self.execution_count = 0
        self.success_count = 0
        self.error_count = 0
        self.logger.info(f"Reset statistics for {self.config.name}")


# Example usage and testing
def main():
    """Example usage of the tool template."""
    # Create tool configuration
    config = ToolConfig(
        name="example_tool",
        description="An example tool for demonstration"
    )
    
    # Initialize the tool
    tool = {{tool_class_name}}(config)
    
    # Print the tool schema
    print("Tool Schema:")
    import json
    print(json.dumps(tool.get_schema(), indent=2))
    
    # Test the tool
    print("\nTesting tool execution:")
    result = tool.execute(test_param="example_value")
    print(json.dumps(result, indent=2))
    
    # Print statistics
    print("\nTool Statistics:")
    print(json.dumps(tool.get_statistics(), indent=2))


if __name__ == "__main__":
    main()
