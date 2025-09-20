# Prompt-Researcher Agent Specification

## Agent Metadata

- **Name**: Prompt-Researcher Agent
- **Version**: 1.0.0
- **Type**: Research & Analysis
- **Category**: Data Collection and Intelligence
- **Created**: 2025-01-20
- **Updated**: 2025-01-20
- **Status**: Production Ready

## Description

The Prompt-Researcher Agent is a sophisticated research automation system that conducts comprehensive multi-source research with advanced learning capabilities. It combines intelligent data collection, persistent memory, and iterative improvement to provide high-quality research datasets and insights.

## Capabilities

### Core Functions

1. **Multi-Source Research Orchestration**
   - Simultaneous search across GitHub, web, Reddit, and extensible sources
   - Intelligent source prioritization based on query type and learned patterns
   - Rate-limited and respectful API usage with error handling

2. **Advanced Quality Assessment**
   - Multi-dimensional scoring: relevance, authority, recency, engagement, completeness
   - Configurable quality thresholds and filtering
   - Cross-source validation and duplicate detection

3. **Persistent Memory and Learning**
   - SQLite-based knowledge graph with entity relationships
   - Pattern recognition for search strategy optimization
   - Performance analytics and source effectiveness tracking

4. **Iterative Research Enrichment**
   - Add new sources and query variations to existing projects
   - Continuous dataset improvement and expansion
   - Historical research session tracking and analysis

5. **Comprehensive Dataset Generation**
   - Multi-format output: Excel, JSON, CSV
   - Structured metadata and methodology documentation
   - Automated insights and recommendations generation

### Specialized Features

- **Learning Engine**: Improves search strategies based on historical performance
- **Knowledge Graph**: Maintains relationships between topics, sources, and results
- **Research Methodology Framework**: Configurable approaches for different research types
- **Quality Scoring System**: Advanced relevance and authority assessment
- **Memory Persistence**: Maintains state across agent restarts and sessions

## Input Schema

### Primary Research Request

```json
{
  "query": "string (required) - The research query or topic",
  "description": "string (optional) - Detailed description of research objectives",
  "research_type": "string (optional) - Type: technology_analysis, market_research, academic_research, product_research",
  "sources": "array[string] (optional) - Specific sources to search, defaults to optimized selection",
  "use_learning": "boolean (optional) - Whether to apply learned optimization patterns, default: true",
  "limit_per_source": "integer (optional) - Maximum results per source, default: 15",
  "quality_threshold": "float (optional) - Minimum quality score for results, default: 0.3"
}
```

### Research Enrichment Request

```json
{
  "project_id": "string (required) - ID of existing research project",
  "additional_sources": "array[string] (optional) - New sources to search",
  "new_query_variations": "array[string] (optional) - Query variations to explore",
  "quality_threshold": "float (optional) - Quality threshold for new results"
}
```

### Insights Request

```json
{
  "project_id": "string (optional) - Specific project to analyze, null for all projects",
  "include_learning_patterns": "boolean (optional) - Include learning insights, default: true",
  "include_recommendations": "boolean (optional) - Include actionable recommendations, default: true"
}
```

## Output Schema

### Research Results

```json
{
  "project_id": "string - Unique project identifier",
  "session_id": "string - Research session identifier",
  "query": "string - Original research query",
  "research_type": "string - Type of research conducted",
  "methodology_used": "string - Research methodology applied",
  "sources_searched": "array[string] - Sources that were searched",
  "total_results": "integer - Total results found",
  "high_quality_results": "integer - Results above quality threshold",
  "quality_threshold": "float - Quality threshold applied",
  "dataset_path": "string - Path to generated dataset file",
  "learning_applied": "boolean - Whether learning optimizations were used",
  "recommendations_confidence": "float - Confidence in learning recommendations (0-1)",
  "results_summary": {
    "total": "integer - Total results count",
    "sources": "object - Results count by source",
    "avg_quality": "float - Average quality score",
    "quality_range": {
      "min": "float - Minimum quality score",
      "max": "float - Maximum quality score"
    },
    "top_results": "array[object] - Top 5 results by quality"
  },
  "insights": "array[object] - Generated insights and findings",
  "analysis": "object - Dimensional analysis results"
}
```

### Enrichment Results

```json
{
  "project_id": "string - Project identifier",
  "enrichment_session_id": "string - Enrichment session identifier",
  "original_results_count": "integer - Count before enrichment",
  "new_results_count": "integer - New results added",
  "total_results_count": "integer - Total after enrichment",
  "quality_threshold": "float - Quality threshold applied",
  "updated_dataset_path": "string - Path to updated dataset",
  "new_results_summary": "object - Summary of new results",
  "enrichment_insights": "array[object] - Insights from enrichment"
}
```

### Research Insights

```json
{
  "memory_insights": {
    "total_projects": "integer - Total projects in memory",
    "total_results": "integer - Total results collected",
    "avg_project_quality": "float - Average quality across projects",
    "most_successful_sources": "array[object] - Top performing sources",
    "research_trends": "array[object] - Research activity trends",
    "learning_insights_count": "integer - Number of learning insights",
    "knowledge_entities": "integer - Entities in knowledge graph"
  },
  "project_specific": "object (optional) - Project-specific analysis",
  "learning_patterns": {
    "most_effective_sources": "object - Source effectiveness rankings",
    "confidence_level": "float - Learning system confidence",
    "similar_topics_found": "integer - Related topics discovered"
  },
  "recommendations": "array[string] - Actionable recommendations"
}
```

## Error Handling

### Common Error Responses

```json
{
  "error": "string - Error type",
  "message": "string - Human-readable error message",
  "details": "object (optional) - Additional error context",
  "suggestions": "array[string] (optional) - Suggested remediation steps"
}
```

### Error Types

- `invalid_query`: Query is empty or malformed
- `project_not_found`: Specified project ID does not exist
- `source_unavailable`: Requested source is not available or configured
- `quality_threshold_invalid`: Quality threshold outside valid range (0-1)
- `memory_error`: Database or memory system error
- `rate_limit_exceeded`: API rate limits exceeded for sources
- `configuration_error`: Invalid research methodology or configuration

## Performance Characteristics

### Latency

- **Single Source Search**: 2-3 seconds average
- **Multi-Source Research**: 5-15 seconds (depending on source count)
- **Research Enrichment**: 3-10 seconds (depending on new sources)
- **Insights Generation**: <1 second for existing projects

### Throughput

- **Concurrent Searches**: Up to 10 simultaneous source searches
- **Results Processing**: 1000+ results per minute
- **Memory Operations**: 100+ database operations per second
- **Learning Updates**: Real-time pattern recognition and storage

### Resource Usage

- **Memory**: 50-200MB depending on dataset size
- **Storage**: ~1MB per 100 research results
- **CPU**: Moderate during active research, minimal during idle
- **Network**: Respectful API usage with built-in rate limiting

## Dependencies

### Required Python Packages

```
pandas>=1.5.0
openpyxl>=3.0.0
requests>=2.28.0
pyyaml>=6.0
numpy>=1.21.0
sqlite3 (built-in)
asyncio (built-in)
```

### External APIs

- **GitHub API**: Repository search and metadata (optional API key for higher limits)
- **Web Search**: Generic web search capabilities
- **Reddit API**: Subreddit and post analysis (optional API credentials)

### System Requirements

- **Python**: 3.8+ (tested with 3.11)
- **Operating System**: Cross-platform (Linux, macOS, Windows)
- **Disk Space**: 100MB+ for datasets and memory storage
- **Network**: Internet connection required for source searches

## Configuration

### Research Methodologies

The agent supports configurable research methodologies stored in YAML format:

```yaml
name: "Technology Analysis"
description: "Comprehensive analysis of technology frameworks and tools"
research_type: "technology_analysis"
sources: ["github", "web", "reddit"]
scoring_weights:
  relevance: 0.30
  authority: 0.25
  recency: 0.20
  engagement: 0.15
  completeness: 0.10
quality_thresholds:
  minimum_score: 0.3
  high_quality_score: 0.7
enrichment_strategies: ["cross_reference_validation"]
analysis_dimensions: ["popularity", "recency", "authority"]
```

### Source Adapters

Extensible adapter system for adding new research sources:

```python
class CustomSourceAdapter(BaseSourceAdapter):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def search(self, query: str, limit: int) -> List[SearchResult]:
        # Implementation for custom source
        pass
    
    def get_source_name(self) -> str:
        return "custom_source"
```

## Security Considerations

### Data Privacy

- **Local Storage**: All data stored locally in SQLite database
- **No External Transmission**: Research data not transmitted to external services
- **API Key Management**: Secure storage of optional API credentials
- **Content Filtering**: Configurable content filtering and sanitization

### Rate Limiting

- **Respectful Usage**: Built-in rate limiting for all external APIs
- **Exponential Backoff**: Automatic retry with increasing delays
- **Error Handling**: Graceful degradation when sources are unavailable
- **Usage Monitoring**: Tracking of API usage and limits

### Access Control

- **File System**: Respects local file system permissions
- **Database**: SQLite database with appropriate file permissions
- **Configuration**: Secure storage of sensitive configuration data
- **Logging**: Configurable logging levels with sensitive data filtering

## Integration Patterns

### Standalone Usage

```python
from enhanced_prompt_researcher import EnhancedPromptResearcher

researcher = EnhancedPromptResearcher("./data", "./config")
results = await researcher.conduct_enhanced_research(
    query="AI frameworks comparison",
    research_type="technology_analysis"
)
```

### Tool Integration

```python
class ResearchTool:
    def __init__(self):
        self.researcher = EnhancedPromptResearcher()
    
    async def research(self, query: str, **kwargs) -> Dict[str, Any]:
        return await self.researcher.conduct_enhanced_research(query, **kwargs)
    
    async def enrich(self, project_id: str, **kwargs) -> Dict[str, Any]:
        return await self.researcher.enrich_existing_research(project_id, **kwargs)
```

### API Service

```python
from fastapi import FastAPI
from enhanced_prompt_researcher import EnhancedPromptResearcher

app = FastAPI()
researcher = EnhancedPromptResearcher()

@app.post("/research")
async def conduct_research(request: ResearchRequest):
    return await researcher.conduct_enhanced_research(**request.dict())

@app.post("/enrich/{project_id}")
async def enrich_research(project_id: str, request: EnrichmentRequest):
    return await researcher.enrich_existing_research(project_id, **request.dict())
```

## Testing

### Unit Tests

```bash
# Run basic functionality tests
python -m pytest tests/test_prompt_researcher.py

# Run memory system tests
python -m pytest tests/test_memory_system.py

# Run integration tests
python -m pytest tests/test_integration.py
```

### Example Research

```bash
# Run comprehensive AI frameworks research example
python examples/test_ai_frameworks_research.py
```

### Performance Tests

```bash
# Run performance benchmarks
python tests/test_performance.py

# Run memory usage tests
python tests/test_memory_usage.py
```

## Monitoring and Observability

### Logging

The agent provides comprehensive logging at multiple levels:

- **INFO**: Research progress, results summary, learning updates
- **DEBUG**: Detailed search operations, scoring calculations, memory operations
- **WARNING**: Rate limiting, quality threshold issues, source unavailability
- **ERROR**: API failures, database errors, configuration issues

### Metrics

Key metrics tracked automatically:

- **Research Success Rate**: Percentage of successful research operations
- **Source Performance**: Response time and quality metrics per source
- **Learning Effectiveness**: Improvement in recommendations over time
- **Quality Distribution**: Distribution of result quality scores
- **Memory Growth**: Database size and entity count trends

### Health Checks

```python
# Check agent health and configuration
health_status = researcher.get_health_status()
print(f"Status: {health_status['status']}")
print(f"Memory: {health_status['memory_usage']}")
print(f"Sources: {health_status['available_sources']}")
```

## Versioning and Compatibility

### Version History

- **1.0.0**: Initial release with core research and learning capabilities
- **Future**: Planned enhancements for real-time monitoring and advanced NLP

### Backward Compatibility

- **Database Schema**: Automatic migration for schema updates
- **Configuration**: Backward-compatible configuration format
- **API**: Semantic versioning for breaking changes
- **Data Formats**: Maintained compatibility for existing datasets

### Migration Support

```python
# Migrate from previous versions
from prompt_researcher.migration import migrate_data
migrate_data(old_version="0.9.0", new_version="1.0.0", data_dir="./data")
```

## Support and Documentation

### Documentation

- **README.md**: Comprehensive usage guide and examples
- **API Documentation**: Detailed function and class documentation
- **Configuration Guide**: Research methodology and source configuration
- **Integration Examples**: Sample code for common integration patterns

### Community

- **Repository**: [vbonk/app-agents](https://github.com/vbonk/app-agents)
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and community support
- **Contributing**: Contribution guidelines in repository

### Maintenance

- **Regular Updates**: Ongoing maintenance and feature development
- **Security Patches**: Prompt security updates and vulnerability fixes
- **Performance Optimization**: Continuous performance monitoring and improvement
- **Community Feedback**: Active incorporation of user feedback and suggestions
