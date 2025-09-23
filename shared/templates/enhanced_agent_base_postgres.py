"""
Enhanced Agent Base Template with Postgres/Prisma Support
Implements all required standards and specifications for app-agents repository.
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union, Callable
from datetime import datetime
from pathlib import Path
import pandas as pd
import requests
from dataclasses import dataclass, asdict
import yaml
import xml.etree.ElementTree as ET

# Import our new Postgres client
import sys
sys.path.append(str(Path(__file__).parent.parent))
from database.prisma_client import (
    PrismaAgentClient, AgentConfig, MemoryEntry, ToolInfo, 
    ExecutionRecord, get_agent_client
)


class EnhancedAgentBase(ABC):
    """
    Enhanced base class for all agents in the app-agents repository.
    Implements all required standards and specifications with Postgres/Prisma backend.
    """
    
    def __init__(self, config: AgentConfig, data_dir: str = "./data"):
        self.config = config
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Initialize database client
        self.db_client = get_agent_client()
        self.agent_id: Optional[str] = None
        
        # Initialize tool registry (local cache)
        self.tools: Dict[str, ToolInfo] = {}
        self._tool_handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        
        # Performance metrics (cached locally)
        self.metrics: Dict[str, List[float]] = {
            "task_completion_rate": [],
            "accuracy_scores": [],
            "response_times": [],
            "user_satisfaction": []
        }
        
        self.logger.info(f"Initialized {config.name} agent v{config.version}")
    
    async def initialize(self):
        """Initialize the agent in the database and set up tools."""
        try:
            # Ensure database connection
            await self.db_client.connect()
            
            # Create or update agent in database
            self.agent_id = await self.db_client.create_or_update_agent(self.config)
            
            # Load existing tools from database
            await self._load_tools_from_db()
            
            # Discover new tools if enabled
            if self.config.tool_discovery_enabled:
                await self._discover_tools()
            
            # Set agent status to active
            await self.db_client.update_agent_status(self.config.name, "ACTIVE")
            
            self.logger.info(f"Agent {self.config.name} initialized with ID: {self.agent_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize agent: {e}")
            raise
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the agent."""
        logger = logging.getLogger(self.config.name)
        logger.setLevel(logging.INFO)
        
        # Create file handler
        log_file = self.data_dir / f"{self.config.name}.log"
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        return logger
    
    async def _load_tools_from_db(self):
        """Load existing tools from the database."""
        if not self.agent_id:
            return
        
        try:
            tools = await self.db_client.get_agent_tools(self.agent_id)
            for tool in tools:
                self.tools[tool.name] = tool
                # Tool handlers need to be registered separately by subclasses
            
            self.logger.info(f"Loaded {len(tools)} tools from database")
        except Exception as e:
            self.logger.error(f"Failed to load tools from database: {e}")
    
    async def _discover_tools(self):
        """Discover available tools in the environment."""
        # This would integrate with the SaaS platform's tool registry
        # For now, we'll implement a basic discovery mechanism
        
        # Check for common tools
        common_tools = [
            {
                "name": "web_search",
                "description": "Search the web for information",
                "input_schema": {"query": "string", "limit": "integer"},
                "output_schema": {"results": "array"}
            },
            {
                "name": "data_analysis",
                "description": "Analyze structured data",
                "input_schema": {"data": "object", "analysis_type": "string"},
                "output_schema": {"insights": "object"}
            },
            {
                "name": "content_generation",
                "description": "Generate text content",
                "input_schema": {"prompt": "string", "style": "string"},
                "output_schema": {"content": "string"}
            }
        ]
        
        for tool_data in common_tools:
            if tool_data["name"] not in self.tools:
                tool = ToolInfo(
                    id=None,
                    agent_id=self.agent_id,
                    name=tool_data["name"],
                    description=tool_data["description"],
                    input_schema=tool_data["input_schema"],
                    output_schema=tool_data["output_schema"]
                )
                await self.register_tool(tool, handler=self._create_unimplemented_tool_handler(tool.name))

        self.logger.info(f"Discovered {len(self.tools)} tools")

    async def register_tool(self, tool_info: ToolInfo, handler: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
        """Register tool metadata and optional handler."""
        try:
            # Store in database
            tool_id = await self.db_client.register_tool(tool_info)
            tool_info.id = tool_id
            
            # Cache locally
            self.tools[tool_info.name] = tool_info
            
            if handler:
                self._tool_handlers[tool_info.name] = handler
                
            self.logger.info(f"Registered tool: {tool_info.name}")
        except Exception as e:
            self.logger.error(f"Failed to register tool {tool_info.name}: {e}")

    def register_tool_handler(self, tool_name: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """Register or replace a handler for an existing tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Cannot register handler for unknown tool '{tool_name}'")
        self._tool_handlers[tool_name] = handler
    
    async def store_memory(self, content: str, metadata: Dict[str, Any] = None, importance: float = 0.5) -> str:
        """Store information in persistent memory."""
        if not self.config.memory_enabled or not self.agent_id:
            return ""
        
        try:
            memory = MemoryEntry(
                id=None,
                agent_id=self.agent_id,
                content=content,
                metadata=metadata or {},
                importance=importance
            )
            
            memory_id = await self.db_client.store_memory(memory)
            self.logger.info(f"Stored memory entry: {memory_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"Failed to store memory: {e}")
            return ""
    
    async def retrieve_memory(self, query: str = None, limit: int = 10, min_importance: float = 0.0) -> List[MemoryEntry]:
        """Retrieve information from persistent memory."""
        if not self.config.memory_enabled or not self.agent_id:
            return []
        
        try:
            memories = await self.db_client.retrieve_memories(
                self.agent_id, query, limit, min_importance
            )
            self.logger.info(f"Retrieved {len(memories)} memories")
            return memories
        except Exception as e:
            self.logger.error(f"Failed to retrieve memories: {e}")
            return []
    
    async def use_tool(self, tool_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Use an available tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        tool = self.tools[tool_name]
        
        # Log tool usage
        self.logger.info(f"Using tool: {tool_name} with inputs: {inputs}")

        handler = self._tool_handlers.get(tool_name)
        success = False
        result = {}
        
        try:
            if not handler:
                self.logger.warning("No handler registered for tool '%s'", tool_name)
                result = {
                    "tool": tool_name,
                    "status": "not_implemented",
                    "result": {},
                    "timestamp": datetime.now().isoformat()
                }
            else:
                result = handler(inputs)
                if not isinstance(result, dict):
                    raise ValueError(f"Tool handler for '{tool_name}' must return a dictionary")

                result.setdefault("tool", tool_name)
                result.setdefault("timestamp", datetime.now().isoformat())
                result.setdefault("status", "success")
                success = True
                
        except Exception as e:
            self.logger.error(f"Tool {tool_name} failed: {e}")
            result = {
                "tool": tool_name,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        # Update tool usage statistics in database
        try:
            await self.db_client.update_tool_usage(self.agent_id, tool_name, success)
        except Exception as e:
            self.logger.error(f"Failed to update tool usage stats: {e}")

        return result

    def _create_unimplemented_tool_handler(self, tool_name: str) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
        """Return a handler that reports missing implementation."""

        def _handler(_: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "tool": tool_name,
                "status": "not_implemented",
                "result": {}
            }

        return _handler
    
    def load_dataset(self, file_path: str, format_type: str = None) -> Any:
        """Load dataset in various formats (md, json, xml, csv)."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {file_path}")
        
        # Auto-detect format if not specified
        if not format_type:
            format_type = path.suffix.lower().lstrip('.')
        
        self.logger.info(f"Loading dataset: {file_path} (format: {format_type})")
        
        if format_type in ['json']:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        elif format_type in ['yaml', 'yml']:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        elif format_type in ['xml']:
            tree = ET.parse(path)
            return tree.getroot()
        
        elif format_type in ['csv']:
            return pd.read_csv(path)
        
        elif format_type in ['md', 'markdown']:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        
        else:
            # Default to text
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    
    def save_dataset(self, data: Any, file_path: str, format_type: str = None):
        """Save dataset in various formats."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if not format_type:
            format_type = path.suffix.lower().lstrip('.')
        
        self.logger.info(f"Saving dataset: {file_path} (format: {format_type})")
        
        if format_type in ['json']:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        elif format_type in ['yaml', 'yml']:
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False)
        
        elif format_type in ['csv'] and isinstance(data, pd.DataFrame):
            data.to_csv(path, index=False)
        
        else:
            # Default to text
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(data))
    
    async def conduct_multi_source_research(self, query: str, sources: List[str] = None) -> Dict[str, Any]:
        """Conduct research across multiple sources."""
        if not sources:
            sources = self.config.data_sources
        
        results = {
            "query": query,
            "sources": sources,
            "findings": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for source in sources:
            try:
                if source == "web":
                    # Use web_search tool if available
                    if "web_search" in self.tools:
                        tool_result = await self.use_tool("web_search", {"query": query, "limit": 5})
                        finding = {
                            "source": source,
                            "data": tool_result.get("result", f"Web search results for: {query}"),
                            "confidence": 0.8
                        }
                    else:
                        finding = {
                            "source": source,
                            "data": f"Web search results for: {query}",
                            "confidence": 0.8
                        }
                elif source == "database":
                    # Mock database search
                    finding = {
                        "source": source,
                        "data": f"Database results for: {query}",
                        "confidence": 0.9
                    }
                else:
                    finding = {
                        "source": source,
                        "data": f"Results from {source} for: {query}",
                        "confidence": 0.7
                    }
                
                results["findings"].append(finding)
                
            except Exception as e:
                self.logger.error(f"Error searching {source}: {e}")
                results["findings"].append({
                    "source": source,
                    "error": str(e),
                    "confidence": 0.0
                })
        
        # Store research results in memory
        await self.store_memory(
            content=f"Research: {query}",
            metadata={"type": "research", "results": results},
            importance=0.7
        )
        
        return results
    
    async def enrich_dataset(self, dataset_id: str, new_data: Any) -> Dict[str, Any]:
        """Enrich existing dataset with new information."""
        # This would integrate with the dataset management system
        enrichment_result = {
            "dataset_id": dataset_id,
            "enrichment_timestamp": datetime.now().isoformat(),
            "new_data_size": len(str(new_data)),
            "status": "success"
        }
        
        # Store enrichment record in memory
        await self.store_memory(
            content=f"Dataset enrichment: {dataset_id}",
            metadata={"type": "enrichment", "result": enrichment_result},
            importance=0.6
        )
        
        self.logger.info(f"Enriched dataset {dataset_id}")
        return enrichment_result
    
    async def optimize_prompts(self, current_prompt: str, performance_data: Dict[str, Any]) -> str:
        """Optimize prompts based on performance data."""
        if not self.config.learning_enabled or not self.agent_id:
            return current_prompt
        
        # Simple optimization logic - in practice, this would be more sophisticated
        optimized_prompt = current_prompt
        
        if performance_data.get("accuracy", 0) < 0.7:
            optimized_prompt += "\n\nPlease be more precise and accurate in your response."
        
        if performance_data.get("response_time", 0) > 10:
            optimized_prompt += "\n\nProvide a concise response."
        
        # Store optimization as learning pattern
        try:
            pattern_data = {
                "original": current_prompt,
                "optimized": optimized_prompt,
                "performance": performance_data
            }
            
            await self.db_client.store_learning_pattern(
                self.agent_id,
                "prompt_optimization",
                pattern_data,
                confidence=0.8,
                improvement_gain=performance_data.get("improvement", 0.1)
            )
            
            self.logger.info("Optimized prompt based on performance data")
        except Exception as e:
            self.logger.error(f"Failed to store learning pattern: {e}")
        
        return optimized_prompt
    
    async def record_metric(self, metric_name: str, value: float, unit: str = None):
        """Record a performance metric."""
        # Cache locally
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        
        self.metrics[metric_name].append(value)
        
        # Store in database
        if self.agent_id:
            try:
                await self.db_client.record_metric(
                    self.agent_id, metric_name, value, unit
                )
            except Exception as e:
                self.logger.error(f"Failed to record metric {metric_name}: {e}")
        
        self.logger.info(f"Recorded metric {metric_name}: {value}")
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of agent performance metrics."""
        summary = {}
        
        # Local metrics summary
        for metric_name, values in self.metrics.items():
            if values:
                summary[f"{metric_name}_local"] = {
                    "count": len(values),
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "latest": values[-1]
                }
        
        # Database metrics summary (last 24 hours)
        if self.agent_id:
            try:
                db_metrics = await self.db_client.get_agent_metrics(self.agent_id, hours=24)
                
                # Group by metric type
                metric_groups = {}
                for metric in db_metrics:
                    metric_type = metric['metric_type']
                    if metric_type not in metric_groups:
                        metric_groups[metric_type] = []
                    metric_groups[metric_type].append(metric['value'])
                
                # Calculate summaries
                for metric_type, values in metric_groups.items():
                    summary[f"{metric_type}_db"] = {
                        "count": len(values),
                        "average": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "latest": values[0] if values else 0  # Most recent first
                    }
                    
            except Exception as e:
                self.logger.error(f"Failed to get database metrics: {e}")
        
        return summary
    
    async def start_execution(self, task_type: str, task_data: Dict[str, Any], session_id: str = None, user_id: str = None) -> str:
        """Start tracking a new execution."""
        if not self.agent_id:
            return ""
        
        try:
            execution = ExecutionRecord(
                id=None,
                agent_id=self.agent_id,
                task_type=task_type,
                task_data=task_data,
                status="RUNNING",
                started_at=datetime.now(),
                session_id=session_id,
                user_id=user_id
            )
            
            execution_id = await self.db_client.create_execution(execution)
            self.logger.info(f"Started execution: {execution_id}")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"Failed to start execution tracking: {e}")
            return ""
    
    async def complete_execution(
        self, 
        execution_id: str, 
        result: Dict[str, Any], 
        response_time: float = None,
        tokens_used: int = None,
        tools_used: List[str] = None
    ):
        """Complete an execution record."""
        try:
            await self.db_client.update_execution(
                execution_id=execution_id,
                status="COMPLETED",
                result=result,
                response_time=response_time,
                tokens_used=tokens_used,
                tools_used=tools_used
            )
            self.logger.info(f"Completed execution: {execution_id}")
        except Exception as e:
            self.logger.error(f"Failed to complete execution {execution_id}: {e}")
    
    async def fail_execution(self, execution_id: str, error_message: str):
        """Mark an execution as failed."""
        try:
            await self.db_client.update_execution(
                execution_id=execution_id,
                status="FAILED",
                error_message=error_message
            )
            self.logger.info(f"Failed execution: {execution_id}")
        except Exception as e:
            self.logger.error(f"Failed to update execution {execution_id}: {e}")
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities. Must be implemented by subclasses."""
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check of the agent."""
        db_health = await self.db_client.health_check()
        
        agent_info = {
            "agent": self.config.name,
            "version": self.config.version,
            "status": "healthy",
            "agent_id": self.agent_id,
            "memory_enabled": self.config.memory_enabled,
            "learning_enabled": self.config.learning_enabled,
            "tools_available": len(self.tools),
            "timestamp": datetime.now().isoformat()
        }
        
        if self.agent_id:
            try:
                recent_memories = await self.retrieve_memory(limit=1)
                agent_info["memory_entries"] = len(recent_memories)
            except Exception:
                agent_info["memory_entries"] = "unknown"
        
        return {
            "agent": agent_info,
            "database": db_health
        }

    async def cleanup(self):
        """Cleanup resources when agent is shutting down."""
        try:
            if self.agent_id:
                await self.db_client.update_agent_status(self.config.name, "INACTIVE")
            self.logger.info(f"Agent {self.config.name} cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


# Example implementation
class ExampleAgent(EnhancedAgentBase):
    """Example implementation of the enhanced agent base."""
    
    def __init__(self):
        config = AgentConfig(
            name="example_agent",
            version="1.0.0",
            description="Example agent demonstrating enhanced capabilities",
            category="SUPPORT",
            capabilities=["research", "analysis", "content_generation"],
            data_sources=["web", "database", "files"]
        )
        super().__init__(config)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task."""
        task_type = task.get("type", "unknown")
        
        # Start execution tracking
        execution_id = await self.start_execution(
            task_type, task, 
            session_id=task.get("session_id"),
            user_id=task.get("user_id")
        )
        
        start_time = datetime.now()
        
        try:
            if task_type == "research":
                result = await self.conduct_multi_source_research(
                    query=task.get("query", ""),
                    sources=task.get("sources")
                )
            
            elif task_type == "analysis":
                # Mock analysis task
                result = {
                    "task_type": "analysis",
                    "result": "Analysis completed",
                    "timestamp": datetime.now().isoformat()
                }
            
            else:
                result = {
                    "error": f"Unknown task type: {task_type}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Complete execution tracking
            if execution_id:
                await self.complete_execution(
                    execution_id, result, response_time=response_time
                )
            
            # Record performance metrics
            await self.record_metric("response_time", response_time, "milliseconds")
            await self.record_metric("task_completion_rate", 1.0, "percentage")
            
            return result
            
        except Exception as e:
            # Fail execution tracking
            if execution_id:
                await self.fail_execution(execution_id, str(e))
            
            # Record failure metric
            await self.record_metric("task_completion_rate", 0.0, "percentage")
            
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return self.config.capabilities


async def main():
    """Example usage"""
    agent = ExampleAgent()
    
    try:
        # Initialize agent
        await agent.initialize()
        
        # Test health check
        health = await agent.health_check()
        print("Health Check:", json.dumps(health, indent=2, default=str))
        
        # Test memory
        memory_id = await agent.store_memory("Test memory entry", {"type": "test"})
        memories = await agent.retrieve_memory()
        print(f"Stored memory: {memory_id}")
        print(f"Retrieved {len(memories)} memories")
        
        # Test tool usage
        try:
            result = await agent.use_tool("web_search", {"query": "test", "limit": 5})
            print("Tool result:", result)
        except Exception as e:
            print("Tool error:", e)
        
        # Test task execution
        task_result = await agent.execute_task({
            "type": "research",
            "query": "AI agent frameworks",
            "session_id": "test_session"
        })
        print("Task result:", json.dumps(task_result, indent=2, default=str))
        
        # Test performance summary
        performance = await agent.get_performance_summary()
        print("Performance:", json.dumps(performance, indent=2, default=str))
        
    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())