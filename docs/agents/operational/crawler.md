# Crawler Agent

## Overview

The Crawler Agent is a specialized AI agent designed to systematically crawl websites and extract detailed information about software applications. It uses a comprehensive research and analysis framework to build a structured knowledge base that can be used to train other AI agents and support development workflows.

## Features

### Intelligent Web Crawling

- Systematic website exploration and data extraction
- Configurable crawling depth and breadth controls
- Respect for robots.txt and rate limiting

### Application Analysis

- Software application feature extraction
- Technology stack identification
- User interface and functionality analysis

### Knowledge Base Construction

- Structured data storage and organization
- Cross-referencing and relationship mapping
- Training data generation for other agents

## Usage

### Basic Crawling

```bash
# Crawl a single website
python3 agents/operational/crawler/src/main.py --url "https://example.com" --depth 2

# Crawl multiple sites from a list
python3 agents/operational/crawler/src/main.py --urls-file sites.txt --output results.json
```

### Application Analysis

```python
from crawler_agent import CrawlerAgent

crawler = CrawlerAgent()
analysis = crawler.analyze_application(
    url="https://github.com/microsoft/vscode",
    analysis_type="feature_extraction",
    output_format="structured"
)

# Results include features, technologies, UI patterns, etc.
print(analysis.features)
print(analysis.technologies)
```

## Configuration

### Crawling Parameters

```json
{
  "crawler": {
    "max_depth": 3,
    "max_pages": 1000,
    "delay_between_requests": 1.0,
    "respect_robots_txt": true,
    "user_agent": "CrawlerAgent/1.0 (Research)",
    "timeout": 30
  },
  "analysis": {
    "feature_detection": true,
    "technology_identification": true,
    "ui_pattern_analysis": true,
    "content_categorization": true
  },
  "storage": {
    "database_url": "postgresql://localhost/crawler_db",
    "output_directory": "./data/crawler_results",
    "cache_enabled": true
  }
}
```

### Analysis Modules

- **Feature Extractor**: Identifies application features and capabilities
- **Technology Detector**: Recognizes frameworks, libraries, and platforms
- **UI Analyzer**: Examines user interface patterns and design
- **Content Classifier**: Categorizes content types and purposes

## Examples

### Website Analysis

```python
analysis_result = crawler.analyze_website(
    url="https://notion.so",
    modules=["features", "technologies", "ui_patterns"],
    save_to_db=True
)

# Access results
print(f"Features found: {len(analysis_result.features)}")
print(f"Technologies: {analysis_result.technologies}")
print(f"UI Patterns: {analysis_result.ui_patterns}")
```

### Batch Processing

```bash
# Process multiple applications
python3 agents/operational/crawler/src/batch_processor.py \
  --input applications.csv \
  --output analysis_results/ \
  --parallel 4 \
  --progress-bar
```

### Knowledge Base Integration

```python
# Store analysis results in knowledge base
kb = KnowledgeBase()
kb.store_analysis(analysis_result)

# Query for similar applications
similar_apps = kb.find_similar_applications(
    features=["task_management", "collaboration"],
    technologies=["react", "nodejs"]
)
```

## Technical Details

### Architecture

- **Crawler Engine**: Multi-threaded web crawling with asyncio
- **Analysis Pipeline**: Modular analysis components
- **Data Storage**: PostgreSQL with pgvector for similarity search
- **Caching System**: Redis-based caching for performance

### Dependencies

- **Web Crawling**: requests, aiohttp, beautifulsoup4, selenium
- **Analysis**: spacy, nltk, scikit-learn for NLP tasks
- **Storage**: psycopg2, redis, sqlalchemy
- **Utilities**: pandas, numpy, tqdm for data processing

### Data Schema

```sql
-- Application analysis results
CREATE TABLE application_analysis (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    crawled_at TIMESTAMP DEFAULT NOW(),
    features JSONB,
    technologies JSONB,
    ui_patterns JSONB,
    content_categories JSONB,
    metadata JSONB
);

-- Technology detection results
CREATE TABLE technology_detection (
    id SERIAL PRIMARY KEY,
    application_id INTEGER REFERENCES application_analysis(id),
    technology_name TEXT,
    version TEXT,
    confidence FLOAT,
    detection_method TEXT
);
```

## Integration

### SaaS Ecosystem

- **Database Storage**: Analysis results stored in PostgreSQL
- **Admin Interface**: Visualization of crawled data and insights
- **API Access**: RESTful endpoints for analysis results

### Cross-Repository Coordination

- Provides training data to other agents
- Contributes to the knowledge base used by research agents
- Supports specification-driven development processes

## Best Practices

### Crawling Ethics

1. Always respect robots.txt files
2. Implement appropriate rate limiting
3. Use identifiable user agents
4. Honor no-index directives

### Data Quality

- Implement data validation and cleaning
- Use multiple analysis methods for verification
- Maintain data provenance and timestamps
- Regular quality audits and updates

### Performance Optimization

- Use caching to avoid redundant crawling
- Implement parallel processing for large jobs
- Monitor resource usage and implement limits
- Optimize database queries and indexing

## Troubleshooting

### Common Issues

**Crawling Blocks**: Check robots.txt and implement proper delays.

**Analysis Failures**: Verify website structure and update selectors.

**Database Connection Issues**: Check PostgreSQL configuration and credentials.

**Memory Issues**: Implement streaming for large datasets.

### Debug Mode

```bash
# Enable debug logging
export CRAWLER_DEBUG=true
export LOG_LEVEL=DEBUG

# Run with verbose output
python3 agents/operational/crawler/src/main.py --verbose --debug
```

## Contributing

### Code Contributions

- Add comprehensive tests for new analysis modules
- Document any new dependencies and their purposes
- Ensure database migrations are included
- Update configuration schemas for new options

### Analysis Improvements

- Validate new analysis modules against known datasets
- Provide performance benchmarks and accuracy metrics
- Document analysis methodology and limitations
- Include example outputs and edge cases

## Future Enhancements

- **Advanced ML Analysis**: Use computer vision for UI analysis
- **Real-time Monitoring**: Continuous website monitoring capabilities
- **API Integration**: Direct integration with application APIs
- **Collaborative Analysis**: Multi-agent analysis coordination
