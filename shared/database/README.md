# Agent Database Integration

This directory contains the database layer for AI agents, providing centralized storage using Postgres/Prisma instead of local SQLite files.

## Overview

The agent framework now uses a shared Postgres database managed by the SaaS Ecosystem Architecture admin app. This provides:

- **Centralized Memory**: All agent memories stored in one database
- **Tool Registry**: Shared tool catalog across agents  
- **Performance Metrics**: Centralized tracking and analytics
- **Learning Patterns**: Cross-agent learning and optimization
- **Execution Tracking**: Complete audit trail of agent activities

## Schema

The database schema is defined in `/saas-ecosystem-architecture/admin-app/prisma/schema.prisma` and includes:

### Core Tables

- **`agents`**: Agent configuration and metadata
- **`agent_memories`**: Persistent memory storage with embeddings
- **`agent_tools`**: Tool definitions and usage statistics  
- **`agent_executions`**: Task execution tracking and performance
- **`agent_metrics`**: Performance metrics over time
- **`learning_patterns`**: Learned optimizations and patterns

### Key Features

- **Multi-tenant**: Isolated by organization
- **Performance Tracking**: Response times, success rates, token usage
- **Memory Management**: Importance scoring and semantic search ready
- **Tool Analytics**: Usage patterns and success rates
- **Learning Loops**: Pattern recognition and prompt optimization

## Usage

### 1. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Configure database connection
DATABASE_URL=postgresql://username:password@localhost:5432/saas_ecosystem_db
ORGANIZATION_ID=your_organization_id
```

### 2. Install Dependencies

```bash
pip install -r requirements-postgres.txt
```

### 3. Agent Implementation

```python
from shared.templates.enhanced_agent_base_postgres import EnhancedAgentBase
from shared.database.prisma_client import AgentConfig

class MyAgent(EnhancedAgentBase):
    def __init__(self):
        config = AgentConfig(
            name="my_agent",
            version="1.0.0", 
            description="My custom agent",
            category="OPERATIONAL",  # STRATEGIC, OPERATIONAL, SUPPORT
            capabilities=["data_analysis", "reporting"],
            data_sources=["database", "api"]
        )
        super().__init__(config)
    
    async def execute_task(self, task):
        # Your task implementation
        return {"status": "completed", "result": "..."}
    
    def get_capabilities(self):
        return self.config.capabilities

# Usage
async def main():
    agent = MyAgent()
    await agent.initialize()  # Connect to database and register
    
    # Execute tasks
    result = await agent.execute_task({"type": "analysis", "data": "..."})
    
    # Cleanup
    await agent.cleanup()
```

### 4. Database Client Direct Usage

```python
from shared.database.prisma_client import get_agent_client

async def example():
    client = get_agent_client()
    await client.connect()
    
    # Store memory
    memory = MemoryEntry(
        agent_id="agent_123",
        content="Important insight discovered",
        metadata={"category": "insight", "confidence": 0.9},
        importance=0.8
    )
    memory_id = await client.store_memory(memory)
    
    # Retrieve memories
    memories = await client.retrieve_memories("agent_123", query="insight")
    
    # Record metrics
    await client.record_metric("agent_123", "accuracy", 0.95, "percentage")
    
    await client.disconnect()
```

## Migration from SQLite

For existing agents using the old SQLite-based system:

### 1. Update Imports

```python
# OLD - deprecated
from shared.templates.enhanced_agent_base import EnhancedAgentBase

# NEW - recommended  
from shared.templates.enhanced_agent_base_postgres import EnhancedAgentBase
```

### 2. Add Async Initialization

```python
# OLD
agent = MyAgent()

# NEW
agent = MyAgent()
await agent.initialize()  # Required for database setup
```

### 3. Update Configuration

```python
# OLD
config = AgentConfig(
    name="my_agent",
    capabilities=["research"],
    data_sources=["web"]
)

# NEW - category required
config = AgentConfig(
    name="my_agent", 
    category="STRATEGIC",  # New required field
    capabilities=["research"],
    data_sources=["web"]
)
```

### 4. Migration Script

A migration script can be created to transfer existing SQLite data:

```python
# migrate_sqlite_to_postgres.py
async def migrate_agent_data(agent_name, sqlite_path):
    # Read from SQLite
    conn = sqlite3.connect(sqlite_path)
    
    # Transfer to Postgres
    client = get_agent_client()
    await client.connect()
    
    # Migrate memories, tools, etc.
    # Implementation depends on specific data structure
```

## Performance Considerations

- **Connection Pooling**: Automatic connection pool management
- **Batch Operations**: Use transactions for multiple operations
- **Memory Indexing**: Indexed by agent, importance, and timestamp
- **Metric Aggregation**: Efficient time-series queries for analytics

## Monitoring

The database client provides built-in monitoring:

```python
# Health check
health = await client.health_check()

# Performance metrics
metrics = await client.get_agent_metrics("agent_123", hours=24)

# Learning patterns
patterns = await client.get_learning_patterns("agent_123", min_confidence=0.7)
```

## Security

- **Organization Isolation**: All queries filtered by organization
- **Connection Security**: SSL/TLS for database connections
- **Data Encryption**: Sensitive data encrypted at rest
- **Access Logging**: All database operations logged

## Development

### Running Tests

```bash
pytest shared/database/tests/ -v
```

### Database Schema Updates

Schema changes should be made in the main SaaS Ecosystem Architecture project:

1. Update `/saas-ecosystem-architecture/admin-app/prisma/schema.prisma`
2. Run `npx prisma db push` or create migration
3. Update Python client if needed
4. Test with existing agents

### Adding New Features

When adding new database features:

1. Update Prisma schema
2. Add methods to `PrismaAgentClient`
3. Update `EnhancedAgentBase` if needed
4. Add tests
5. Update documentation