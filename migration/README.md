# SQLite to PostgreSQL Migration Guide

## Overview

This directory contains tools and documentation for migrating agent data from SQLite databases to PostgreSQL with Prisma ORM, as part of the workspace-wide standardization on PostgreSQL/Prisma architecture.

## Migration Strategy

### Phase 1: Parallel Implementation ✅
- SQLite code maintained with deprecation warnings
- PostgreSQL/Prisma equivalents implemented
- All new development uses PostgreSQL

### Phase 2: Data Migration (Current)
- Migrate existing agent data using automated tools
- Validate data integrity across systems
- Maintain backward compatibility during transition

### Phase 3: Deprecation and Cleanup (Planned)
- Remove SQLite dependencies
- Update all documentation
- Archive SQLite implementations

## Migration Tools

### `sqlite_to_postgres_migrator.py`

**Purpose**: Automated migration of agent data from SQLite to PostgreSQL

**Usage**:
```bash
# Dry run (recommended first)
python migration/sqlite_to_postgres_migrator.py \
  --postgres-url "postgresql://user:pass@localhost:5432/saas_ecosystem" \
  --agents-path "./agents" \
  --dry-run

# Create backup script
python migration/sqlite_to_postgres_migrator.py \
  --postgres-url "postgresql://user:pass@localhost:5432/saas_ecosystem" \
  --agents-path "./agents" \
  --backup

# Execute migration
python migration/sqlite_to_postgres_migrator.py \
  --postgres-url "postgresql://user:pass@localhost:5432/saas_ecosystem" \
  --agents-path "./agents"
```

**Features**:
- Automatic discovery of SQLite databases
- Extraction of memory, tools, and metrics data
- Transaction-safe PostgreSQL insertion
- Comprehensive migration reporting
- Backup script generation

### Migration Process

1. **Pre-Migration Checklist**
   ```bash
   # Verify PostgreSQL schema is up to date
   cd /Users/tony/Projects/saas-ecosystem-architecture/admin-app
   npx prisma generate
   npx prisma db push
   
   # Back up SQLite databases
   python migration/sqlite_to_postgres_migrator.py --backup
   bash backup_sqlite.sh
   ```

2. **Execute Migration**
   ```bash
   # Dry run first
   python migration/sqlite_to_postgres_migrator.py \
     --postgres-url "$DATABASE_URL" \
     --dry-run
   
   # If dry run succeeds, execute migration
   python migration/sqlite_to_postgres_migrator.py \
     --postgres-url "$DATABASE_URL"
   ```

3. **Post-Migration Validation**
   ```bash
   # Check migration report
   cat migration_report_*.json
   
   # Validate data in PostgreSQL
   psql $DATABASE_URL -c "SELECT COUNT(*) FROM agent_memories;"
   psql $DATABASE_URL -c "SELECT COUNT(*) FROM agent_tools;"
   psql $DATABASE_URL -c "SELECT COUNT(*) FROM agent_metrics;"
   ```

## Data Mapping

### SQLite to PostgreSQL Schema Mapping

| SQLite Table | PostgreSQL Table | Notes |
|--------------|------------------|-------|
| `memory`, `agent_memory` | `agent_memories` | Memory entries with embeddings |
| `tools`, `agent_tools` | `agent_tools` | Tool registry and configurations |
| `metrics`, `performance` | `agent_metrics` | Performance and execution metrics |
| `execution_log` | `agent_executions` | Task execution history |

### Data Transformation

```python
# SQLite Record
{
  "id": 1,
  "content": "User query about pricing",
  "timestamp": "2024-01-15 10:30:00"
}

# PostgreSQL Record
{
  "id": "cm1234567890abcdef",  # UUID
  "agent_id": "operational_crawler",
  "content": "{\"content\": \"User query about pricing\", \"timestamp\": \"2024-01-15 10:30:00\"}",
  "metadata": {"source_table": "memory", "migrated_at": "2024-01-15T10:30:00Z"},
  "embedding": null,  # Will be populated by future AI processing
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Agent Updates Required

### 1. Update Import Statements
```python
# Old (deprecated)
from shared.templates.enhanced_agent_base import EnhancedAgentBase

# New (recommended)
from shared.templates.enhanced_agent_base_postgres import EnhancedAgentBase
```

### 2. Update Database Configuration
```python
# Old (SQLite)
agent_config = AgentConfig(
    name="my_agent",
    memory_enabled=True,
    memory_backend="sqlite"
)

# New (PostgreSQL)
agent_config = AgentConfig(
    name="my_agent",
    memory_enabled=True,
    memory_backend="postgres",
    database_url=os.getenv("DATABASE_URL")
)
```

### 3. Update Memory Operations
```python
# Old (SQLite)
await self.store_memory("key", data)
result = await self.retrieve_memory("key")

# New (PostgreSQL) - Same interface, different backend
await self.store_memory("key", data)  # Now uses PostgreSQL
result = await self.retrieve_memory("key")  # Vector search enabled
```

## Environment Variables

```bash
# Required for PostgreSQL connection
DATABASE_URL="postgresql://user:pass@localhost:5432/saas_ecosystem"

# Optional migration settings
MIGRATION_BATCH_SIZE=100
MIGRATION_TIMEOUT=300
MIGRATION_BACKUP_PATH="./backups"
```

## Troubleshooting

### Common Issues

1. **Connection Errors**
   ```
   Error: could not connect to server
   ```
   - Verify PostgreSQL is running
   - Check DATABASE_URL format
   - Ensure network connectivity

2. **Schema Errors**
   ```
   Error: relation "agent_memories" does not exist
   ```
   - Run Prisma migrations: `npx prisma db push`
   - Verify schema is up to date

3. **Permission Errors**
   ```
   Error: permission denied for table agent_memories
   ```
   - Check PostgreSQL user permissions
   - Ensure user can CREATE, INSERT, UPDATE, DELETE

### Migration Validation

```sql
-- Check migration completeness
SELECT 
  a.name as agent_name,
  COUNT(m.id) as memory_count,
  COUNT(t.id) as tool_count,
  COUNT(mt.id) as metric_count
FROM agents a
LEFT JOIN agent_memories m ON a.id = m.agent_id
LEFT JOIN agent_tools t ON a.id = t.agent_id  
LEFT JOIN agent_metrics mt ON a.id = mt.agent_id
GROUP BY a.name;

-- Verify recent migrations
SELECT 
  agent_id,
  COUNT(*) as records,
  MAX(created_at) as latest_record
FROM agent_memories 
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY agent_id;
```

## Rollback Procedure

If migration issues occur:

1. **Stop all agent processes**
2. **Restore from backup**
   ```bash
   # Restore SQLite files
   cp ./backups/sqlite_backup_*/\* ./agents/
   ```
3. **Revert to SQLite-based agents**
   ```python
   # Temporarily use deprecated SQLite base
   from shared.templates.enhanced_agent_base import EnhancedAgentBase
   ```
4. **Investigate and fix issues**
5. **Retry migration**

## Migration Timeline

- **Week 1**: Backup and dry-run testing
- **Week 2**: Phased migration of non-critical agents
- **Week 3**: Migration of production agents
- **Week 4**: Validation and SQLite cleanup

## Success Criteria

- ✅ All agent data successfully migrated
- ✅ No data loss or corruption
- ✅ Performance meets or exceeds SQLite baseline
- ✅ All agents running on PostgreSQL/Prisma
- ✅ SQLite dependencies removed
- ✅ Documentation updated

## Support

For migration issues or questions:
1. Check migration logs and reports
2. Review this documentation
3. Validate PostgreSQL schema alignment
4. Test with dry-run before production migration