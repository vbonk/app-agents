#!/usr/bin/env python3
"""
Test Suite for Weather Agent

This test suite demonstrates comprehensive testing practices for AI agents
created with the agent-builder framework.

Author: Agent-Builder Framework
Created: 2025-09-20
"""

import unittest
import json
import tempfile
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List
import logging

# Add the src directory to the path so we can import the agent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import WeatherAgent, AgentConfig, WeatherAPITool, AgentMemory

# Suppress logging during tests unless debugging
logging.getLogger().setLevel(logging.CRITICAL)


class TestAgentBase(unittest.TestCase):
    """Base test class for agent testing with common utilities."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_data_dir = tempfile.mkdtemp()
        self.mock_config = self._create_mock_config()
        
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up temporary files
        import shutil
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
    def _create_mock_config(self) -> AgentConfig:
        """Create a mock configuration for testing."""
        return AgentConfig(
            name="test_weather_agent",
            description="Test weather agent for unit testing",
            version="1.0.0",
            max_iterations=5,
            enable_human_feedback=False,
            log_level="CRITICAL"
        )
    
    def assert_valid_response(self, response: Dict[str, Any]):
        """Assert that a response has the expected structure."""
        self.assertIsInstance(response, dict)
        self.assertIn("success", response)
        self.assertIsInstance(response["success"], bool)
        
        if response["success"]:
            self.assertIn("data", response)
        else:
            self.assertIn("error", response)
    
    def assert_tool_schema_valid(self, schema: Dict[str, Any]):
        """Assert that a tool schema is valid."""
        required_fields = ["name", "description", "parameters", "returns"]
        for field in required_fields:
            self.assertIn(field, schema, f"Schema missing required field: {field}")
        
        # Validate parameters structure
        params = schema["parameters"]
        self.assertIn("type", params)
        self.assertEqual(params["type"], "object")
        self.assertIn("properties", params)
        
        # Validate returns structure
        returns = schema["returns"]
        self.assertIn("type", returns)
        self.assertEqual(returns["type"], "object")


class TestWeatherAgent(TestAgentBase):
    """Test cases for the WeatherAgent."""
    
    def setUp(self):
        """Set up test fixtures for agent tests."""
        super().setUp()
        self.agent = WeatherAgent(self.mock_config)
    
    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.config.name, "test_weather_agent")
        self.assertIsInstance(self.agent.tools, dict)
        self.assertIn("weather_api", self.agent.tools)
        self.assertIsInstance(self.agent.memory, AgentMemory)
    
    def test_agent_configuration(self):
        """Test agent configuration handling."""
        # Test default configuration
        default_agent = WeatherAgent()
        self.assertEqual(default_agent.config.name, "weather-agent")
        self.assertEqual(default_agent.config.max_iterations, 10)
        
        # Test custom configuration
        self.assertEqual(self.agent.config.name, "test_weather_agent")
        self.assertEqual(self.agent.config.max_iterations, 5)
    
    def test_process_user_input_greeting(self):
        """Test greeting input processing."""
        greetings = ["hello", "hi", "hey", "good morning"]
        for greeting in greetings:
            response = self.agent.process_user_input(greeting)
            self.assertIsInstance(response, str)
            self.assertIn("Weather Agent", response)
            self.assertGreater(len(response), 0)
    
    def test_process_user_input_help(self):
        """Test help command processing."""
        help_commands = ["help", "what can you do", "commands"]
        for help_cmd in help_commands:
            response = self.agent.process_user_input(help_cmd)
            self.assertIn("weather", response.lower())
            self.assertIn("tool", response.lower())
    
    def test_weather_request_processing(self):
        """Test weather request processing."""
        with patch.object(self.agent, 'execute_tool') as mock_execute:
            mock_execute.return_value = {
                "success": True,
                "data": {
                    "location": "London",
                    "temperature": 20.5,
                    "description": "sunny",
                    "humidity": 60,
                    "wind_speed": 10.0,
                    "units": "celsius"
                }
            }
            
            response = self.agent.process_user_input("What's the weather in London?")
            self.assertIn("London", response)
            self.assertIn("20.5", response)
            self.assertIn("sunny", response.lower())
            mock_execute.assert_called_once()
    
    def test_location_extraction(self):
        """Test location extraction from user input."""
        test_cases = [
            ("What's the weather in London?", "London"),
            ("Tell me the weather for New York", "New York"),
            ("Weather in Tokyo please", "Tokyo"),
            ("How's the weather at Paris", "Paris"),
            ("What's the temperature in San Francisco", "San Francisco"),
        ]
        
        for user_input, expected_location in test_cases:
            location = self.agent._extract_location(user_input)
            self.assertEqual(location.lower(), expected_location.lower())
    
    def test_location_extraction_no_location(self):
        """Test location extraction when no location is provided."""
        test_cases = [
            "What's the weather?",
            "Tell me the temperature",
            "How's the weather today?",
            "Weather please"
        ]
        
        for user_input in test_cases:
            location = self.agent._extract_location(user_input)
            self.assertIsNone(location)
    
    def test_memory_functionality(self):
        """Test agent memory system."""
        # Test adding messages
        self.agent.memory.add_message("user", "test message")
        context = self.agent.memory.get_context()
        self.assertIn("conversation_history", context)
        self.assertEqual(len(context["conversation_history"]), 1)
        self.assertEqual(context["conversation_history"][0]["content"], "test message")
        
        # Test adding tool results
        self.agent.memory.add_tool_result("test_tool", {"result": "success"})
        context = self.agent.memory.get_context()
        self.assertIn("recent_tool_results", context)
        self.assertEqual(len(context["recent_tool_results"]), 1)
    
    def test_tool_management(self):
        """Test tool addition and management."""
        # Test that weather_api tool is added by default
        self.assertIn("weather_api", self.agent.tools)
        
        # Test adding a new tool
        mock_tool = Mock()
        mock_tool.name = "test_tool"
        mock_tool.description = "Test tool"
        
        self.agent.add_tool(mock_tool)
        self.assertIn("test_tool", self.agent.tools)
        self.assertEqual(self.agent.tools["test_tool"], mock_tool)
    
    def test_error_handling(self):
        """Test agent error handling."""
        with patch.object(self.agent, '_generate_response', side_effect=Exception("Test error")):
            response = self.agent.process_user_input("test")
            self.assertIn("error", response.lower())
            self.assertIn("apologize", response.lower())
    
    def test_status_reporting(self):
        """Test agent status reporting."""
        status = self.agent.get_status()
        expected_fields = ["name", "version", "is_running", "iteration_count", "tools_count", "memory_size"]
        for field in expected_fields:
            self.assertIn(field, status)
        
        self.assertEqual(status["name"], self.agent.config.name)
        self.assertEqual(status["version"], self.agent.config.version)
        self.assertFalse(status["is_running"])
        self.assertEqual(status["tools_count"], len(self.agent.tools))
    
    def test_conversation_export(self):
        """Test conversation export functionality."""
        # Add some conversation data
        self.agent.process_user_input("Hello")
        self.agent.process_user_input("What's the weather in London?")
        
        export_data = self.agent.export_conversation()
        
        required_fields = ["agent_config", "conversation_history", "tool_results", "status"]
        for field in required_fields:
            self.assertIn(field, export_data)
        
        # Check agent config
        config = export_data["agent_config"]
        self.assertEqual(config["name"], self.agent.config.name)
        self.assertEqual(config["version"], self.agent.config.version)
        
        # Check conversation history
        history = export_data["conversation_history"]
        self.assertGreater(len(history), 0)


class TestWeatherAPITool(TestAgentBase):
    """Test cases for the WeatherAPITool."""
    
    def setUp(self):
        """Set up test fixtures for tool tests."""
        super().setUp()
        self.tool = WeatherAPITool()
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly."""
        self.assertIsNotNone(self.tool)
        self.assertEqual(self.tool.name, "weather_api")
        self.assertIn("weather", self.tool.description.lower())
    
    def test_tool_schema(self):
        """Test tool schema generation."""
        schema = self.tool.get_schema()
        self.assert_tool_schema_valid(schema)
        
        # Check specific schema details
        params = schema["parameters"]["properties"]
        self.assertIn("location", params)
        self.assertIn("units", params)
        
        # Check required parameters
        required = schema["parameters"]["required"]
        self.assertIn("location", required)
    
    def test_input_validation_success(self):
        """Test successful input validation."""
        valid_inputs = [
            {"location": "London"},
            {"location": "New York", "units": "celsius"},
            {"location": "Tokyo", "units": "fahrenheit"},
            {"location": "Paris", "units": "kelvin"},
        ]
        
        for valid_input in valid_inputs:
            self.assertTrue(self.tool.validate_input(**valid_input))
    
    def test_input_validation_failure(self):
        """Test input validation failure scenarios."""
        invalid_inputs = [
            {},  # Missing location
            {"location": ""},  # Empty location
            {"location": "   "},  # Whitespace only location
            {"location": 123},  # Non-string location
            {"location": "London", "units": "invalid"},  # Invalid units
        ]
        
        for invalid_input in invalid_inputs:
            self.assertFalse(self.tool.validate_input(**invalid_input))
    
    def test_successful_execution(self):
        """Test successful tool execution."""
        result = self.tool.execute(location="London", units="celsius")
        self.assert_valid_response(result)
        self.assertTrue(result["success"])
        
        # Check data structure
        data = result["data"]
        expected_fields = ["location", "temperature", "description", "humidity", "wind_speed", "units"]
        for field in expected_fields:
            self.assertIn(field, data)
        
        # Check data types
        self.assertIsInstance(data["temperature"], (int, float))
        self.assertIsInstance(data["humidity"], int)
        self.assertIsInstance(data["wind_speed"], (int, float))
        self.assertEqual(data["units"], "celsius")
    
    def test_execution_with_different_units(self):
        """Test tool execution with different temperature units."""
        units_tests = ["celsius", "fahrenheit", "kelvin"]
        
        for units in units_tests:
            result = self.tool.execute(location="London", units=units)
            self.assertTrue(result["success"])
            self.assertEqual(result["data"]["units"], units)
    
    def test_execution_with_invalid_input(self):
        """Test tool execution with invalid input."""
        result = self.tool.execute()  # No parameters
        self.assert_valid_response(result)
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_weather_simulation(self):
        """Test the weather simulation logic."""
        # Test different locations to ensure variation
        locations = ["London", "Arctic", "Sahara Desert", "Hawaii", "Alaska"]
        
        for location in locations:
            weather_data = self.tool._simulate_weather_api(location, "celsius")
            
            # Check that all required fields are present
            required_fields = ["location", "temperature", "description", "humidity", "wind_speed", "units"]
            for field in required_fields:
                self.assertIn(field, weather_data)
            
            # Check reasonable value ranges
            self.assertIsInstance(weather_data["temperature"], (int, float))
            self.assertGreaterEqual(weather_data["humidity"], 0)
            self.assertLessEqual(weather_data["humidity"], 100)
            self.assertGreaterEqual(weather_data["wind_speed"], 0)


class TestAgentMemory(TestAgentBase):
    """Test cases for the AgentMemory system."""
    
    def setUp(self):
        """Set up test fixtures for memory tests."""
        super().setUp()
        self.memory = AgentMemory()
    
    def test_memory_initialization(self):
        """Test memory system initialization."""
        self.assertIsInstance(self.memory.conversation_history, list)
        self.assertIsInstance(self.memory.context, dict)
        self.assertIsInstance(self.memory.tool_results, list)
        self.assertEqual(len(self.memory.conversation_history), 0)
        self.assertEqual(len(self.memory.tool_results), 0)
    
    def test_add_message(self):
        """Test adding messages to memory."""
        self.memory.add_message("user", "Hello")
        self.memory.add_message("assistant", "Hi there!")
        
        self.assertEqual(len(self.memory.conversation_history), 2)
        
        # Check message structure
        message = self.memory.conversation_history[0]
        self.assertEqual(message["role"], "user")
        self.assertEqual(message["content"], "Hello")
        self.assertIn("timestamp", message)
        self.assertIn("metadata", message)
    
    def test_add_tool_result(self):
        """Test adding tool results to memory."""
        result = {"success": True, "data": {"temperature": 20}}
        self.memory.add_tool_result("weather_api", result)
        
        self.assertEqual(len(self.memory.tool_results), 1)
        
        # Check tool result structure
        tool_result = self.memory.tool_results[0]
        self.assertEqual(tool_result["tool"], "weather_api")
        self.assertEqual(tool_result["result"], result)
        self.assertIn("timestamp", tool_result)
    
    def test_get_context(self):
        """Test getting context from memory."""
        # Add some data
        for i in range(10):
            self.memory.add_message("user", f"Message {i}")
        
        for i in range(5):
            self.memory.add_tool_result(f"tool_{i}", {"result": i})
        
        context = self.memory.get_context()
        
        # Check context structure
        self.assertIn("conversation_history", context)
        self.assertIn("context", context)
        self.assertIn("recent_tool_results", context)
        
        # Check that only recent items are included
        self.assertEqual(len(context["conversation_history"]), 5)  # Last 5 messages
        self.assertEqual(len(context["recent_tool_results"]), 3)   # Last 3 tool results


class TestIntegration(TestAgentBase):
    """Integration tests for agent and tool interactions."""
    
    def setUp(self):
        """Set up test fixtures for integration tests."""
        super().setUp()
        self.agent = WeatherAgent(self.mock_config)
    
    def test_agent_tool_integration(self):
        """Test agent using weather tool."""
        result = self.agent.execute_tool("weather_api", location="London", units="celsius")
        self.assert_valid_response(result)
        self.assertTrue(result["success"])
        
        # Check that result was added to memory
        context = self.agent.memory.get_context()
        self.assertEqual(len(context["recent_tool_results"]), 1)
        self.assertEqual(context["recent_tool_results"][0]["tool"], "weather_api")
    
    def test_end_to_end_weather_workflow(self):
        """Test complete weather request workflow."""
        user_input = "What's the weather in Tokyo?"
        response = self.agent.process_user_input(user_input)
        
        # Check that response contains weather information
        self.assertIn("Tokyo", response)
        self.assertIn("Temperature", response)
        
        # Check that conversation was recorded
        context = self.agent.memory.get_context()
        self.assertEqual(len(context["conversation_history"]), 2)  # User + assistant
        self.assertEqual(context["conversation_history"][0]["role"], "user")
        self.assertEqual(context["conversation_history"][1]["role"], "assistant")
    
    def test_error_propagation(self):
        """Test error handling across components."""
        # Mock the weather tool to raise an exception
        with patch.object(self.agent.tools["weather_api"], "execute", side_effect=Exception("API Error")):
            result = self.agent.execute_tool("weather_api", location="London")
            self.assertFalse(result["success"])
            self.assertIn("error", result)
    
    def test_invalid_tool_execution(self):
        """Test executing non-existent tool."""
        result = self.agent.execute_tool("nonexistent_tool", param="value")
        self.assertFalse(result["success"])
        self.assertIn("not found", result["error"])


class TestPerformance(TestAgentBase):
    """Performance tests for the agent and tools."""
    
    def setUp(self):
        """Set up test fixtures for performance tests."""
        super().setUp()
        self.agent = WeatherAgent(self.mock_config)
    
    def test_response_time(self):
        """Test that responses are generated within acceptable time limits."""
        import time
        
        start_time = time.time()
        response = self.agent.process_user_input("What's the weather in London?")
        end_time = time.time()
        
        # Should respond within 2 seconds for simulated API
        self.assertLess(end_time - start_time, 2.0)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_memory_efficiency(self):
        """Test memory usage with large conversation history."""
        # Add many messages
        for i in range(100):
            self.agent.process_user_input(f"Message {i}")
        
        # Context should still be limited to recent items
        context = self.agent.memory.get_context()
        self.assertLessEqual(len(context["conversation_history"]), 5)
        self.assertLessEqual(len(context["recent_tool_results"]), 3)
    
    def test_concurrent_tool_execution(self):
        """Test multiple tool executions."""
        import threading
        import time
        
        results = []
        
        def execute_tool():
            result = self.agent.execute_tool("weather_api", location="London")
            results.append(result)
        
        # Execute multiple tools concurrently
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=execute_tool)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check that all executions succeeded
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertTrue(result["success"])


class TestSecurity(TestAgentBase):
    """Security tests for the agent and tools."""
    
    def setUp(self):
        """Set up test fixtures for security tests."""
        super().setUp()
        self.agent = WeatherAgent(self.mock_config)
    
    def test_input_sanitization(self):
        """Test that malicious input is properly handled."""
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "../../../etc/passwd",
            "London'; DELETE FROM weather; --",
            "<img src=x onerror=alert('xss')>",
        ]
        
        for malicious_input in malicious_inputs:
            # Should not crash and should return a reasonable response
            response = self.agent.process_user_input(f"Weather in {malicious_input}")
            self.assertIsInstance(response, str)
            # Should not contain the malicious content directly
            self.assertNotIn("<script>", response)
            self.assertNotIn("DROP TABLE", response)
    
    def test_location_validation(self):
        """Test location parameter validation."""
        # Test extremely long location names
        long_location = "A" * 1000
        result = self.agent.execute_tool("weather_api", location=long_location)
        # Should handle gracefully (either succeed or fail safely)
        self.assertIn("success", result)
    
    def test_error_message_safety(self):
        """Test that error messages don't expose sensitive information."""
        # Force an error condition
        with patch.object(self.agent.tools["weather_api"], "_simulate_weather_api", 
                         side_effect=Exception("Internal system error: /etc/passwd")):
            result = self.agent.execute_tool("weather_api", location="London")
            
            self.assertFalse(result["success"])
            # Error message should not contain sensitive paths
            self.assertNotIn("/etc/passwd", result["error"])


def create_test_suite() -> unittest.TestSuite:
    """Create a comprehensive test suite."""
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestWeatherAgent,
        TestWeatherAPITool,
        TestAgentMemory,
        TestIntegration,
        TestPerformance,
        TestSecurity
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_tests(verbosity: int = 2) -> unittest.TestResult:
    """Run all tests and return the results."""
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


if __name__ == "__main__":
    # Run tests when script is executed directly
    print("Running Weather Agent Test Suite")
    print("=" * 50)
    
    result = run_tests()
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}")
    
    # Exit with appropriate code
    exit_code = 0 if result.wasSuccessful() else 1
    exit(exit_code)
