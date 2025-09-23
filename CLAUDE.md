# CLAUDE.md - App Agents Development Guidance

## Project Overview

The **App Agents** repository is a production-ready AI agent development platform that provides a comprehensive framework for building, deploying, and managing intelligent agents in SaaS environments. This repository is now fully standardized on PostgreSQL/Prisma architecture and integrates seamlessly with the broader SaaS ecosystem.

## 🎯 Current Status

### ✅ Production Ready - All Systems Operational
- **Database Architecture**: Fully migrated to PostgreSQL/Prisma
- **Agent Framework**: 4 production agents (v2.0.0) with comprehensive capabilities
- **Cross-Repository Integration**: Seamless coordination with saas-ecosystem-architecture
- **Quality Standards**: 90%+ test coverage, comprehensive documentation
- **Security Compliance**: Enterprise-grade security implementation

### 📊 Agent Inventory
1. **Enhanced Crawler Agent v2.0.0** (`agents/operational/crawler/`)
   - Multi-source research capabilities
   - PostgreSQL memory persistence
   - Dataset enrichment and analysis
   - Performance: 94.2% completion rate

2. **Enhanced Agent-Builder v2.0.0** (`agents/support/agent-builder/`)
   - Best practices integration
   - Code generation and templating
   - PostgreSQL integration patterns
   - Standards compliance enforcement

3. **Enhanced UI-Architect-Agent v2.0.0** (`agents/support/ui-architect-agent/`)
   - Multi-dimensional design analysis
   - Component generation
   - Database-backed design patterns
   - UI/UX research integration

4. **Enhanced Prompt-Researcher v2.0.0** (`agents/strategic/prompt-researcher/`)
   - Advanced memory system with PostgreSQL
   - Learning engine and optimization
   - Multi-source integration
   - Performance analytics

## 🏗️ Architecture Integration

### Central Database Architecture
```typescript
// All agents now use centralized PostgreSQL database
import { PrismaAgentClient } from '@/shared/database/prisma_client';

const agentClient = new PrismaAgentClient();
await agentClient.connect();

// Shared across saas-ecosystem-architecture
const agentConfig = await agentClient.create_or_update_agent({
  name: "my_agent",
  version: "2.0.0",
  category: "OPERATIONAL",
  capabilities: ["research", "analysis", "memory"],
  organizationId: "org_123"
});
```

### Cross-Repository Coordination
- **Primary Schema**: `saas-ecosystem-architecture/admin-app/prisma/schema.prisma`
- **Agent Implementation**: `app-agents/shared/database/prisma_client.py`
- **Coordination Tool**: `app-agents/scripts/validate_cross_repo_alignment.py`

## 🚀 Development Workflow

### Creating New Agents

#### 1. Use Enhanced Agent-Builder
```bash
cd agents/support/agent-builder
python src/enhanced_agent_builder.py --agent-name "my_new_agent" --category "operational"
```

#### 2. Inherit from PostgreSQL Base
```python
from shared.templates.enhanced_agent_base_postgres import EnhancedAgentBase

class MyNewAgent(EnhancedAgentBase):
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        # PostgreSQL connection automatically configured
```

#### 3. Implement Required Standards
```python
async def execute_task(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
    # Multi-source research (required)
    research_data = await self.conduct_multi_source_research(task_input)
    
    # Store in persistent memory (PostgreSQL)
    await self.store_memory("task_context", research_data)
    
    # Tool discovery and usage (required)
    available_tools = await self.discover_tools()
    
    # Iterative enrichment (required)
    enriched_data = await self.enrich_dataset(research_data)
    
    return {"result": enriched_data, "tools_used": available_tools}
```

### Testing and Validation

#### Comprehensive Testing Requirements
```bash
# Run agent-specific tests
pytest agents/operational/crawler/tests/ -v --cov

# Cross-repository validation
python scripts/validate_cross_repo_alignment.py

# Performance benchmarking
python scripts/benchmark_agent_performance.py --agent-id "operational_crawler"
```

#### Standards Compliance Check
```python
# All agents must pass standards validation
from shared.standards.validator import AgentStandardsValidator

validator = AgentStandardsValidator()
compliance_report = await validator.validate_agent("my_agent")
assert compliance_report.compliance_score >= 0.90
```

## 🔐 Security and Compliance

### Database Security
- **Multi-tenant isolation**: Organization-based data separation
- **Encrypted storage**: AES-256 encryption for sensitive data
- **Audit logging**: Complete activity tracking
- **Access controls**: Role-based permissions

### Agent Security Standards
```python
# REQUIRED: Secure configuration
agent_config = AgentConfig(
    name="secure_agent",
    database_url=os.getenv("DATABASE_URL"),  # Never hardcode
    encryption_key=os.getenv("AGENT_ENCRYPTION_KEY"),
    audit_enabled=True
)

# FORBIDDEN: Insecure patterns
# agent_config.api_key = "sk-1234567890"  # NEVER hardcode secrets
# sqlite_db = "local_memory.db"           # DEPRECATED - use PostgreSQL
```

## 📊 Performance Standards

### Required Performance Metrics
- **Task Completion Rate**: >90%
- **Response Time**: <5 seconds average
- **Accuracy Score**: >93%
- **Memory Efficiency**: <100MB per agent
- **Database Connection**: <2 seconds

### Monitoring and Observability
```python
# Built-in performance tracking
class PerformanceTracker:
    async def track_execution(self, agent_id: str, task_type: str):
        metrics = {
            "completion_time": execution_time,
            "memory_usage": memory_peak,
            "database_queries": query_count,
            "success_rate": success_percentage
        }
        await self.store_metrics(agent_id, metrics)
```

## 🛠️ Migration and Maintenance

### SQLite to PostgreSQL Migration
```bash
# Automated migration tool
python migration/sqlite_to_postgres_migrator.py \
  --postgres-url "$DATABASE_URL" \
  --agents-path "./agents" \
  --dry-run  # Test first

# Execute migration
python migration/sqlite_to_postgres_migrator.py \
  --postgres-url "$DATABASE_URL" \
  --agents-path "./agents"
```

### Cross-Repository Synchronization
```bash
# Validate alignment across repositories
python scripts/validate_cross_repo_alignment.py \
  --workspace /Users/tony/Projects \
  --output alignment_report.json

# Sync schemas if needed
npm run sync:schemas  # In saas-spec-driven-development
```

## 📚 Key Resources

### Essential Files
- **`shared/standards/agent_standards_and_specifications.md`**: Complete agent requirements
- **`shared/templates/enhanced_agent_base_postgres.py`**: PostgreSQL base class
- **`shared/database/prisma_client.py`**: Database client implementation
- **`migration/README.md`**: Migration guide and procedures

### Documentation
- **`agents/*/agents.md`**: Agent-specific documentation
- **`agents/*/README.md`**: Setup and usage instructions
- **`docs/`**: Comprehensive development guides
- **`manus/`**: Research findings and implementation artifacts

## 🔄 Cross-Repository Dependencies

### Required Environment Variables
```bash
# PostgreSQL connection (shared across repositories)
DATABASE_URL="postgresql://user:pass@localhost:5432/saas_ecosystem"

# Agent configuration
AGENT_ENCRYPTION_KEY="your-256-bit-key"
AGENT_REGISTRY_URL="http://localhost:3001"

# Cross-repository coordination
SAAS_ECOSYSTEM_URL="http://localhost:3000"
SPEC_DRIVEN_URL="http://localhost:3002"
```

### Service Dependencies
- **saas-ecosystem-architecture**: Primary database schema and admin interface
- **saas-spec-driven-development**: Specification management and coordination
- **app-agents**: Agent implementation and execution (this repository)

## 🚨 Critical Requirements

### NEVER Do These
- ❌ Use SQLite for new agents (deprecated)
- ❌ Store secrets in code or local files
- ❌ Create agents without comprehensive testing
- ❌ Deploy without cross-repository validation
- ❌ Modify schemas without coordination

### ALWAYS Do These
- ✅ Use PostgreSQL/Prisma for all data storage
- ✅ Inherit from `EnhancedAgentBase` (PostgreSQL version)
- ✅ Follow comprehensive agent standards
- ✅ Run cross-repository validation before deployment
- ✅ Implement all required capabilities (memory, research, tools, learning)

## 🎯 Development Priorities

### Immediate Focus
1. **Standards Compliance**: Ensure all agents meet v2.0.0 requirements
2. **Performance Optimization**: Achieve >95% success rates
3. **Cross-Repository Integration**: Seamless coordination
4. **Documentation Currency**: Automated updates and validation

### Strategic Evolution
1. **Advanced AI Integration**: Multi-provider LLM support
2. **Enhanced Learning**: ML-powered optimization
3. **Ecosystem Expansion**: Additional specialized agents
4. **Enterprise Features**: Advanced security and compliance

---

This repository represents the cutting edge of AI agent development with enterprise-grade architecture, comprehensive standards, and seamless ecosystem integration. All development should prioritize quality, security, and cross-repository coordination.

*Last updated: 2025-01-21 - Automatically maintained*