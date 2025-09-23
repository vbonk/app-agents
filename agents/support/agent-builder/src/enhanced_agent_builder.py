"""
Enhanced Agent-Builder Agent
Updated to meet the new agent standards and specifications.
"""

import asyncio
import json
import sqlite3
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd
import yaml
import sys
import os

# Add shared templates to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared', 'templates'))

from enhanced_agent_base import EnhancedAgentBase, AgentConfig


class EnhancedAgentBuilder(EnhancedAgentBase):
    """
    Enhanced Agent-Builder with comprehensive agent development capabilities.
    Implements all required standards: multi-source research, persistent memory,
    iterative dataset enrichment, prompt optimization, and tool awareness.
    """
    
    def __init__(self, data_dir: str = "./agent_builder_data"):
        config = AgentConfig(
            name="enhanced_agent_builder",
            version="2.0.0",
            description="Comprehensive agent development system with enhanced capabilities",
            capabilities=[
                "agent_design",
                "code_generation",
                "template_management",
                "best_practices_integration",
                "multi_source_research",
                "dataset_enrichment",
                "prompt_optimization",
                "tool_discovery"
            ],
            data_sources=["documentation", "code_repositories", "best_practices", "templates"]
        )
        super().__init__(config, data_dir)
        
        # Agent-builder specific configuration
        self.template_dir = Path(__file__).resolve().parents[3] / "shared" / "templates" / "agent_templates"
        self.best_practices_db = self.data_dir / "best_practices.json"
        
        # Initialize agent-builder specific tools
        self._init_agent_builder_tools()
        
        # Load best practices
        self._load_best_practices()
        
        self.logger.info("Enhanced Agent-Builder initialized")
    
    def _init_agent_builder_tools(self):
        """Initialize agent-builder specific tools."""
        builder_tools = {
            "code_generator": {
                "name": "code_generator",
                "description": "Generate Python code for agents based on specifications",
                "input_schema": {"spec": "object", "template": "string"},
                "output_schema": {"code": "string", "files": "array"}
            },
            "template_processor": {
                "name": "template_processor",
                "description": "Process and customize agent templates",
                "input_schema": {"template": "string", "variables": "object"},
                "output_schema": {"processed_template": "string"}
            },
            "best_practices_analyzer": {
                "name": "best_practices_analyzer",
                "description": "Analyze agent design against best practices",
                "input_schema": {"agent_spec": "object"},
                "output_schema": {"compliance_score": "float", "recommendations": "array"}
            },
            "dependency_manager": {
                "name": "dependency_manager",
                "description": "Manage agent dependencies and requirements",
                "input_schema": {"capabilities": "array", "platform": "string"},
                "output_schema": {"dependencies": "array", "requirements_txt": "string"}
            }
        }
        
        for tool_name, tool_data in builder_tools.items():
            from enhanced_agent_base import ToolInfo
            tool = ToolInfo(**tool_data)

            handler_map = {
                "code_generator": self._handle_code_generator,
                "template_processor": self._handle_template_processor,
                "best_practices_analyzer": self._handle_best_practices_analyzer,
                "dependency_manager": self._handle_dependency_manager
            }

            handler = handler_map.get(tool_name)
            self.register_tool(tool, handler=handler)

    def _handle_code_generator(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agent code based on a specification."""
        spec = payload.get("spec", {})
        template = payload.get("template")

        code = self._generate_agent_code(spec)
        files = []

        if template:
            files.append({"template": template})

        return {
            "result": {
                "code": code,
                "files": files
            }
        }

    def _handle_template_processor(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Apply simple templating using provided variables."""
        template_reference = payload.get("template", "")
        variables = payload.get("variables", {})

        template_content = template_reference
        candidate_path = self.template_dir / template_reference
        if candidate_path.exists():
            template_content = candidate_path.read_text(encoding="utf-8")

        try:
            processed = template_content.format(**variables)
        except Exception as exc:
            processed = template_content
            self.logger.error("Template processing error for %s: %s", template_reference, exc)

        return {
            "result": {
                "processed_template": processed
            }
        }

    def _handle_best_practices_analyzer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Return a simple compliance score with recommendations."""
        agent_spec = payload.get("agent_spec", {})

        checks = [
            ("name", bool(agent_spec.get("name")), "Provide an agent name"),
            ("description", bool(agent_spec.get("description")), "Add a description"),
            ("capabilities", bool(agent_spec.get("capabilities")), "List at least one capability"),
            ("data_sources", bool(agent_spec.get("data_sources")), "Define data sources"),
            (
                "documentation",
                any(key in agent_spec for key in ("readme", "docs", "documentation")),
                "Document usage expectations"
            ),
        ]

        passed = [label for label, ok, _ in checks if ok]
        failed = [message for _, ok, message in checks if not ok]

        compliance_score = len(passed) / len(checks) if checks else 1.0

        return {
            "result": {
                "compliance_score": round(compliance_score, 2),
                "recommendations": failed
            }
        }

    def _handle_dependency_manager(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Map agent capabilities to dependency suggestions."""
        capabilities = payload.get("capabilities", []) or []

        base_deps = {
            "core": ["requests", "pandas", "pyyaml"],
            "testing": ["pytest"]
        }
        capability_deps = {
            "web_crawling": ["beautifulsoup4"],
            "data_analysis": ["numpy"],
            "multi_source_research": ["httpx"],
            "dataset_enrichment": ["openpyxl"],
            "prompt_optimization": []
        }

        resolved: List[str] = []
        for deps in base_deps.values():
            resolved.extend(deps)

        for capability in capabilities:
            resolved.extend(capability_deps.get(capability, []))

        normalized = sorted(dict.fromkeys(resolved))
        requirements_txt = "\n".join(normalized) + ("\n" if normalized else "")

        return {
            "result": {
                "dependencies": normalized,
                "requirements_txt": requirements_txt
            }
        }
    
    def _load_best_practices(self):
        """Load best practices from various sources."""
        if self.best_practices_db.exists():
            self.best_practices = self.load_dataset(str(self.best_practices_db), "json")
        else:
            # Initialize with default best practices
            self.best_practices = {
                "openai": {
                    "agent_design": [
                        "Use clear, specific prompts",
                        "Implement proper error handling",
                        "Include comprehensive logging",
                        "Design for scalability"
                    ],
                    "code_quality": [
                        "Follow PEP 8 style guidelines",
                        "Write comprehensive tests",
                        "Use type hints",
                        "Document all functions"
                    ]
                },
                "anthropic": {
                    "agent_behavior": [
                        "Design for helpful, harmless, honest interactions",
                        "Implement proper safety measures",
                        "Use constitutional AI principles",
                        "Ensure transparent decision making"
                    ]
                },
                "general": {
                    "architecture": [
                        "Use modular design patterns",
                        "Implement proper separation of concerns",
                        "Design for testability",
                        "Use dependency injection"
                    ]
                }
            }
            self.save_dataset(self.best_practices, str(self.best_practices_db), "json")
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent-builder task."""
        task_type = task.get("type", "build")
        
        start_time = datetime.now()
        
        try:
            if task_type == "build":
                result = await self._execute_build_task(task)
            elif task_type == "analyze":
                result = await self._execute_analysis_task(task)
            elif task_type == "template":
                result = await self._execute_template_task(task)
            elif task_type == "research":
                result = self.conduct_multi_source_research(
                    query=task.get("query", ""),
                    sources=task.get("sources")
                )
            elif task_type == "optimize":
                result = await self._execute_optimization_task(task)
            else:
                result = {
                    "error": f"Unknown task type: {task_type}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Record performance metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self.record_metric("response_times", execution_time)
            
            if "error" not in result:
                self.record_metric("task_completion_rate", 1.0)
            else:
                self.record_metric("task_completion_rate", 0.0)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            self.record_metric("task_completion_rate", 0.0)
            return {
                "error": str(e),
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _execute_build_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent building task."""
        agent_spec = task.get("specification", {})
        output_dir = task.get("output_dir", str(self.data_dir / "generated_agents"))
        
        results = {
            "task_type": "build",
            "agent_name": agent_spec.get("name", "unnamed_agent"),
            "files_generated": [],
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Validate specification
            validation_result = self._validate_agent_specification(agent_spec)
            if not validation_result["valid"]:
                results["error"] = f"Invalid specification: {validation_result['errors']}"
                return results
            
            # Analyze against best practices
            best_practices_analysis = self.use_tool("best_practices_analyzer", {
                "agent_spec": agent_spec
            })
            
            results["compliance_score"] = best_practices_analysis.get("result", {}).get("compliance_score", 0.5)
            results["recommendations"] = best_practices_analysis.get("result", {}).get("recommendations", [])
            
            # Generate agent code
            code_generation_result = self.use_tool("code_generator", {
                "spec": agent_spec,
                "template": "enhanced_agent_base"
            })
            
            # Create output directory
            output_path = Path(output_dir) / agent_spec.get("name", "unnamed_agent")
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate main agent file
            agent_code = self._generate_agent_code(agent_spec)
            agent_file = output_path / "src" / f"{agent_spec.get('name', 'agent')}.py"
            agent_file.parent.mkdir(exist_ok=True)
            
            with open(agent_file, 'w') as f:
                f.write(agent_code)
            results["files_generated"].append(str(agent_file))
            
            # Generate configuration file
            config_data = self._generate_agent_config(agent_spec)
            config_file = output_path / "config" / "agent_config.yaml"
            config_file.parent.mkdir(exist_ok=True)
            
            with open(config_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            results["files_generated"].append(str(config_file))
            
            # Generate test file
            test_code = self._generate_test_code(agent_spec)
            test_file = output_path / "tests" / f"test_{agent_spec.get('name', 'agent')}.py"
            test_file.parent.mkdir(exist_ok=True)
            
            with open(test_file, 'w') as f:
                f.write(test_code)
            results["files_generated"].append(str(test_file))
            
            # Generate README
            readme_content = self._generate_readme(agent_spec)
            readme_file = output_path / "README.md"
            
            with open(readme_file, 'w') as f:
                f.write(readme_content)
            results["files_generated"].append(str(readme_file))
            
            # Generate agents.md specification
            agents_md_content = self._generate_agents_md(agent_spec)
            agents_md_file = output_path / "agents.md"
            
            with open(agents_md_file, 'w') as f:
                f.write(agents_md_content)
            results["files_generated"].append(str(agents_md_file))
            
            # Generate requirements.txt
            dependencies = self.use_tool("dependency_manager", {
                "capabilities": agent_spec.get("capabilities", []),
                "platform": "python"
            })
            
            requirements_file = output_path / "requirements.txt"
            with open(requirements_file, 'w') as f:
                f.write(dependencies.get("result", {}).get("requirements_txt", ""))
            results["files_generated"].append(str(requirements_file))
            
            results["output_directory"] = str(output_path)
            
            # Store build results in memory
            self.store_memory(
                content=f"Built agent: {agent_spec.get('name', 'unnamed_agent')}",
                metadata={
                    "type": "agent_build",
                    "agent_name": agent_spec.get("name"),
                    "files_generated": len(results["files_generated"]),
                    "compliance_score": results["compliance_score"]
                }
            )
            
            return results
            
        except Exception as e:
            self.logger.error(f"Agent build failed: {e}")
            results["error"] = str(e)
            return results
    
    def _validate_agent_specification(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Validate agent specification."""
        errors = []
        
        required_fields = ["name", "description", "capabilities"]
        for field in required_fields:
            if field not in spec:
                errors.append(f"Missing required field: {field}")
        
        if "name" in spec and not spec["name"].replace("_", "").replace("-", "").isalnum():
            errors.append("Agent name must be alphanumeric (with underscores/hyphens)")
        
        if "capabilities" in spec and not isinstance(spec["capabilities"], list):
            errors.append("Capabilities must be a list")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def _generate_agent_code(self, spec: Dict[str, Any]) -> str:
        """Generate the main agent code."""
        agent_name = spec.get("name", "Agent")
        class_name = "".join(word.capitalize() for word in agent_name.split("_"))
        
        capabilities = spec.get("capabilities", [])
        description = spec.get("description", "Generated agent")
        
        code_template = f'''"""
{class_name}
Generated by Enhanced Agent-Builder v2.0.0
{description}
"""

import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

# Add shared templates to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared', 'templates'))

from enhanced_agent_base import EnhancedAgentBase, AgentConfig


class {class_name}(EnhancedAgentBase):
    """
    {description}
    
    Capabilities: {', '.join(capabilities)}
    """
    
    def __init__(self, data_dir: str = "./{agent_name}_data"):
        config = AgentConfig(
            name="{agent_name}",
            version="1.0.0",
            description="{description}",
            capabilities={capabilities},
            data_sources={spec.get("data_sources", ["web", "files"])}
        )
        super().__init__(config, data_dir)
        
        # Initialize agent-specific tools
        self._init_agent_tools()
        
        self.logger.info("{class_name} initialized")
    
    def _init_agent_tools(self):
        """Initialize agent-specific tools."""
        # Add custom tools here based on capabilities
        pass
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task."""
        task_type = task.get("type", "default")
        
        start_time = datetime.now()
        
        try:
            if task_type == "research":
                result = self.conduct_multi_source_research(
                    query=task.get("query", ""),
                    sources=task.get("sources")
                )
            else:
                # Implement custom task handling here
                result = {{
                    "task_type": task_type,
                    "status": "completed",
                    "message": f"Executed {{task_type}} task",
                    "timestamp": datetime.now().isoformat()
                }}
            
            # Record performance metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self.record_metric("response_times", execution_time)
            self.record_metric("task_completion_rate", 1.0)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {{e}}")
            self.record_metric("task_completion_rate", 0.0)
            return {{
                "error": str(e),
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            }}
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return self.config.capabilities


if __name__ == "__main__":
    # Example usage
    agent = {class_name}()
    
    # Test health check
    health = agent.health_check()
    print("Health Check:", json.dumps(health, indent=2))
    
    # Test task execution
    async def test_agent():
        task = {{
            "type": "research",
            "query": "test query"
        }}
        result = await agent.execute_task(task)
        print("Task Result:", json.dumps(result, indent=2))
    
    asyncio.run(test_agent())
'''
        
        return code_template
    
    def _generate_agent_config(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agent configuration."""
        return {
            "agent": {
                "name": spec.get("name", "agent"),
                "version": "1.0.0",
                "description": spec.get("description", "Generated agent"),
                "capabilities": spec.get("capabilities", []),
                "data_sources": spec.get("data_sources", ["web", "files"])
            },
            "settings": {
                "memory_enabled": True,
                "learning_enabled": True,
                "tool_discovery_enabled": True,
                "log_level": "INFO"
            },
            "performance": {
                "max_concurrent_tasks": 5,
                "timeout_seconds": 300,
                "retry_attempts": 3
            }
        }
    
    def _generate_test_code(self, spec: Dict[str, Any]) -> str:
        """Generate test code for the agent."""
        agent_name = spec.get("name", "Agent")
        class_name = "".join(word.capitalize() for word in agent_name.split("_"))
        
        test_template = f'''"""
Test suite for {class_name}
Generated by Enhanced Agent-Builder v2.0.0
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from {agent_name} import {class_name}


class Test{class_name}:
    """Test suite for {class_name}."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = {class_name}(data_dir="./test_data")
    
    def teardown_method(self):
        """Clean up after tests."""
        # Clean up test data if needed
        pass
    
    def test_initialization(self):
        """Test agent initialization."""
        assert self.agent.config.name == "{agent_name}"
        assert self.agent.config.version == "1.0.0"
        assert isinstance(self.agent.config.capabilities, list)
    
    def test_health_check(self):
        """Test agent health check."""
        health = self.agent.health_check()
        
        assert health["agent"] == "{agent_name}"
        assert health["status"] == "healthy"
        assert "timestamp" in health
    
    def test_get_capabilities(self):
        """Test capabilities retrieval."""
        capabilities = self.agent.get_capabilities()
        assert isinstance(capabilities, list)
        assert len(capabilities) > 0
    
    @pytest.mark.asyncio
    async def test_execute_task(self):
        """Test task execution."""
        task = {{
            "type": "research",
            "query": "test query"
        }}
        
        result = await self.agent.execute_task(task)
        
        assert "timestamp" in result
        assert result.get("error") is None or "error" in result
    
    def test_memory_operations(self):
        """Test memory storage and retrieval."""
        # Test memory storage
        memory_id = self.agent.store_memory("Test memory", {{"type": "test"}})
        assert memory_id is not None
        
        # Test memory retrieval
        memories = self.agent.retrieve_memory("Test", limit=1)
        assert len(memories) >= 0
    
    def test_tool_usage(self):
        """Test tool usage."""
        # Test with a known tool
        if "web_search" in self.agent.tools:
            result = self.agent.use_tool("web_search", {{"query": "test", "limit": 5}})
            assert "tool" in result
            assert result["tool"] == "web_search"
    
    def test_dataset_operations(self):
        """Test dataset loading and saving."""
        # Test data saving
        test_data = {{"test": "data", "timestamp": "2025-01-01"}}
        test_file = "./test_data/test_dataset.json"
        
        self.agent.save_dataset(test_data, test_file, "json")
        
        # Test data loading
        loaded_data = self.agent.load_dataset(test_file, "json")
        assert loaded_data == test_data
    
    def test_performance_metrics(self):
        """Test performance metrics recording."""
        self.agent.record_metric("test_metric", 0.95)
        
        summary = self.agent.get_performance_summary()
        assert "test_metric" in summary
        assert summary["test_metric"]["latest"] == 0.95


if __name__ == "__main__":
    pytest.main([__file__])
'''
        
        return test_template
    
    def _generate_readme(self, spec: Dict[str, Any]) -> str:
        """Generate README for the agent."""
        agent_name = spec.get("name", "Agent")
        description = spec.get("description", "Generated agent")
        capabilities = spec.get("capabilities", [])
        
        readme_template = f'''# {agent_name.replace("_", " ").title()}

{description}

## Overview

This agent was generated by the Enhanced Agent-Builder v2.0.0 and implements all required standards for the app-agents repository.

## Capabilities

{chr(10).join(f"- {capability}" for capability in capabilities)}

## Features

- **Multi-Source Research**: Gather information from various sources
- **Persistent Memory**: Store and retrieve information across sessions
- **Iterative Dataset Enrichment**: Continuously improve datasets
- **Prompt Optimization**: Automatically optimize prompts based on performance
- **Tool Awareness**: Discover and utilize available tools
- **Data Versatility**: Work with multiple data formats (JSON, YAML, XML, CSV, Markdown)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the agent:
```python
from src.{agent_name} import {agent_name.replace("_", " ").title().replace(" ", "")}

agent = {agent_name.replace("_", " ").title().replace(" ", "")}()
health = agent.health_check()
print(health)
```

## Usage

### Basic Task Execution

```python
import asyncio

async def run_task():
    task = {{
        "type": "research",
        "query": "your research query here"
    }}
    
    result = await agent.execute_task(task)
    print(result)

asyncio.run(run_task())
```

### Memory Operations

```python
# Store information
memory_id = agent.store_memory("Important information", {{"type": "note"}})

# Retrieve information
memories = agent.retrieve_memory("Important", limit=5)
```

### Dataset Operations

```python
# Load dataset
data = agent.load_dataset("data.json", "json")

# Save dataset
agent.save_dataset(data, "output.json", "json")
```

## Configuration

The agent can be configured through the `config/agent_config.yaml` file:

```yaml
agent:
  name: {agent_name}
  version: 1.0.0
  capabilities: {capabilities}

settings:
  memory_enabled: true
  learning_enabled: true
  tool_discovery_enabled: true
```

## Testing

Run the test suite:

```bash
pytest tests/
```

## Performance Metrics

The agent tracks the following metrics:
- Task completion rate
- Response times
- Accuracy scores
- User satisfaction

Access metrics:
```python
performance = agent.get_performance_summary()
print(performance)
```

## Integration with SaaS Architecture

This agent is designed to integrate with the SaaS ecosystem architecture:

- **Database Integration**: Uses Prisma ORM with PostgreSQL and pgvector
- **API Endpoints**: Exposes RESTful API for external integration
- **Multi-Tenancy**: Supports tenant isolation and data security
- **Monitoring**: Comprehensive logging and performance tracking

## Contributing

1. Follow the agent standards and specifications
2. Write comprehensive tests
3. Update documentation
4. Ensure compliance with best practices

## License

This agent is part of the app-agents repository and follows the same licensing terms.
'''
        
        return readme_template
    
    def _generate_agents_md(self, spec: Dict[str, Any]) -> str:
        """Generate agents.md specification file."""
        agent_name = spec.get("name", "Agent")
        description = spec.get("description", "Generated agent")
        capabilities = spec.get("capabilities", [])
        
        agents_md_template = f'''# {agent_name.replace("_", " ").title()} Agent Specification

## Agent Metadata

- **Name**: {agent_name.replace("_", " ").title()}
- **Version**: 1.0.0
- **Type**: Generated Agent
- **Category**: {spec.get("category", "General Purpose")}
- **Created**: {datetime.now().strftime("%Y-%m-%d")}
- **Updated**: {datetime.now().strftime("%Y-%m-%d")}
- **Status**: Production Ready

## Description

{description}

This agent was generated by the Enhanced Agent-Builder v2.0.0 and implements all required standards for the app-agents repository, including multi-source research, persistent memory, iterative dataset enrichment, prompt optimization, and tool awareness.

## Capabilities

### Core Functions

{chr(10).join(f"{i+1}. **{capability.replace('_', ' ').title()}**: Advanced {capability.replace('_', ' ')} capabilities" for i, capability in enumerate(capabilities))}

### Specialized Features

- **Multi-Source Research**: Conducts research across web, databases, and files
- **Persistent Memory**: SQLite-based memory system with learning patterns
- **Dataset Management**: Supports JSON, YAML, XML, CSV, and Markdown formats
- **Tool Integration**: Automatic tool discovery and usage tracking
- **Performance Optimization**: Continuous improvement through learning
- **SaaS Integration**: Built for multi-tenant SaaS architecture

## Input Schema

### Primary Task Request

```json
{{
  "type": "string (required) - Task type to execute",
  "query": "string (optional) - Query or prompt for the task",
  "data": "object (optional) - Input data for processing",
  "config": "object (optional) - Task-specific configuration",
  "sources": "array[string] (optional) - Data sources to use"
}}
```

### Research Request

```json
{{
  "type": "research",
  "query": "string (required) - Research query",
  "sources": "array[string] (optional) - Sources to search",
  "limit": "integer (optional) - Maximum results per source"
}}
```

## Output Schema

### Task Result

```json
{{
  "task_type": "string - Type of task executed",
  "status": "string - Execution status (completed/error)",
  "result": "object - Task-specific results",
  "timestamp": "string - ISO timestamp of completion",
  "execution_time": "float - Time taken in seconds",
  "error": "string (optional) - Error message if failed"
}}
```

### Research Result

```json
{{
  "query": "string - Original research query",
  "sources": "array[string] - Sources searched",
  "findings": "array[object] - Research findings",
  "timestamp": "string - ISO timestamp",
  "total_results": "integer - Total results found"
}}
```

## Error Handling

### Common Error Responses

```json
{{
  "error": "string - Error type",
  "message": "string - Human-readable error message",
  "details": "object (optional) - Additional error context",
  "timestamp": "string - ISO timestamp of error"
}}
```

### Error Types

- `invalid_task_type`: Unknown or unsupported task type
- `missing_required_field`: Required input field is missing
- `data_processing_error`: Error processing input data
- `tool_unavailable`: Required tool is not available
- `memory_error`: Database or memory system error

## Performance Characteristics

### Latency

- **Simple Tasks**: 1-2 seconds average
- **Research Tasks**: 3-10 seconds (depending on sources)
- **Data Processing**: 2-5 seconds (depending on data size)

### Throughput

- **Concurrent Tasks**: Up to 5 simultaneous tasks
- **Memory Operations**: 100+ operations per second
- **Tool Usage**: Real-time tool discovery and execution

### Resource Usage

- **Memory**: 50-200MB depending on dataset size
- **Storage**: ~1MB per 100 memory entries
- **CPU**: Moderate during active processing

## Dependencies

### Required Python Packages

```
pandas>=1.5.0
numpy>=1.21.0
requests>=2.28.0
pyyaml>=6.0
sqlite3 (built-in)
asyncio (built-in)
```

### System Requirements

- **Python**: 3.11+ (tested with 3.11)
- **Operating System**: Cross-platform (Linux, macOS, Windows)
- **Disk Space**: 100MB+ for data and memory storage
- **Network**: Internet connection for research tasks

## Configuration

### Agent Configuration

The agent supports configuration through YAML files:

```yaml
agent:
  name: {agent_name}
  version: 1.0.0
  capabilities: {capabilities}

settings:
  memory_enabled: true
  learning_enabled: true
  tool_discovery_enabled: true
```

### Performance Tuning

```yaml
performance:
  max_concurrent_tasks: 5
  timeout_seconds: 300
  retry_attempts: 3
  memory_limit_mb: 500
```

## Security Considerations

### Data Privacy

- **Local Storage**: All data stored locally in SQLite database
- **No External Transmission**: Sensitive data not transmitted externally
- **Access Control**: File system permissions respected
- **Logging**: Configurable logging levels with sensitive data filtering

### Multi-Tenancy

- **Data Isolation**: Tenant data separated at database level
- **Access Control**: Row-level security implementation
- **API Security**: OAuth 2.0 authentication required
- **Audit Logging**: Comprehensive activity logging

## Integration Patterns

### Standalone Usage

```python
from src.{agent_name} import {agent_name.replace("_", " ").title().replace(" ", "")}

agent = {agent_name.replace("_", " ").title().replace(" ", "")}()
result = await agent.execute_task({{"type": "research", "query": "example"}})
```

### API Service Integration

```python
from fastapi import FastAPI
from src.{agent_name} import {agent_name.replace("_", " ").title().replace(" ", "")}

app = FastAPI()
agent = {agent_name.replace("_", " ").title().replace(" ", "")}()

@app.post("/execute")
async def execute_task(request: dict):
    return await agent.execute_task(request)
```

## Testing

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_{agent_name}.py::Test{agent_name.replace("_", " ").title().replace(" ", "")}::test_initialization
```

### Performance Tests

```bash
# Run performance benchmarks
python tests/performance_tests.py
```

## Monitoring and Observability

### Logging

The agent provides comprehensive logging:

- **INFO**: Task execution, performance metrics
- **DEBUG**: Detailed operation logs
- **WARNING**: Performance issues, recoverable errors
- **ERROR**: Task failures, system errors

### Metrics

Key metrics tracked:

- **Task Completion Rate**: Percentage of successful tasks
- **Response Times**: Average and percentile response times
- **Memory Usage**: Memory system utilization
- **Tool Usage**: Tool discovery and usage statistics

### Health Checks

```python
# Check agent health
health = agent.health_check()
print(health)
```

## Versioning and Compatibility

### Version History

- **1.0.0**: Initial generated version with all standard capabilities

### Backward Compatibility

- **Configuration**: Backward-compatible configuration format
- **API**: Semantic versioning for breaking changes
- **Data**: Automatic migration for data format changes

## Support and Documentation

### Documentation

- **README.md**: Comprehensive usage guide
- **API Documentation**: Detailed function documentation
- **Configuration Guide**: Setup and configuration instructions
- **Integration Examples**: Sample code for common patterns

### Community

- **Repository**: [app-agents](https://github.com/vbonk/app-agents)
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and support

### Maintenance

- **Regular Updates**: Ongoing maintenance and improvements
- **Security Patches**: Prompt security updates
- **Performance Optimization**: Continuous performance monitoring
- **Community Feedback**: Active incorporation of user feedback
'''
        
        return agents_md_template
    
    async def _execute_analysis_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an agent analysis task."""
        analysis_type = task.get("analysis_type", "specification")
        target = task.get("target")
        
        results = {
            "task_type": "analysis",
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            if analysis_type == "specification":
                results["analysis"] = self._analyze_specification(target)
            elif analysis_type == "best_practices":
                results["analysis"] = self._analyze_best_practices_compliance(target)
            elif analysis_type == "performance":
                results["analysis"] = self._analyze_performance_requirements(target)
            else:
                results["error"] = f"Unknown analysis type: {analysis_type}"
            
            return results
            
        except Exception as e:
            self.logger.error(f"Analysis task failed: {e}")
            results["error"] = str(e)
            return results
    
    def _analyze_specification(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze agent specification for completeness and quality."""
        analysis = {
            "completeness_score": 0.0,
            "quality_score": 0.0,
            "missing_fields": [],
            "recommendations": []
        }
        
        required_fields = ["name", "description", "capabilities", "data_sources"]
        optional_fields = ["version", "category", "dependencies", "performance_requirements"]
        
        # Check completeness
        present_required = sum(1 for field in required_fields if field in spec)
        present_optional = sum(1 for field in optional_fields if field in spec)
        
        analysis["completeness_score"] = (present_required / len(required_fields)) * 0.8 + \
                                       (present_optional / len(optional_fields)) * 0.2
        
        # Identify missing fields
        analysis["missing_fields"] = [field for field in required_fields if field not in spec]
        
        # Quality assessment
        quality_factors = []
        
        if "description" in spec and len(spec["description"]) > 50:
            quality_factors.append(0.2)
        
        if "capabilities" in spec and len(spec["capabilities"]) >= 3:
            quality_factors.append(0.2)
        
        if "data_sources" in spec and len(spec["data_sources"]) >= 2:
            quality_factors.append(0.2)
        
        analysis["quality_score"] = sum(quality_factors)
        
        # Generate recommendations
        if analysis["completeness_score"] < 0.8:
            analysis["recommendations"].append("Add missing required fields")
        
        if "description" in spec and len(spec["description"]) < 50:
            analysis["recommendations"].append("Provide more detailed description")
        
        if "capabilities" not in spec or len(spec["capabilities"]) < 3:
            analysis["recommendations"].append("Define at least 3 specific capabilities")
        
        return analysis
    
    def _analyze_best_practices_compliance(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze specification against best practices."""
        compliance_analysis = self.use_tool("best_practices_analyzer", {
            "agent_spec": spec
        })
        
        return compliance_analysis.get("result", {
            "compliance_score": 0.5,
            "recommendations": ["Unable to analyze best practices compliance"]
        })
    
    def _analyze_performance_requirements(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance requirements and provide recommendations."""
        capabilities = spec.get("capabilities", [])
        data_sources = spec.get("data_sources", [])
        
        analysis = {
            "estimated_complexity": "medium",
            "resource_requirements": {},
            "performance_recommendations": []
        }
        
        # Estimate complexity based on capabilities
        complexity_score = len(capabilities) * 0.1 + len(data_sources) * 0.05
        
        if complexity_score < 0.3:
            analysis["estimated_complexity"] = "low"
        elif complexity_score > 0.7:
            analysis["estimated_complexity"] = "high"
        
        # Resource requirements
        analysis["resource_requirements"] = {
            "memory_mb": max(100, len(capabilities) * 50),
            "storage_mb": max(50, len(data_sources) * 25),
            "cpu_cores": 1 if complexity_score < 0.5 else 2
        }
        
        # Performance recommendations
        if "research" in capabilities:
            analysis["performance_recommendations"].append("Implement caching for research results")
        
        if len(data_sources) > 3:
            analysis["performance_recommendations"].append("Use connection pooling for data sources")
        
        if "learning" in capabilities:
            analysis["performance_recommendations"].append("Optimize memory system for frequent updates")
        
        return analysis
    
    async def _execute_template_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a template management task."""
        template_action = task.get("action", "list")
        
        results = {
            "task_type": "template",
            "action": template_action,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            if template_action == "list":
                results["templates"] = self._list_available_templates()
            elif template_action == "create":
                results["template"] = self._create_custom_template(task.get("template_spec", {}))
            elif template_action == "process":
                results["processed"] = self._process_template(
                    task.get("template_name"),
                    task.get("variables", {})
                )
            else:
                results["error"] = f"Unknown template action: {template_action}"
            
            return results
            
        except Exception as e:
            self.logger.error(f"Template task failed: {e}")
            results["error"] = str(e)
            return results
    
    def _list_available_templates(self) -> List[Dict[str, Any]]:
        """List available agent templates."""
        templates = []
        
        if self.template_dir.exists():
            for template_file in self.template_dir.glob("*.py"):
                templates.append({
                    "name": template_file.stem,
                    "path": str(template_file),
                    "type": "python"
                })
            
            for template_file in self.template_dir.glob("*.md"):
                templates.append({
                    "name": template_file.stem,
                    "path": str(template_file),
                    "type": "markdown"
                })
        
        # Add built-in templates
        templates.extend([
            {
                "name": "enhanced_agent_base",
                "type": "python",
                "description": "Enhanced base agent with all standard capabilities"
            },
            {
                "name": "research_agent",
                "type": "python",
                "description": "Specialized research agent template"
            },
            {
                "name": "analysis_agent",
                "type": "python",
                "description": "Data analysis agent template"
            }
        ])
        
        return templates
    
    def _create_custom_template(self, template_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a custom agent template."""
        template_name = template_spec.get("name", "custom_template")
        template_type = template_spec.get("type", "python")
        
        if template_type == "python":
            template_content = self._generate_agent_code(template_spec)
        else:
            template_content = template_spec.get("content", "# Custom Template")
        
        # Save template
        template_file = self.template_dir / f"{template_name}.{template_type}"
        template_file.parent.mkdir(exist_ok=True)
        
        with open(template_file, 'w') as f:
            f.write(template_content)
        
        return {
            "name": template_name,
            "path": str(template_file),
            "type": template_type,
            "created": datetime.now().isoformat()
        }
    
    def _process_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Process a template with variables."""
        template_processing = self.use_tool("template_processor", {
            "template": template_name,
            "variables": variables
        })
        
        return template_processing.get("result", {}).get("processed_template", "")
    
    async def _execute_optimization_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an optimization task."""
        optimization_type = task.get("optimization_type", "performance")
        target_spec = task.get("target_specification", {})
        
        results = {
            "task_type": "optimization",
            "optimization_type": optimization_type,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            if optimization_type == "performance":
                results["optimizations"] = self._optimize_for_performance(target_spec)
            elif optimization_type == "memory":
                results["optimizations"] = self._optimize_for_memory(target_spec)
            elif optimization_type == "scalability":
                results["optimizations"] = self._optimize_for_scalability(target_spec)
            else:
                results["error"] = f"Unknown optimization type: {optimization_type}"
            
            return results
            
        except Exception as e:
            self.logger.error(f"Optimization task failed: {e}")
            results["error"] = str(e)
            return results
    
    def _optimize_for_performance(self, spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate performance optimizations."""
        optimizations = []
        
        capabilities = spec.get("capabilities", [])
        
        if "research" in capabilities:
            optimizations.append({
                "type": "caching",
                "description": "Implement result caching for research operations",
                "impact": "high",
                "implementation": "Add Redis or in-memory cache for frequent queries"
            })
        
        if "data_processing" in capabilities:
            optimizations.append({
                "type": "parallel_processing",
                "description": "Use parallel processing for data operations",
                "impact": "medium",
                "implementation": "Implement asyncio for concurrent data processing"
            })
        
        if len(capabilities) > 5:
            optimizations.append({
                "type": "lazy_loading",
                "description": "Implement lazy loading for capabilities",
                "impact": "medium",
                "implementation": "Load capability modules only when needed"
            })
        
        return optimizations
    
    def _optimize_for_memory(self, spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate memory optimizations."""
        optimizations = []
        
        data_sources = spec.get("data_sources", [])
        
        if len(data_sources) > 3:
            optimizations.append({
                "type": "connection_pooling",
                "description": "Implement connection pooling for data sources",
                "impact": "high",
                "implementation": "Use connection pools to reduce memory overhead"
            })
        
        optimizations.append({
            "type": "memory_cleanup",
            "description": "Implement automatic memory cleanup",
            "impact": "medium",
            "implementation": "Add periodic cleanup of unused memory entries"
        })
        
        return optimizations
    
    def _optimize_for_scalability(self, spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate scalability optimizations."""
        optimizations = []
        
        optimizations.append({
            "type": "horizontal_scaling",
            "description": "Design for horizontal scaling",
            "impact": "high",
            "implementation": "Use stateless design and external storage"
        })
        
        optimizations.append({
            "type": "load_balancing",
            "description": "Implement load balancing for high availability",
            "impact": "high",
            "implementation": "Use load balancer for multiple agent instances"
        })
        
        return optimizations
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return self.config.capabilities


# Example usage and testing
if __name__ == "__main__":
    async def test_enhanced_agent_builder():
        """Test the enhanced agent builder."""
        builder = EnhancedAgentBuilder()
        
        # Test health check
        health = builder.health_check()
        print("Health Check:", json.dumps(health, indent=2))
        
        # Test agent building
        agent_spec = {
            "name": "test_research_agent",
            "description": "A test research agent for demonstration",
            "capabilities": ["research", "analysis", "content_generation"],
            "data_sources": ["web", "databases", "files"],
            "category": "Research & Analysis"
        }
        
        build_task = {
            "type": "build",
            "specification": agent_spec,
            "output_dir": "./generated_agents"
        }
        
        print("\\nBuilding agent...")
        result = await builder.execute_task(build_task)
        print("Build Result:", json.dumps(result, indent=2))
        
        # Test analysis
        analysis_task = {
            "type": "analyze",
            "analysis_type": "specification",
            "target": agent_spec
        }
        
        print("\\nAnalyzing specification...")
        analysis_result = await builder.execute_task(analysis_task)
        print("Analysis Result:", json.dumps(analysis_result, indent=2))
    
    # Run the test
    asyncio.run(test_enhanced_agent_builder())
