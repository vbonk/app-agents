#!/usr/bin/env python3
"""
Prompt-Researcher Agent: Advanced Multi-Source Research System

This agent conducts comprehensive research across multiple platforms,
maintains persistent memory, and iteratively enriches datasets.
"""

import asyncio
import json
import sqlite3
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import pandas as pd
import httpx
from urllib.parse import quote_plus
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Represents a single search result from any source."""
    title: str
    url: str
    content: str
    source: str
    timestamp: datetime
    metadata: Dict[str, Any]
    relevance_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

@dataclass
class ResearchProject:
    """Represents a research project with all its data."""
    project_id: str
    query: str
    description: str
    sources: List[str]
    status: str
    created_at: datetime
    updated_at: datetime
    results_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

class SearchAdapter(ABC):
    """Abstract base class for all search adapters."""
    
    @abstractmethod
    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Perform search and return results."""
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of this search source."""
        pass

class GitHubSearchAdapter(SearchAdapter):
    """Search adapter for GitHub repositories."""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token
        self.base_url = "https://api.github.com/search/repositories"
    
    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search GitHub repositories."""
        headers = {}
        if self.api_token:
            headers['Authorization'] = f'token {self.api_token}'
        
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': min(limit, 100)
        }
        
        timeout = httpx.Timeout(10.0, connect=5.0)

        try:
            async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
            
            results = []
            for item in data.get('items', []):
                result = SearchResult(
                    title=item['full_name'],
                    url=item['html_url'],
                    content=item.get('description', ''),
                    source='github',
                    timestamp=datetime.now(),
                    metadata={
                        'stars': item['stargazers_count'],
                        'forks': item['forks_count'],
                        'language': item.get('language'),
                        'updated_at': item['updated_at'],
                        'topics': item.get('topics', [])
                    }
                )
                results.append(result)
            
            return results
        except (httpx.HTTPError, ValueError) as e:
            logger.error(f"GitHub search failed: {e}")
            return []
    
    def get_source_name(self) -> str:
        return "github"

class WebSearchAdapter(SearchAdapter):
    """Search adapter for general web search."""
    
    def __init__(self, api_key: Optional[str] = None, search_engine: str = "duckduckgo"):
        self.api_key = api_key
        self.search_engine = search_engine
    
    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Perform web search using DuckDuckGo (no API key required)."""
        try:
            # Using DuckDuckGo instant answer API (limited but free)
            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
            timeout = httpx.Timeout(10.0, connect=5.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
            
            results = []
            
            # Add abstract if available
            if data.get('Abstract'):
                result = SearchResult(
                    title=data.get('Heading', query),
                    url=data.get('AbstractURL', ''),
                    content=data['Abstract'],
                    source='web',
                    timestamp=datetime.now(),
                    metadata={
                        'source_name': data.get('AbstractSource', 'DuckDuckGo'),
                        'type': 'abstract'
                    }
                )
                results.append(result)
            
            # Add related topics
            for topic in data.get('RelatedTopics', [])[:limit-1]:
                if isinstance(topic, dict) and 'Text' in topic:
                    result = SearchResult(
                        title=topic.get('Text', '')[:100] + '...',
                        url=topic.get('FirstURL', ''),
                        content=topic.get('Text', ''),
                        source='web',
                        timestamp=datetime.now(),
                        metadata={
                            'type': 'related_topic'
                        }
                    )
                    results.append(result)
            
            return results[:limit]
        except (httpx.HTTPError, ValueError) as e:
            logger.error(f"Web search failed: {e}")
            return []
    
    def get_source_name(self) -> str:
        return "web"

class RedditSearchAdapter(SearchAdapter):
    """Search adapter for Reddit."""
    
    def __init__(self):
        self.base_url = "https://www.reddit.com/search.json"
    
    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search Reddit posts."""
        params = {
            'q': query,
            'sort': 'relevance',
            'limit': min(limit, 25),
            't': 'all'
        }
        
        headers = {
            'User-Agent': 'PromptResearcher/1.0'
        }
        
        try:
            timeout = httpx.Timeout(10.0, connect=5.0)
            async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
            
            results = []
            for post in data['data']['children']:
                post_data = post['data']
                result = SearchResult(
                    title=post_data['title'],
                    url=f"https://reddit.com{post_data['permalink']}",
                    content=post_data.get('selftext', ''),
                    source='reddit',
                    timestamp=datetime.now(),
                    metadata={
                        'subreddit': post_data['subreddit'],
                        'score': post_data['score'],
                        'num_comments': post_data['num_comments'],
                        'created_utc': post_data['created_utc'],
                        'author': post_data['author']
                    }
                )
                results.append(result)
            
            return results
        except (httpx.HTTPError, ValueError) as e:
            logger.error(f"Reddit search failed: {e}")
            return []
    
    def get_source_name(self) -> str:
        return "reddit"

class MemorySystem:
    """Manages persistent storage and retrieval of research data."""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.db_path = self.data_dir / "memory.db"
        self.raw_data_dir = self.data_dir / "raw"
        self.processed_data_dir = self.data_dir / "processed"
        
        self.raw_data_dir.mkdir(exist_ok=True)
        self.processed_data_dir.mkdir(exist_ok=True)
        
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                query TEXT NOT NULL,
                description TEXT,
                sources TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                results_count INTEGER DEFAULT 0
            )
        ''')
        
        # Create search_results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT,
                title TEXT,
                url TEXT,
                content TEXT,
                source TEXT,
                timestamp TEXT,
                metadata TEXT,
                relevance_score REAL,
                FOREIGN KEY (project_id) REFERENCES projects (project_id)
            )
        ''')
        
        # Create search_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT,
                query TEXT,
                source TEXT,
                timestamp TEXT,
                results_count INTEGER,
                FOREIGN KEY (project_id) REFERENCES projects (project_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_project(self, project: ResearchProject) -> bool:
        """Save or update a research project."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            project_dict = project.to_dict()
            project_dict['sources'] = json.dumps(project.sources)
            
            cursor.execute('''
                INSERT OR REPLACE INTO projects 
                (project_id, query, description, sources, status, created_at, updated_at, results_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_dict['project_id'],
                project_dict['query'],
                project_dict['description'],
                project_dict['sources'],
                project_dict['status'],
                project_dict['created_at'],
                project_dict['updated_at'],
                project_dict['results_count']
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Failed to save project: {e}")
            return False
    
    def get_project(self, project_id: str) -> Optional[ResearchProject]:
        """Retrieve a research project by ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM projects WHERE project_id = ?', (project_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return ResearchProject(
                    project_id=row[0],
                    query=row[1],
                    description=row[2],
                    sources=json.loads(row[3]),
                    status=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    updated_at=datetime.fromisoformat(row[6]),
                    results_count=row[7]
                )
            return None
        except Exception as e:
            logger.error(f"Failed to get project: {e}")
            return None
    
    def save_search_results(self, project_id: str, results: List[SearchResult]) -> bool:
        """Save search results for a project."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for result in results:
                result_dict = result.to_dict()
                cursor.execute('''
                    INSERT INTO search_results 
                    (project_id, title, url, content, source, timestamp, metadata, relevance_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    project_id,
                    result_dict['title'],
                    result_dict['url'],
                    result_dict['content'],
                    result_dict['source'],
                    result_dict['timestamp'],
                    json.dumps(result_dict['metadata']),
                    result_dict['relevance_score']
                ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Failed to save search results: {e}")
            return False
    
    def get_search_results(self, project_id: str) -> List[SearchResult]:
        """Retrieve all search results for a project."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM search_results WHERE project_id = ?', (project_id,))
            rows = cursor.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                result = SearchResult(
                    title=row[2],
                    url=row[3],
                    content=row[4],
                    source=row[5],
                    timestamp=datetime.fromisoformat(row[6]),
                    metadata=json.loads(row[7]),
                    relevance_score=row[8]
                )
                results.append(result)
            
            return results
        except Exception as e:
            logger.error(f"Failed to get search results: {e}")
            return []

class PromptResearcher:
    """Main agent class for conducting comprehensive research."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.memory = MemorySystem(self.data_dir / "memory")
        
        # Initialize search adapters
        self.adapters = {
            'github': GitHubSearchAdapter(),
            'web': WebSearchAdapter(),
            'reddit': RedditSearchAdapter()
        }
        
        logger.info("PromptResearcher initialized")
    
    def _generate_project_id(self, query: str) -> str:
        """Generate a unique project ID based on the query."""
        return hashlib.md5(f"{query}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
    
    async def conduct_research(self, 
                             query: str, 
                             description: str = "",
                             sources: Optional[List[str]] = None,
                             limit_per_source: int = 10) -> str:
        """Conduct comprehensive research on a given query."""
        
        if sources is None:
            sources = list(self.adapters.keys())
        
        # Create new research project
        project_id = self._generate_project_id(query)
        project = ResearchProject(
            project_id=project_id,
            query=query,
            description=description,
            sources=sources,
            status="in_progress",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        logger.info(f"Starting research project: {project_id}")
        logger.info(f"Query: {query}")
        logger.info(f"Sources: {sources}")
        
        # Save project to memory
        self.memory.save_project(project)
        
        all_results = []
        
        # Search each source
        for source in sources:
            if source in self.adapters:
                logger.info(f"Searching {source}...")
                try:
                    results = await self.adapters[source].search(query, limit_per_source)
                    all_results.extend(results)
                    logger.info(f"Found {len(results)} results from {source}")
                    
                    # Add small delay to be respectful to APIs
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Error searching {source}: {e}")
        
        # Save results to memory
        self.memory.save_search_results(project_id, all_results)
        
        # Update project status
        project.status = "completed"
        project.updated_at = datetime.now()
        project.results_count = len(all_results)
        self.memory.save_project(project)
        
        # Generate dataset
        dataset_path = self._generate_dataset(project_id, all_results)
        
        logger.info(f"Research completed. Found {len(all_results)} total results")
        logger.info(f"Dataset saved to: {dataset_path}")
        
        return project_id
    
    def _generate_dataset(self, project_id: str, results: List[SearchResult]) -> str:
        """Generate a comprehensive dataset from search results."""
        
        # Prepare data for DataFrame
        data = []
        for result in results:
            row = {
                'project_id': project_id,
                'title': result.title,
                'url': result.url,
                'content': result.content[:500] + '...' if len(result.content) > 500 else result.content,
                'source': result.source,
                'timestamp': result.timestamp.isoformat(),
                'relevance_score': result.relevance_score
            }
            
            # Add metadata fields
            for key, value in result.metadata.items():
                row[f'meta_{key}'] = value
            
            data.append(row)
        
        # Create DataFrame and save to Excel
        df = pd.DataFrame(data)
        dataset_path = self.data_dir / "processed" / f"{project_id}_dataset.xlsx"
        
        with pd.ExcelWriter(dataset_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Research_Results', index=False)
            
            # Create summary sheet
            summary_data = {
                'Metric': ['Total Results', 'Sources Used', 'GitHub Results', 'Web Results', 'Reddit Results'],
                'Value': [
                    len(results),
                    len(df['source'].unique()),
                    len(df[df['source'] == 'github']),
                    len(df[df['source'] == 'web']),
                    len(df[df['source'] == 'reddit'])
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        return str(dataset_path)
    
    async def update_research(self, project_id: str, additional_sources: Optional[List[str]] = None) -> bool:
        """Update existing research with new data."""
        
        project = self.memory.get_project(project_id)
        if not project:
            logger.error(f"Project {project_id} not found")
            return False
        
        logger.info(f"Updating research project: {project_id}")
        
        # Use original sources if no additional sources specified
        sources_to_search = additional_sources or project.sources
        
        all_results = []
        
        # Search each source
        for source in sources_to_search:
            if source in self.adapters:
                logger.info(f"Searching {source} for updates...")
                try:
                    results = await self.adapters[source].search(project.query, 10)
                    all_results.extend(results)
                    logger.info(f"Found {len(results)} new results from {source}")
                    
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Error searching {source}: {e}")
        
        # Save new results
        self.memory.save_search_results(project_id, all_results)
        
        # Update project
        project.updated_at = datetime.now()
        project.results_count += len(all_results)
        self.memory.save_project(project)
        
        # Regenerate dataset with all results
        all_project_results = self.memory.get_search_results(project_id)
        self._generate_dataset(project_id, all_project_results)
        
        logger.info(f"Research updated. Added {len(all_results)} new results")
        return True
    
    def get_research_summary(self, project_id: str) -> Dict[str, Any]:
        """Get a summary of a research project."""
        
        project = self.memory.get_project(project_id)
        if not project:
            return {}
        
        results = self.memory.get_search_results(project_id)
        
        # Calculate statistics
        source_counts = {}
        for result in results:
            source_counts[result.source] = source_counts.get(result.source, 0) + 1
        
        return {
            'project_id': project.project_id,
            'query': project.query,
            'description': project.description,
            'status': project.status,
            'created_at': project.created_at.isoformat(),
            'updated_at': project.updated_at.isoformat(),
            'total_results': len(results),
            'source_breakdown': source_counts,
            'sources_searched': project.sources
        }

# Example usage and testing
async def main():
    """Example usage of the PromptResearcher agent."""
    
    # Initialize the researcher
    researcher = PromptResearcher("./data")
    
    # Conduct research on AI agent frameworks
    project_id = await researcher.conduct_research(
        query="AI agent frameworks Python",
        description="Research on popular AI agent frameworks for Python development",
        sources=['github', 'web', 'reddit'],
        limit_per_source=5
    )
    
    # Get research summary
    summary = researcher.get_research_summary(project_id)
    print(f"Research Summary: {json.dumps(summary, indent=2)}")
    
    # Update research with additional data
    await researcher.update_research(project_id, ['github'])
    
    # Get updated summary
    updated_summary = researcher.get_research_summary(project_id)
    print(f"Updated Summary: {json.dumps(updated_summary, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
