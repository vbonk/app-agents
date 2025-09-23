# Cross-Repository Coordination Strategy

## Overview

This document defines the coordination strategy between three core repositories in Tony's development workspace:
- **saas-ecosystem-architecture**: Architecture definitions and admin app
- **app-agents**: AI agent implementations and frameworks  
- **saas-spec-driven-development**: Specification-driven development processes

## 1. Standardized PostgreSQL/Prisma Architecture

### Core Database Strategy
All repositories will use **PostgreSQL with Prisma ORM** as the standardized data layer:

```prisma
// Shared schema patterns across all repositories
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

### Repository-Specific Database Responsibilities

#### **saas-ecosystem-architecture/admin-app/prisma/schema.prisma**
- **Primary schema definition** for the entire ecosystem
- Agent management tables (agents, agent_memories, agent_tools, etc.)
- Multi-tenant organization structure
- Shared reference data and configurations

#### **app-agents/shared/database/schema.prisma**
- **Extends** the primary schema with agent-specific tables
- Runtime execution data and metrics
- Agent-specific tool registries and configurations
- Inherits from saas-ecosystem-architecture via shared models

#### **saas-spec-driven-development/prisma/schema.prisma**
- **Specification and development workflow data**
- Requirements, specifications, and development artifacts
- Links to agents and implementations via foreign keys

## 2. Schema Coordination Strategy

### Shared Model Library
```typescript
// @shared/database-models (npm package or git submodule)
export interface AgentConfig {
  id: string;
  name: string;
  version: string;
  organizationId: string;
  // ... shared types
}
```

### Cross-Repository Schema Management

1. **Primary Schema (saas-ecosystem-architecture)**
   ```bash
   # Generate shared types
   npx prisma generate
   npm run export-types  # Custom script to export TypeScript types
   ```

2. **Secondary Schemas (app-agents, saas-spec-driven-development)**
   ```bash
   # Import shared types
   npm install @tony-workspace/shared-database-types
   npx prisma generate
   ```

### Schema Update Workflow
```mermaid
graph TD
    A[Schema Change in saas-ecosystem-architecture] 
    B[Run Schema Validation]
    C[Generate Migration]
    D[Export Updated Types]
    E[Update app-agents Schema]
    F[Update saas-spec-driven-development Schema]
    G[Run Cross-Repository Tests]
    H[Deploy Changes]
    
    A --> B --> C --> D
    D --> E
    D --> F
    E --> G
    F --> G
    G --> H
```

## 3. SQLite to PostgreSQL Migration Strategy

### Migration Phases

#### Phase 1: Parallel Implementation (Current)
- Maintain SQLite code with deprecation warnings
- Implement PostgreSQL/Prisma equivalents
- Update all new development to use PostgreSQL

#### Phase 2: Data Migration Utilities
```python
# /app-agents/migration/sqlite_to_postgres.py
import sqlite3
import asyncpg
from prisma import Prisma

class SQLiteToPostgresMigrator:
    async def migrate_agent_memory(self, agent_id: str):
        """Migrate agent memory from SQLite to PostgreSQL"""
        # Extract from SQLite
        sqlite_conn = sqlite3.connect(f"agents/{agent_id}/memory.db")
        
        # Transform and load to PostgreSQL
        prisma = Prisma()
        await prisma.connect()
        
        # Migration logic here
        
    async def migrate_all_agents(self):
        """Migrate all agent data to PostgreSQL"""
        # Bulk migration process
```

#### Phase 3: Deprecation and Removal
- Remove SQLite dependencies from all repositories
- Update documentation to reflect PostgreSQL-only approach
- Archive SQLite implementations for reference

### Migration Command Structure
```bash
# Cross-repository migration commands
npm run migrate:check        # Validate migration readiness
npm run migrate:sqlite-to-pg # Execute migration
npm run migrate:validate     # Verify migration success
npm run migrate:cleanup      # Remove SQLite artifacts
```

## 4. Deployment Coordination Strategy

### Multi-Repository CI/CD Pipeline

#### Repository Dependencies
```yaml
# .github/workflows/coordinated-deployment.yml
name: Coordinated Deployment
on:
  workflow_dispatch:
    inputs:
      repositories:
        description: 'Comma-separated list of repositories to deploy'
        required: true
        default: 'saas-ecosystem-architecture,app-agents,saas-spec-driven-development'

jobs:
  coordinate-deployment:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        repo: ${{ fromJson(github.event.inputs.repositories) }}
    steps:
      - name: Deploy Repository
        uses: ./.github/actions/deploy-with-coordination
```

#### Deployment Sequence
```mermaid
graph TD
    A[saas-ecosystem-architecture Deploy]
    B[Database Migration]
    C[Schema Validation]
    D[app-agents Deploy]
    E[saas-spec-driven-development Deploy]
    F[Integration Tests]
    G[Health Checks]
    H[Rollback if Failed]
    
    A --> B --> C
    C --> D
    C --> E
    D --> F
    E --> F
    F --> G
    G --> H
```

### Environment Coordination

#### Shared Environment Variables
```bash
# .env.shared (template across all repositories)
DATABASE_URL="postgresql://user:pass@localhost:5432/saas_ecosystem"
REDIS_URL="redis://localhost:6379"
PRISMA_SCHEMA_PATH="./prisma/schema.prisma"

# Repository-specific overrides
AGENT_REGISTRY_URL="http://app-agents:3001"
SPEC_SERVICE_URL="http://saas-spec-driven-development:3002"
ADMIN_APP_URL="http://saas-ecosystem-architecture:3000"
```

#### Configuration Management
```typescript
// @shared/config
export const getEnvironmentConfig = () => ({
  database: {
    url: process.env.DATABASE_URL,
    maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS || '10')
  },
  services: {
    agentRegistry: process.env.AGENT_REGISTRY_URL,
    specService: process.env.SPEC_SERVICE_URL,
    adminApp: process.env.ADMIN_APP_URL
  }
});
```

### Health Check Coordination
```typescript
// Cross-repository health checking
export class HealthChecker {
  async checkCrossRepositoryHealth(): Promise<HealthStatus> {
    const checks = await Promise.all([
      this.checkDatabase(),
      this.checkAgentRegistry(),
      this.checkSpecService(),
      this.checkSchemaAlignment()
    ]);
    
    return {
      overall: checks.every(c => c.status === 'healthy') ? 'healthy' : 'unhealthy',
      services: checks
    };
  }
}
```

## 5. Development Workflow Coordination

### Daily Development Process
1. **Schema Changes**: Always start in saas-ecosystem-architecture
2. **Agent Development**: Use shared types from saas-ecosystem-architecture
3. **Specification Updates**: Coordinate with both other repositories
4. **Testing**: Run cross-repository integration tests before merge

### Branching Strategy
```bash
# Coordinated feature development
git checkout -b feature/cross-repo-agent-enhancement

# Work across repositories with same branch name
cd ../saas-ecosystem-architecture && git checkout -b feature/cross-repo-agent-enhancement
cd ../app-agents && git checkout -b feature/cross-repo-agent-enhancement
cd ../saas-spec-driven-development && git checkout -b feature/cross-repo-agent-enhancement
```

### Code Review Process
- **Schema changes**: Require review from all repository maintainers
- **Agent changes**: Review by architecture and spec teams
- **Deployment changes**: Multi-repository testing required

## 6. Monitoring and Observability

### Cross-Repository Metrics
```typescript
// Shared metrics collection
export const trackCrossRepositoryMetric = (
  repository: string,
  metric: string,
  value: number,
  tags: Record<string, string>
) => {
  // Send to shared monitoring system
};
```

### Deployment Dashboards
- **Schema Drift Detection**: Monitor schema differences across repositories
- **Cross-Repository Dependencies**: Track service dependencies and health
- **Migration Status**: Monitor SQLite to PostgreSQL migration progress
- **Performance Metrics**: Unified view of system performance

## Implementation Timeline

### Week 1: Foundation
- [ ] Set up shared database types package
- [ ] Implement schema coordination in saas-ecosystem-architecture
- [ ] Create migration utilities for SQLite to PostgreSQL

### Week 2: Repository Integration  
- [ ] Update app-agents to use shared schema
- [ ] Implement cross-repository health checks
- [ ] Set up coordinated CI/CD pipelines

### Week 3: Migration Execution
- [ ] Execute SQLite to PostgreSQL migration
- [ ] Validate all cross-repository integrations
- [ ] Implement monitoring and observability

### Week 4: Optimization & Documentation
- [ ] Optimize cross-repository performance
- [ ] Complete documentation updates
- [ ] Establish ongoing maintenance procedures

## Success Metrics

- **Schema Alignment**: 100% schema consistency across repositories
- **Migration Completion**: 100% SQLite to PostgreSQL migration
- **Deployment Coordination**: <5 minute cross-repository deployment time
- **Integration Health**: 99.9% cross-repository integration uptime
- **Development Velocity**: Reduced cross-repository feature development time by 50%

---

This coordination strategy ensures all three repositories work together seamlessly while maintaining their individual responsibilities and enabling efficient cross-repository development and deployment.