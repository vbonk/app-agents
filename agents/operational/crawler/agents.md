# Enhanced Crawler Agent

## Agent Metadata
- **Name**: enhanced_crawler_agent
- **Version**: 2.0.0
- **Type**: Research & Analysis
- **Author**: Manus AI
- **License**: MIT
- **Category**: Operational — Data Collection & Research

## Description
The Enhanced Crawler Agent performs respectful web crawling, content extraction, and enrichment. It relies on the shared `EnhancedAgentBase` to provide persistent memory, dataset management, and standardized tooling. The agent is designed to support SaaSArch-aligned research workflows where structured competitive intelligence and product analysis data is required.

## Prompt Assets
- **System Prompt**: [`crawler-system-prompt.md`](crawler-system-prompt.md)
- **Chat Prompt**: [`crawler-chat-prompt.md`](crawler-chat-prompt.md)

## Capabilities
- **Web Crawling**: Fetches HTML from target URLs while applying configurable delays and retries.
- **Content Extraction**: Parses HTML using CSS selectors to capture targeted fields and metadata.
- **Heuristic Analysis**: Scores pages for quality and relevance based on keyword coverage and length.
- **Dataset Enrichment**: Persists crawl output as JSON datasets and records summaries in persistent memory for downstream analysis.
- **Multi-Source Research**: Delegates to the shared research workflow for blended source discovery when required.

## Tooling
- `url_validator` – Validates and normalizes URLs prior to crawling.
- `html_parser` – Extracts structured data from HTML using CSS selectors.
- `content_analyzer` – Produces heuristic quality and relevance scores.
- `data_enricher` – Adds timestamps, provenance, and metadata to extracted records.

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The agent depends on standard HTTP and parsing libraries (`requests`, `beautifulsoup4`, `httpx`, `pandas`, `pyyaml`, `numpy`) that are enumerated in the repository `requirements.txt`.

## Usage
```python
from agents.crawler.src.enhanced_crawler_agent import EnhancedCrawlerAgent
import asyncio

agent = EnhancedCrawlerAgent()

async def run():
    result = await agent.execute_task({
        "type": "crawl",
        "urls": ["https://example.com"],
        "config": {
            "max_pages": 1,
            "selectors": {
                "headline": "h1",
                "lead_paragraph": "p"
            }
        },
        "keywords": ["example", "product"]
    })
    print(result)

asyncio.run(run())
```

## Datasets
- Generated crawl datasets are written to the agent data directory (default `./crawler_data`) with timestamped filenames. Each crawl also stores a five-record snapshot in persistent memory for downstream analysis routines.

## Testing
Dedicated tests are not yet implemented for the crawler agent. When aligning with SaaSArch, add pytest suites that cover URL validation, selector extraction, and analysis scoring logic.

## Notes
- Respect website terms of service and robots.txt when supplying URLs.
- Provide explicit selectors and keyword criteria to improve relevance scoring.
- Combine with the Prompt Researcher Agent for blended research workflows.
