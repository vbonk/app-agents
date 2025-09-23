"""
Enhanced Crawler Agent
Updated to meet the new agent standards and specifications.
"""

import asyncio
import json
import sqlite3
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys
import os

# Add shared templates to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared', 'templates'))

from enhanced_agent_base import EnhancedAgentBase, AgentConfig


class EnhancedCrawlerAgent(EnhancedAgentBase):
    """
    Enhanced Crawler Agent with comprehensive web crawling and analysis capabilities.
    Implements all required standards: multi-source research, persistent memory,
    iterative dataset enrichment, prompt optimization, and tool awareness.
    """
    
    def __init__(self, data_dir: str = "./crawler_data"):
        config = AgentConfig(
            name="enhanced_crawler_agent",
            version="2.0.0",
            description="Comprehensive web crawling and analysis system with enhanced capabilities",
            capabilities=[
                "web_crawling",
                "content_extraction",
                "data_analysis",
                "multi_source_research",
                "dataset_enrichment",
                "prompt_optimization",
                "tool_discovery"
            ],
            data_sources=["web", "apis", "databases", "files", "social_media"]
        )
        super().__init__(config, data_dir)
        
        # Crawler-specific configuration
        self.crawl_delay = 1.0  # Respectful crawling delay
        self.max_retries = 3
        self.timeout = 30
        
        # Initialize crawler-specific tools
        self._init_crawler_tools()
        
        self.logger.info("Enhanced Crawler Agent initialized")
    
    def _init_crawler_tools(self):
        """Initialize crawler-specific tools."""
        crawler_tools = {
            "html_parser": {
                "name": "html_parser",
                "description": "Parse HTML content and extract structured data",
                "input_schema": {"html": "string", "selectors": "object"},
                "output_schema": {"extracted_data": "object"}
            },
            "url_validator": {
                "name": "url_validator",
                "description": "Validate and normalize URLs",
                "input_schema": {"url": "string"},
                "output_schema": {"valid": "boolean", "normalized_url": "string"}
            },
            "content_analyzer": {
                "name": "content_analyzer",
                "description": "Analyze content quality and relevance",
                "input_schema": {"content": "string", "criteria": "object"},
                "output_schema": {"quality_score": "float", "relevance_score": "float"}
            },
            "data_enricher": {
                "name": "data_enricher",
                "description": "Enrich crawled data with additional metadata",
                "input_schema": {"data": "object", "enrichment_sources": "array"},
                "output_schema": {"enriched_data": "object"}
            }
        }
        
        for tool_name, tool_data in crawler_tools.items():
            from enhanced_agent_base import ToolInfo
            tool = ToolInfo(**tool_data)

            handler_map = {
                "html_parser": self._handle_html_parser,
                "url_validator": self._handle_url_validator,
                "content_analyzer": self._handle_content_analyzer,
                "data_enricher": self._handle_data_enricher
            }

            self.register_tool(tool, handler=handler_map.get(tool_name))

    def _handle_url_validator(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validate URLs and return normalised forms."""
        url = (payload.get("url") or "").strip()
        from urllib.parse import urlparse, urlunparse

        parsed = urlparse(url)
        valid = parsed.scheme in {"http", "https"} and bool(parsed.netloc)
        normalized = urlunparse(parsed) if valid else url

        return {
            "result": {
                "valid": valid,
                "normalized_url": normalized
            }
        }

    def _handle_html_parser(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extract fields from HTML using CSS selectors."""
        html = payload.get("html", "")
        selectors = payload.get("selectors", {}) or {}

        soup = BeautifulSoup(html, "html.parser")
        extracted: Dict[str, Any] = {}

        for key, selector in selectors.items():
            if not selector:
                continue
            nodes = soup.select(selector)
            if not nodes:
                extracted[key] = None
            else:
                text_values = [node.get_text(strip=True) for node in nodes]
                extracted[key] = text_values if len(text_values) > 1 else text_values[0]

        return {
            "result": {
                "extracted_data": extracted
            }
        }

    def _handle_content_analyzer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Provide heuristic quality and relevance scores for content."""
        content = payload.get("content", "")
        criteria = payload.get("criteria", {}) or {}

        min_length = max(criteria.get("min_length", 200), 1)
        keywords = [kw.lower() for kw in criteria.get("relevance_keywords", []) if isinstance(kw, str)]

        length_score = min(len(content) / min_length, 1.0)

        if keywords:
            lowered = content.lower()
            matches = sum(1 for kw in keywords if kw in lowered)
            relevance_score = matches / len(keywords)
        else:
            relevance_score = 0.5

        quality_score = round((0.6 * length_score) + (0.4 * relevance_score), 2)

        return {
            "result": {
                "quality_score": round(quality_score, 2),
                "relevance_score": round(relevance_score, 2)
            }
        }

    def _handle_data_enricher(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Attach metadata to crawled results."""
        data = payload.get("data", {})
        sources = payload.get("enrichment_sources", []) or []

        enriched = {
            "data": data,
            "enriched_at": datetime.now().isoformat(),
            "sources": sources
        }

        return {
            "result": {
                "enriched_data": enriched
            }
        }
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a crawler task."""
        task_type = task.get("type", "crawl")
        
        start_time = datetime.now()
        
        try:
            if task_type == "crawl":
                result = await self._execute_crawl_task(task)
            elif task_type == "analyze":
                result = await self._execute_analysis_task(task)
            elif task_type == "enrich":
                result = await self._execute_enrichment_task(task)
            elif task_type == "research":
                result = self.conduct_multi_source_research(
                    query=task.get("query", ""),
                    sources=task.get("sources")
                )
            else:
                result = {
                    "error": f"Unknown task type: {task_type}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Record performance metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self.record_metric("response_times", execution_time)
            
            if "error" not in result:
                self.record_metric("task_completion_rate", 1.0)
            else:
                self.record_metric("task_completion_rate", 0.0)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            self.record_metric("task_completion_rate", 0.0)
            return {
                "error": str(e),
                "task_type": task_type,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _execute_crawl_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a web crawling task."""
        urls = task.get("urls", [])
        if isinstance(urls, str):
            urls = [urls]
        
        crawl_config = task.get("config", {})
        max_pages = crawl_config.get("max_pages", 10)
        extract_selectors = crawl_config.get("selectors", {})
        
        results = {
            "task_type": "crawl",
            "urls_processed": 0,
            "pages_crawled": 0,
            "data_extracted": [],
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for url in urls[:max_pages]:
            try:
                # Validate URL
                url_validation = self.use_tool("url_validator", {"url": url})
                if not url_validation.get("result", {}).get("valid", False):
                    results["errors"].append(f"Invalid URL: {url}")
                    continue
                
                # Crawl the page
                page_data = await self._crawl_page(url, extract_selectors)
                
                if page_data:
                    # Analyze content quality
                    quality_analysis = self.use_tool("content_analyzer", {
                        "content": page_data.get("content", ""),
                        "criteria": {"min_length": 100, "relevance_keywords": task.get("keywords", [])}
                    })
                    
                    page_data["quality_score"] = quality_analysis.get("result", {}).get("quality_score", 0.5)
                    page_data["relevance_score"] = quality_analysis.get("result", {}).get("relevance_score", 0.5)
                    
                    results["data_extracted"].append(page_data)
                    results["pages_crawled"] += 1
                
                results["urls_processed"] += 1
                
                # Respectful crawling delay
                await asyncio.sleep(self.crawl_delay)
                
            except Exception as e:
                self.logger.error(f"Error crawling {url}: {e}")
                results["errors"].append(f"Error crawling {url}: {str(e)}")
        
        # Store crawl results in memory
        memory_snapshot = results["data_extracted"][:5]
        self.store_memory(
            content=f"Crawl task completed: {results['pages_crawled']} pages",
            metadata={
                "type": "crawl_results",
                "urls": urls,
                "pages_crawled": results["pages_crawled"],
                "timestamp": results["timestamp"],
                "data": memory_snapshot
            }
        )

        # Save dataset
        if results["data_extracted"]:
            dataset_path = self.data_dir / f"crawl_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.save_dataset(results["data_extracted"], str(dataset_path), "json")
            results["dataset_path"] = str(dataset_path)
        else:
            results["dataset_path"] = None

        return results
    
    async def _crawl_page(self, url: str, selectors: Dict[str, str] = None) -> Optional[Dict[str, Any]]:
        """Crawl a single page and extract data."""
        try:
            # Make HTTP request
            response = requests.get(url, timeout=self.timeout, headers={
                'User-Agent': 'Enhanced-Crawler-Agent/2.0.0 (Research Purpose)'
            })
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic data
            page_data = {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "content": soup.get_text(strip=True),
                "links": [a.get('href') for a in soup.find_all('a', href=True)],
                "images": [img.get('src') for img in soup.find_all('img', src=True)],
                "crawled_at": datetime.now().isoformat(),
                "status_code": response.status_code,
                "content_length": len(response.content)
            }
            
            # Extract custom selectors if provided
            if selectors:
                extracted_data = self.use_tool("html_parser", {
                    "html": str(soup),
                    "selectors": selectors
                })
                page_data["custom_extractions"] = extracted_data.get("result", {})
            
            return page_data
            
        except Exception as e:
            self.logger.error(f"Error crawling page {url}: {e}")
            return None
    
    async def _execute_analysis_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a data analysis task."""
        data_source = task.get("data_source")
        analysis_type = task.get("analysis_type", "basic")
        
        results = {
            "task_type": "analysis",
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Load data
            if data_source:
                if isinstance(data_source, str) and Path(data_source).exists():
                    data = self.load_dataset(data_source)
                else:
                    data = data_source
            else:
                # Use recent crawl data from memory
                recent_memories = self.retrieve_memory("crawl_results", limit=1)
                if recent_memories:
                    data = recent_memories[0].metadata.get("data", [])
                else:
                    raise ValueError("No data source provided and no recent crawl data found")
            
            # Perform analysis based on type
            if analysis_type == "basic":
                results["analysis"] = self._perform_basic_analysis(data)
            elif analysis_type == "content":
                results["analysis"] = self._perform_content_analysis(data)
            elif analysis_type == "link":
                results["analysis"] = self._perform_link_analysis(data)
            else:
                results["analysis"] = {"error": f"Unknown analysis type: {analysis_type}"}
            
            # Store analysis results
            self.store_memory(
                content=f"Analysis completed: {analysis_type}",
                metadata={
                    "type": "analysis_results",
                    "analysis_type": analysis_type,
                    "results": results["analysis"]
                }
            )
            
            return results
            
        except Exception as e:
            self.logger.error(f"Analysis task failed: {e}")
            results["error"] = str(e)
            return results
    
    def _perform_basic_analysis(self, data: Any) -> Dict[str, Any]:
        """Perform basic statistical analysis of crawled data."""
        if isinstance(data, list):
            return {
                "total_items": len(data),
                "item_types": list(set(type(item).__name__ for item in data)),
                "sample_item": data[0] if data else None
            }
        elif isinstance(data, dict):
            return {
                "total_keys": len(data.keys()),
                "keys": list(data.keys()),
                "data_types": {k: type(v).__name__ for k, v in data.items()}
            }
        else:
            return {
                "data_type": type(data).__name__,
                "data_length": len(str(data)) if hasattr(data, '__len__') else 0
            }
    
    def _perform_content_analysis(self, data: Any) -> Dict[str, Any]:
        """Perform content analysis of crawled data."""
        if not isinstance(data, list):
            data = [data]
        
        total_content_length = 0
        total_links = 0
        total_images = 0
        domains = set()
        
        for item in data:
            if isinstance(item, dict):
                content = item.get("content", "")
                total_content_length += len(content)
                
                links = item.get("links", [])
                total_links += len(links)
                
                images = item.get("images", [])
                total_images += len(images)
                
                url = item.get("url", "")
                if url:
                    try:
                        from urllib.parse import urlparse
                        domain = urlparse(url).netloc
                        domains.add(domain)
                    except:
                        pass
        
        return {
            "total_content_length": total_content_length,
            "average_content_length": total_content_length / len(data) if data else 0,
            "total_links": total_links,
            "total_images": total_images,
            "unique_domains": len(domains),
            "domains": list(domains)
        }
    
    def _perform_link_analysis(self, data: Any) -> Dict[str, Any]:
        """Perform link analysis of crawled data."""
        if not isinstance(data, list):
            data = [data]
        
        all_links = []
        internal_links = []
        external_links = []
        
        for item in data:
            if isinstance(item, dict):
                base_url = item.get("url", "")
                links = item.get("links", [])
                
                for link in links:
                    if link:
                        all_links.append(link)
                        
                        # Classify as internal or external
                        if link.startswith('http'):
                            if base_url and base_url in link:
                                internal_links.append(link)
                            else:
                                external_links.append(link)
                        else:
                            internal_links.append(link)
        
        return {
            "total_links": len(all_links),
            "internal_links": len(internal_links),
            "external_links": len(external_links),
            "unique_links": len(set(all_links)),
            "most_common_domains": self._get_most_common_domains(external_links)
        }
    
    def _get_most_common_domains(self, links: List[str]) -> Dict[str, int]:
        """Get most common domains from a list of links."""
        domain_counts = {}
        
        for link in links:
            try:
                from urllib.parse import urlparse
                domain = urlparse(link).netloc
                if domain:
                    domain_counts[domain] = domain_counts.get(domain, 0) + 1
            except:
                continue
        
        # Return top 10 domains
        sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_domains[:10])
    
    async def _execute_enrichment_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a dataset enrichment task."""
        dataset_id = task.get("dataset_id")
        enrichment_sources = task.get("sources", ["metadata", "content_analysis"])
        
        results = {
            "task_type": "enrichment",
            "dataset_id": dataset_id,
            "enrichment_sources": enrichment_sources,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Load existing dataset
            if dataset_id and Path(dataset_id).exists():
                existing_data = self.load_dataset(dataset_id)
            else:
                # Use recent data from memory
                recent_memories = self.retrieve_memory("crawl_results", limit=1)
                if recent_memories:
                    existing_data = recent_memories[0].metadata.get("data", [])
                else:
                    raise ValueError("No dataset found for enrichment")
            
            # Perform enrichment
            enriched_data = []
            
            if isinstance(existing_data, list):
                for item in existing_data:
                    enriched_item = await self._enrich_item(item, enrichment_sources)
                    enriched_data.append(enriched_item)
            else:
                enriched_data = await self._enrich_item(existing_data, enrichment_sources)
            
            # Save enriched dataset
            enriched_path = self.data_dir / f"enriched_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            self.save_dataset(enriched_data, str(enriched_path), "json")
            
            results["enriched_dataset_path"] = str(enriched_path)
            results["items_enriched"] = len(enriched_data) if isinstance(enriched_data, list) else 1
            
            # Store enrichment results
            self.store_memory(
                content=f"Dataset enrichment completed",
                metadata={
                    "type": "enrichment_results",
                    "dataset_id": dataset_id,
                    "items_enriched": results["items_enriched"]
                }
            )
            
            return results
            
        except Exception as e:
            self.logger.error(f"Enrichment task failed: {e}")
            results["error"] = str(e)
            return results
    
    async def _enrich_item(self, item: Dict[str, Any], sources: List[str]) -> Dict[str, Any]:
        """Enrich a single data item."""
        enriched_item = item.copy()
        
        for source in sources:
            try:
                if source == "metadata":
                    # Add metadata enrichment
                    enriched_item["enrichment_metadata"] = {
                        "enriched_at": datetime.now().isoformat(),
                        "enrichment_version": "2.0.0",
                        "original_keys": list(item.keys())
                    }
                
                elif source == "content_analysis":
                    # Perform content analysis
                    content = item.get("content", "")
                    if content:
                        analysis = self.use_tool("content_analyzer", {
                            "content": content,
                            "criteria": {"sentiment": True, "keywords": True}
                        })
                        enriched_item["content_analysis"] = analysis.get("result", {})
                
                elif source == "external_data":
                    # Mock external data enrichment
                    enriched_item["external_data"] = {
                        "source": "external_api",
                        "data": "Mock external data",
                        "confidence": 0.8
                    }
                
            except Exception as e:
                self.logger.error(f"Error enriching with {source}: {e}")
                enriched_item[f"{source}_error"] = str(e)
        
        return enriched_item
    
    def get_capabilities(self) -> List[str]:
        """Return agent capabilities."""
        return self.config.capabilities
    
    def optimize_crawl_strategy(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize crawling strategy based on performance data."""
        current_strategy = {
            "crawl_delay": self.crawl_delay,
            "max_retries": self.max_retries,
            "timeout": self.timeout
        }
        
        optimized_strategy = current_strategy.copy()
        
        # Optimize based on performance metrics
        avg_response_time = performance_data.get("avg_response_time", 0)
        error_rate = performance_data.get("error_rate", 0)
        
        if avg_response_time > 10:
            # Increase timeout for slow responses
            optimized_strategy["timeout"] = min(60, self.timeout * 1.5)
        
        if error_rate > 0.2:
            # Increase delay and retries for high error rates
            optimized_strategy["crawl_delay"] = min(5.0, self.crawl_delay * 1.5)
            optimized_strategy["max_retries"] = min(5, self.max_retries + 1)
        
        # Apply optimizations
        self.crawl_delay = optimized_strategy["crawl_delay"]
        self.max_retries = optimized_strategy["max_retries"]
        self.timeout = optimized_strategy["timeout"]
        
        # Store optimization in learning patterns
        conn = sqlite3.connect(self.memory_db_path)
        cursor = conn.cursor()
        
        pattern_id = f"crawl_opt_{datetime.now().isoformat()}"
        cursor.execute('''
            INSERT INTO learning_patterns (id, pattern_type, pattern_data, confidence, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            pattern_id,
            "crawl_optimization",
            json.dumps({
                "original": current_strategy,
                "optimized": optimized_strategy,
                "performance": performance_data
            }),
            0.8,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        self.logger.info("Optimized crawl strategy based on performance data")
        return optimized_strategy


# Example usage and testing
if __name__ == "__main__":
    async def test_enhanced_crawler():
        """Test the enhanced crawler agent."""
        agent = EnhancedCrawlerAgent()
        
        # Test health check
        health = agent.health_check()
        print("Health Check:", json.dumps(health, indent=2))
        
        # Test crawling task
        crawl_task = {
            "type": "crawl",
            "urls": ["https://httpbin.org/html"],
            "config": {
                "max_pages": 1,
                "selectors": {
                    "title": "title",
                    "headings": "h1, h2, h3"
                }
            }
        }
        
        print("\nExecuting crawl task...")
        result = await agent.execute_task(crawl_task)
        print("Crawl Result:", json.dumps(result, indent=2))
        
        # Test analysis task
        analysis_task = {
            "type": "analysis",
            "analysis_type": "basic"
        }
        
        print("\nExecuting analysis task...")
        analysis_result = await agent.execute_task(analysis_task)
        print("Analysis Result:", json.dumps(analysis_result, indent=2))
        
        # Test performance summary
        performance = agent.get_performance_summary()
        print("\nPerformance Summary:", json.dumps(performance, indent=2))
    
    # Run the test
    asyncio.run(test_enhanced_crawler())
