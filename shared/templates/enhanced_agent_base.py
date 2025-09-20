"""
Enhanced Agent Base Template
Implements all required standards and specifications for app-agents repository.
"""

import asyncio
import json
import sqlite3
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from pathlib import Path
import pandas as pd
import requests
from dataclasses import dataclass, asdict
import yaml
import xml.etree.ElementTree as ET


@dataclass
class AgentConfig:
    """Configuration for agent behavior and capabilities."""
    name: str
    version: str
    description: str
    capabilities: List[str]
    data_sources: List[str]
    memory_enabled: bool = True
    learning_enabled: bool = True
    tool_discovery_enabled: bool = True


@dataclass
class MemoryEntry:
    """Represents a memory entry in the agent's persistent storage."""
    id: str
    timestamp: datetime
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None


@dataclass
class ToolInfo:
    """Information about an available tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    usage_count: int = 0


class EnhancedAgentBase(ABC):
    """
    Enhanced base class for all agents in the app-agents repository.
    Implements all required standards and specifications.
    """
    
    def __init__(self, config: AgentConfig, data_dir: str = "./data"):
        self.config = config
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Initialize memory system
        self.memory_db_path = self.data_dir / f"{config.name}_memory.db"
        self._init_memory_system()
        
        # Initialize tool registry
        self.tools: Dict[str, ToolInfo] = {}
        if config.tool_discovery_enabled:
            self._discover_tools()
        
        # Performance metrics
        self.metrics: Dict[str, List[float]] = {
            "task_completion_rate": [],
            "accuracy_scores": [],
            "response_times": [],
            "user_satisfaction": []
        }
        
        self.logger.info(f"Initialized {config.name} agent v{config.version}")
    
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
    
    def _init_memory_system(self):
        """Initialize the persistent memory system."""
        conn = sqlite3.connect(self.memory_db_path)
        cursor = conn.cursor()
        
        # Create memory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                content TEXT,
                metadata TEXT,
                embedding TEXT
            )
        ''')
        
        # Create learning patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_patterns (
                id TEXT PRIMARY KEY,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence REAL,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _discover_tools(self):
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
            tool = ToolInfo(**tool_data)
            self.tools[tool.name] = tool
        
        self.logger.info(f"Discovered {len(self.tools)} tools")
    
    def store_memory(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Store information in persistent memory."""
        if not self.config.memory_enabled:
            return ""
        
        memory_id = f"{self.config.name}_{datetime.now().isoformat()}"
        entry = MemoryEntry(
            id=memory_id,
            timestamp=datetime.now(),
            content=content,
            metadata=metadata or {}
        )
        
        conn = sqlite3.connect(self.memory_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memory (id, timestamp, content, metadata, embedding)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            entry.id,
            entry.timestamp.isoformat(),
            entry.content,
            json.dumps(entry.metadata),
            json.dumps(entry.embedding) if entry.embedding else None
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Stored memory entry: {memory_id}")
        return memory_id
    
    def retrieve_memory(self, query: str = None, limit: int = 10) -> List[MemoryEntry]:
        """Retrieve information from persistent memory."""
        if not self.config.memory_enabled:
            return []
        
        conn = sqlite3.connect(self.memory_db_path)
        cursor = conn.cursor()
        
        if query:
            cursor.execute('''
                SELECT * FROM memory 
                WHERE content LIKE ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (f"%{query}%", limit))
        else:
            cursor.execute('''
                SELECT * FROM memory 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            memories.append(MemoryEntry(
                id=row[0],
                timestamp=datetime.fromisoformat(row[1]),
                content=row[2],
                metadata=json.loads(row[3]),
                embedding=json.loads(row[4]) if row[4] else None
            ))
        
        return memories
    
    def use_tool(self, tool_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Use an available tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        tool.usage_count += 1
        
        # Log tool usage
        self.logger.info(f"Using tool: {tool_name} with inputs: {inputs}")
        
        # This would integrate with the actual tool implementation
        # For now, return a mock response
        return {
            "tool": tool_name,
            "status": "success",
            "result": f"Mock result from {tool_name}",
            "timestamp": datetime.now().isoformat()
        }
    
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
    
    def conduct_multi_source_research(self, query: str, sources: List[str] = None) -> Dict[str, Any]:
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
                    # Mock web search
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
        self.store_memory(
            content=f"Research: {query}",
            metadata={"type": "research", "results": results}
        )
        
        return results
    
    def enrich_dataset(self, dataset_id: str, new_data: Any) -> Dict[str, Any]:
        """Enrich existing dataset with new information."""
        # This would integrate with the dataset management system
        enrichment_result = {
            "dataset_id": dataset_id,
            "enrichment_timestamp": datetime.now().isoformat(),
            "new_data_size": len(str(new_data)),
            "status": "success"
        }
        
        self.logger.info(f"Enriched dataset {dataset_id}")
        return enrichment_result
    
    def optimize_prompts(self, current_prompt: str, performance_data: Dict[str, Any]) -> str:
        """Optimize prompts based on performance data."""
        if not self.config.learning_enabled:
            return current_prompt
        
        # Simple optimization logic - in practice, this would be more sophisticated
        optimized_prompt = current_prompt
        
        if performance_data.get("accuracy", 0) < 0.7:
            optimized_prompt += "\n\nPlease be more precise and accurate in your response."
        
        if performance_data.get("response_time", 0) > 10:
            optimized_prompt += "\n\nProvide a concise response."
        
        # Store optimization in learning patterns
        conn = sqlite3.connect(self.memory_db_path)
        cursor = conn.cursor()
        
        pattern_id = f"prompt_opt_{datetime.now().isoformat()}"
        cursor.execute('''
            INSERT INTO learning_patterns (id, pattern_type, pattern_data, confidence, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            pattern_id,
            "prompt_optimization",
            json.dumps({
                "original": current_prompt,
                "optimized": optimized_prompt,
                "performance": performance_data
            }),
            0.8,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.info("Optimized prompt based on performance data")
        return optimized_prompt
    
    def record_metric(self, metric_name: str, value: float):
        """Record a performance metric."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        
        self.metrics[metric_name].append(value)
        self.logger.info(f"Recorded metric {metric_name}: {value}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of agent performance metrics."""
        summary = {}
        
        for metric_name, values in self.metrics.items():
            if values:
                summary[metric_name] = {
                    "count": len(values),
                    "average": sum(values) / len(values),
                    "min": min(values),
                    "max": max(values),
                    "latest": values[-1]
                }
            else:
                summary[metric_name] = {
                    "count": 0,
                    "average": 0,
                    "min": 0,
                    "max": 0,
                    "latest": 0
                }
        
        return summary
    
    @abstractmethod
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities. Must be implemented by subclasses."""
        pass
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check of the agent."""
        return {
            "agent": self.config.name,
            "version": self.config.version,
            "status": "healthy",
            "memory_enabled": self.config.memory_enabled,
            "learning_enabled": self.config.learning_enabled,
            "tools_available": len(self.tools),
            "memory_entries": len(self.retrieve_memory()),
            "timestamp": datetime.now().isoformat()
        }


# Example implementation
class ExampleAgent(EnhancedAgentBase):
    """Example implementation of the enhanced agent base."""
    
    def __init__(self):
        config = AgentConfig(
            name="example_agent",
            version="1.0.0",
            description="Example agent demonstrating enhanced capabilities",
            capabilities=["research", "analysis", "content_generation"],
            data_sources=["web", "database", "files"]
        )
        super().__init__(config)
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task."""
        task_type = task.get("type", "unknown")
        
        if task_type == "research":
            return self.conduct_multi_source_research(
                query=task.get("query", ""),
                sources=task.get("sources")
            )
        
        elif task_type == "analysis":
            # Mock analysis task
            return {
                "task_type": "analysis",
                "result": "Analysis completed",
                "timestamp": datetime.now().isoformat()
            }
        
        else:
            return {
                "error": f"Unknown task type: {task_type}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return self.config.capabilities


if __name__ == "__main__":
    # Example usage
    agent = ExampleAgent()
    
    # Test health check
    health = agent.health_check()
    print("Health Check:", json.dumps(health, indent=2))
    
    # Test memory
    memory_id = agent.store_memory("Test memory entry", {"type": "test"})
    memories = agent.retrieve_memory()
    print(f"Stored memory: {memory_id}")
    print(f"Retrieved {len(memories)} memories")
    
    # Test tool usage
    try:
        result = agent.use_tool("web_search", {"query": "test", "limit": 5})
        print("Tool result:", result)
    except Exception as e:
        print("Tool error:", e)
    
    # Test dataset loading
    try:
        # This would work with an actual file
        # data = agent.load_dataset("test.json")
        print("Dataset loading capability available")
    except Exception as e:
        print("Dataset loading test skipped (no test file)")
