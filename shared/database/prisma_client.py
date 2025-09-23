"""
Prisma Database Client for AI Agents
Provides connection to the centralized Postgres database using Prisma-compatible queries.
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from dataclasses import dataclass, asdict
import asyncpg
from asyncpg import Connection, Pool


@dataclass
class AgentConfig:
    """Configuration for agent behavior and capabilities."""
    name: str
    version: str
    description: str
    category: str  # STRATEGIC, OPERATIONAL, SUPPORT
    capabilities: List[str]
    data_sources: List[str]
    memory_enabled: bool = True
    learning_enabled: bool = True
    tool_discovery_enabled: bool = True
    system_prompt: Optional[str] = None
    chat_prompt: Optional[str] = None


@dataclass
class MemoryEntry:
    """Represents a memory entry in the agent's persistent storage."""
    id: Optional[str]
    agent_id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    importance: float = 0.5
    created_at: Optional[datetime] = None
    accessed_at: Optional[datetime] = None


@dataclass
class ToolInfo:
    """Information about an available tool."""
    id: Optional[str]
    agent_id: str
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    usage_count: int = 0
    success_rate: float = 0.0
    is_enabled: bool = True
    priority: int = 1


@dataclass
class ExecutionRecord:
    """Record of an agent execution."""
    id: Optional[str]
    agent_id: str
    task_type: str
    task_data: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    response_time: Optional[float] = None
    tokens_used: Optional[int] = None
    tools_used: Optional[List[str]] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    organization_id: str = ""


class PrismaAgentClient:
    """
    Database client for AI agents using direct Postgres connection
    with Prisma-compatible schema.
    """
    
    def __init__(self, database_url: str = None, organization_id: str = None):
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.organization_id = organization_id or os.getenv("ORGANIZATION_ID", "default")
        self.pool: Optional[Pool] = None
        self.logger = logging.getLogger(__name__)
        
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")
    
    async def connect(self):
        """Initialize the database connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=1,
                max_size=10,
                command_timeout=60
            )
            self.logger.info("Connected to Postgres database")
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise
    
    async def disconnect(self):
        """Close the database connection pool."""
        if self.pool:
            await self.pool.close()
            self.logger.info("Disconnected from database")
    
    async def _execute_query(self, query: str, *args):
        """Execute a query and return results."""
        if not self.pool:
            await self.connect()
        
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def _execute_single(self, query: str, *args):
        """Execute a query and return a single result."""
        if not self.pool:
            await self.connect()
        
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
    
    async def _execute_update(self, query: str, *args):
        """Execute an update/insert query."""
        if not self.pool:
            await self.connect()
        
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    # =========================================================================
    # AGENT MANAGEMENT
    # =========================================================================
    
    async def create_or_update_agent(self, config: AgentConfig) -> str:
        """Create or update an agent in the database."""
        query = """
            INSERT INTO agents (
                name, version, description, category, capabilities, 
                data_sources, memory_enabled, learning_enabled, 
                tool_discovery_enabled, system_prompt, chat_prompt, 
                organization_id, created_at, updated_at
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14
            )
            ON CONFLICT (name) DO UPDATE SET
                version = EXCLUDED.version,
                description = EXCLUDED.description,
                category = EXCLUDED.category,
                capabilities = EXCLUDED.capabilities,
                data_sources = EXCLUDED.data_sources,
                memory_enabled = EXCLUDED.memory_enabled,
                learning_enabled = EXCLUDED.learning_enabled,
                tool_discovery_enabled = EXCLUDED.tool_discovery_enabled,
                system_prompt = EXCLUDED.system_prompt,
                chat_prompt = EXCLUDED.chat_prompt,
                updated_at = EXCLUDED.updated_at
            RETURNING id
        """
        
        now = datetime.now()
        result = await self._execute_single(
            query,
            config.name,
            config.version,
            config.description,
            config.category,
            json.dumps(config.capabilities),
            json.dumps(config.data_sources),
            config.memory_enabled,
            config.learning_enabled,
            config.tool_discovery_enabled,
            config.system_prompt,
            config.chat_prompt,
            self.organization_id,
            now,
            now
        )
        
        agent_id = result['id']
        self.logger.info(f"Created/updated agent: {config.name} (ID: {agent_id})")
        return agent_id
    
    async def get_agent(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get agent information by name."""
        query = """
            SELECT * FROM agents 
            WHERE name = $1 AND organization_id = $2
        """
        
        result = await self._execute_single(query, agent_name, self.organization_id)
        if result:
            agent_dict = dict(result)
            # Parse JSON fields
            agent_dict['capabilities'] = json.loads(agent_dict['capabilities'])
            agent_dict['data_sources'] = json.loads(agent_dict['data_sources'])
            return agent_dict
        return None
    
    async def update_agent_status(self, agent_name: str, status: str) -> bool:
        """Update agent status (ACTIVE, INACTIVE, MAINTENANCE, DEPRECATED)."""
        query = """
            UPDATE agents 
            SET status = $1, updated_at = $2
            WHERE name = $3 AND organization_id = $4
        """
        
        result = await self._execute_update(
            query, status, datetime.now(), agent_name, self.organization_id
        )
        return "UPDATE 1" in result
    
    # =========================================================================
    # MEMORY MANAGEMENT
    # =========================================================================
    
    async def store_memory(self, memory: MemoryEntry) -> str:
        """Store a memory entry for an agent."""
        query = """
            INSERT INTO agent_memories (
                agent_id, content, metadata, embedding, importance,
                created_at, accessed_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
        """
        
        now = datetime.now()
        result = await self._execute_single(
            query,
            memory.agent_id,
            memory.content,
            json.dumps(memory.metadata),
            json.dumps(memory.embedding) if memory.embedding else None,
            memory.importance,
            now,
            now
        )
        
        memory_id = result['id']
        self.logger.info(f"Stored memory for agent {memory.agent_id}: {memory_id}")
        return memory_id
    
    async def retrieve_memories(
        self, 
        agent_id: str, 
        query: Optional[str] = None, 
        limit: int = 10,
        min_importance: float = 0.0
    ) -> List[MemoryEntry]:
        """Retrieve memories for an agent."""
        if query:
            sql = """
                SELECT * FROM agent_memories 
                WHERE agent_id = $1 AND content ILIKE $2 AND importance >= $3
                ORDER BY importance DESC, accessed_at DESC 
                LIMIT $4
            """
            results = await self._execute_query(
                sql, agent_id, f"%{query}%", min_importance, limit
            )
        else:
            sql = """
                SELECT * FROM agent_memories 
                WHERE agent_id = $1 AND importance >= $2
                ORDER BY importance DESC, accessed_at DESC 
                LIMIT $3
            """
            results = await self._execute_query(sql, agent_id, min_importance, limit)
        
        memories = []
        for row in results:
            memory = MemoryEntry(
                id=row['id'],
                agent_id=row['agent_id'],
                content=row['content'],
                metadata=json.loads(row['metadata']),
                embedding=json.loads(row['embedding']) if row['embedding'] else None,
                importance=row['importance'],
                created_at=row['created_at'],
                accessed_at=row['accessed_at']
            )
            memories.append(memory)
        
        # Update accessed_at for retrieved memories
        if memories:
            memory_ids = [m.id for m in memories]
            await self._execute_update(
                "UPDATE agent_memories SET accessed_at = $1 WHERE id = ANY($2)",
                datetime.now(), memory_ids
            )
        
        return memories
    
    # =========================================================================
    # TOOL MANAGEMENT
    # =========================================================================
    
    async def register_tool(self, tool: ToolInfo) -> str:
        """Register a tool for an agent."""
        query = """
            INSERT INTO agent_tools (
                agent_id, name, description, input_schema, output_schema,
                usage_count, success_rate, is_enabled, priority,
                created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            ON CONFLICT (agent_id, name) DO UPDATE SET
                description = EXCLUDED.description,
                input_schema = EXCLUDED.input_schema,
                output_schema = EXCLUDED.output_schema,
                is_enabled = EXCLUDED.is_enabled,
                priority = EXCLUDED.priority,
                updated_at = EXCLUDED.updated_at
            RETURNING id
        """
        
        now = datetime.now()
        result = await self._execute_single(
            query,
            tool.agent_id,
            tool.name,
            tool.description,
            json.dumps(tool.input_schema),
            json.dumps(tool.output_schema),
            tool.usage_count,
            tool.success_rate,
            tool.is_enabled,
            tool.priority,
            now,
            now
        )
        
        return result['id']
    
    async def get_agent_tools(self, agent_id: str, enabled_only: bool = True) -> List[ToolInfo]:
        """Get all tools for an agent."""
        if enabled_only:
            query = """
                SELECT * FROM agent_tools 
                WHERE agent_id = $1 AND is_enabled = true
                ORDER BY priority DESC, name
            """
            results = await self._execute_query(query, agent_id)
        else:
            query = """
                SELECT * FROM agent_tools 
                WHERE agent_id = $1
                ORDER BY priority DESC, name
            """
            results = await self._execute_query(query, agent_id)
        
        tools = []
        for row in results:
            tool = ToolInfo(
                id=row['id'],
                agent_id=row['agent_id'],
                name=row['name'],
                description=row['description'],
                input_schema=json.loads(row['input_schema']),
                output_schema=json.loads(row['output_schema']),
                usage_count=row['usage_count'],
                success_rate=row['success_rate'],
                is_enabled=row['is_enabled'],
                priority=row['priority']
            )
            tools.append(tool)
        
        return tools
    
    async def update_tool_usage(self, agent_id: str, tool_name: str, success: bool):
        """Update tool usage statistics."""
        query = """
            UPDATE agent_tools 
            SET usage_count = usage_count + 1,
                success_rate = (
                    CASE 
                        WHEN $3 THEN (success_rate * usage_count + 1.0) / (usage_count + 1)
                        ELSE (success_rate * usage_count) / (usage_count + 1)
                    END
                ),
                last_used_at = $4,
                updated_at = $4
            WHERE agent_id = $1 AND name = $2
        """
        
        now = datetime.now()
        await self._execute_update(query, agent_id, tool_name, success, now)
    
    # =========================================================================
    # EXECUTION TRACKING
    # =========================================================================
    
    async def create_execution(self, execution: ExecutionRecord) -> str:
        """Create a new execution record."""
        query = """
            INSERT INTO agent_executions (
                agent_id, task_type, task_data, status, started_at,
                session_id, user_id, organization_id
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """
        
        result = await self._execute_single(
            query,
            execution.agent_id,
            execution.task_type,
            json.dumps(execution.task_data),
            execution.status,
            execution.started_at or datetime.now(),
            execution.session_id,
            execution.user_id,
            self.organization_id
        )
        
        return result['id']
    
    async def update_execution(
        self, 
        execution_id: str, 
        status: str, 
        result: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        response_time: Optional[float] = None,
        tokens_used: Optional[int] = None,
        tools_used: Optional[List[str]] = None
    ):
        """Update an execution record."""
        query = """
            UPDATE agent_executions 
            SET status = $2, result = $3, error_message = $4,
                completed_at = $5, response_time = $6, tokens_used = $7,
                tools_used = $8
            WHERE id = $1
        """
        
        await self._execute_update(
            query,
            execution_id,
            status,
            json.dumps(result) if result else None,
            error_message,
            datetime.now(),
            response_time,
            tokens_used,
            json.dumps(tools_used) if tools_used else None
        )
    
    # =========================================================================
    # METRICS TRACKING
    # =========================================================================
    
    async def record_metric(
        self, 
        agent_id: str, 
        metric_type: str, 
        value: float, 
        unit: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record a performance metric for an agent."""
        query = """
            INSERT INTO agent_metrics (
                agent_id, metric_type, value, unit, metadata, timestamp
            ) VALUES ($1, $2, $3, $4, $5, $6)
        """
        
        await self._execute_update(
            query,
            agent_id,
            metric_type,
            value,
            unit,
            json.dumps(metadata) if metadata else None,
            datetime.now()
        )
    
    async def get_agent_metrics(
        self, 
        agent_id: str, 
        metric_type: Optional[str] = None,
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Get recent metrics for an agent."""
        if metric_type:
            query = """
                SELECT * FROM agent_metrics 
                WHERE agent_id = $1 AND metric_type = $2 
                AND timestamp > NOW() - INTERVAL '%s hours'
                ORDER BY timestamp DESC
            """ % hours
            results = await self._execute_query(query, agent_id, metric_type)
        else:
            query = """
                SELECT * FROM agent_metrics 
                WHERE agent_id = $1 
                AND timestamp > NOW() - INTERVAL '%s hours'
                ORDER BY timestamp DESC
            """ % hours
            results = await self._execute_query(query, agent_id)
        
        metrics = []
        for row in results:
            metric = {
                'id': row['id'],
                'agent_id': row['agent_id'],
                'metric_type': row['metric_type'],
                'value': float(row['value']),
                'unit': row['unit'],
                'metadata': json.loads(row['metadata']) if row['metadata'] else None,
                'timestamp': row['timestamp']
            }
            metrics.append(metric)
        
        return metrics
    
    # =========================================================================
    # LEARNING PATTERNS
    # =========================================================================
    
    async def store_learning_pattern(
        self,
        agent_id: str,
        pattern_type: str,
        pattern_data: Dict[str, Any],
        confidence: float,
        source_executions: int = 1,
        improvement_gain: Optional[float] = None
    ) -> str:
        """Store a learning pattern for an agent."""
        query = """
            INSERT INTO learning_patterns (
                agent_id, pattern_type, pattern_data, confidence,
                source_executions, improvement_gain, created_at, updated_at
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """
        
        now = datetime.now()
        result = await self._execute_single(
            query,
            agent_id,
            pattern_type,
            json.dumps(pattern_data),
            confidence,
            source_executions,
            improvement_gain,
            now,
            now
        )
        
        return result['id']
    
    async def get_learning_patterns(
        self, 
        agent_id: str, 
        pattern_type: Optional[str] = None,
        min_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Get learning patterns for an agent."""
        if pattern_type:
            query = """
                SELECT * FROM learning_patterns 
                WHERE agent_id = $1 AND pattern_type = $2 AND confidence >= $3
                ORDER BY confidence DESC, updated_at DESC
            """
            results = await self._execute_query(query, agent_id, pattern_type, min_confidence)
        else:
            query = """
                SELECT * FROM learning_patterns 
                WHERE agent_id = $1 AND confidence >= $2
                ORDER BY confidence DESC, updated_at DESC
            """
            results = await self._execute_query(query, agent_id, min_confidence)
        
        patterns = []
        for row in results:
            pattern = {
                'id': row['id'],
                'agent_id': row['agent_id'],
                'pattern_type': row['pattern_type'],
                'pattern_data': json.loads(row['pattern_data']),
                'confidence': row['confidence'],
                'source_executions': row['source_executions'],
                'improvement_gain': row['improvement_gain'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'last_applied_at': row['last_applied_at']
            }
            patterns.append(pattern)
        
        return patterns
    
    # =========================================================================
    # HEALTH CHECK
    # =========================================================================
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check of the database connection."""
        try:
            result = await self._execute_single("SELECT 1 as health")
            return {
                "status": "healthy",
                "database": "connected",
                "organization_id": self.organization_id,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


# Singleton instance for easy usage
_global_client: Optional[PrismaAgentClient] = None

def get_agent_client(database_url: str = None, organization_id: str = None) -> PrismaAgentClient:
    """Get or create the global agent database client."""
    global _global_client
    if _global_client is None:
        _global_client = PrismaAgentClient(database_url, organization_id)
    return _global_client


async def initialize_agent_db():
    """Initialize the agent database connection."""
    client = get_agent_client()
    await client.connect()
    return client


async def cleanup_agent_db():
    """Cleanup the agent database connection."""
    global _global_client
    if _global_client:
        await _global_client.disconnect()
        _global_client = None