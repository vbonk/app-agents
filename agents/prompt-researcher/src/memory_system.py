#!/usr/bin/env python3
"""
Advanced Memory System with Learning Capabilities for Prompt-Researcher Agent

This module implements a sophisticated memory system that learns from past research,
improves search strategies, and maintains comprehensive knowledge graphs.
"""

import json
import sqlite3
import pickle
import hashlib
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import logging

logger = logging.getLogger(__name__)

@dataclass
class SearchPattern:
    """Represents a learned search pattern."""
    query_keywords: List[str]
    successful_sources: List[str]
    optimal_parameters: Dict[str, Any]
    success_rate: float
    usage_count: int
    last_used: datetime
    effectiveness_score: float

@dataclass
class LearningInsight:
    """Represents a learned insight from research patterns."""
    insight_type: str
    description: str
    confidence: float
    supporting_evidence: List[str]
    created_at: datetime
    applications: List[str]

@dataclass
class ResearchStrategy:
    """Represents an optimized research strategy."""
    strategy_id: str
    name: str
    description: str
    query_patterns: List[str]
    source_priorities: Dict[str, float]
    parameter_optimizations: Dict[str, Any]
    success_metrics: Dict[str, float]
    created_at: datetime
    usage_count: int

class KnowledgeGraph:
    """Manages relationships between research topics, sources, and results."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_knowledge_graph_db()
    
    def _init_knowledge_graph_db(self):
        """Initialize the knowledge graph database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Entities table (topics, sources, results)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                entity_id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL,
                name TEXT NOT NULL,
                properties TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_entity TEXT,
                target_entity TEXT,
                relationship_type TEXT,
                strength REAL,
                properties TEXT,
                created_at TEXT,
                FOREIGN KEY (source_entity) REFERENCES entities (entity_id),
                FOREIGN KEY (target_entity) REFERENCES entities (entity_id)
            )
        ''')
        
        # Topic clusters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topic_clusters (
                cluster_id TEXT PRIMARY KEY,
                cluster_name TEXT,
                keywords TEXT,
                entities TEXT,
                coherence_score REAL,
                created_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_entity(self, entity_id: str, entity_type: str, name: str, properties: Dict[str, Any] = None):
        """Add an entity to the knowledge graph."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO entities 
            (entity_id, entity_type, name, properties, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            entity_id,
            entity_type,
            name,
            json.dumps(properties or {}),
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def add_relationship(self, source_entity: str, target_entity: str, 
                        relationship_type: str, strength: float = 1.0, 
                        properties: Dict[str, Any] = None):
        """Add a relationship between entities."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO relationships 
            (source_entity, target_entity, relationship_type, strength, properties, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            source_entity,
            target_entity,
            relationship_type,
            strength,
            json.dumps(properties or {}),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_related_entities(self, entity_id: str, relationship_type: str = None) -> List[Dict[str, Any]]:
        """Get entities related to a given entity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT e.entity_id, e.entity_type, e.name, e.properties, r.strength, r.relationship_type
            FROM entities e
            JOIN relationships r ON e.entity_id = r.target_entity
            WHERE r.source_entity = ?
        '''
        params = [entity_id]
        
        if relationship_type:
            query += ' AND r.relationship_type = ?'
            params.append(relationship_type)
        
        query += ' ORDER BY r.strength DESC'
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'entity_id': row[0],
                'entity_type': row[1],
                'name': row[2],
                'properties': json.loads(row[3]),
                'strength': row[4],
                'relationship_type': row[5]
            }
            for row in results
        ]
    
    def find_similar_topics(self, keywords: List[str], threshold: float = 0.3) -> List[str]:
        """Find topics similar to given keywords."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple keyword matching (can be enhanced with embeddings)
        similar_topics = []
        
        cursor.execute('SELECT entity_id, name, properties FROM entities WHERE entity_type = "topic"')
        topics = cursor.fetchall()
        
        for topic in topics:
            topic_properties = json.loads(topic[2])
            topic_keywords = topic_properties.get('keywords', [])
            
            # Calculate similarity based on keyword overlap
            overlap = len(set(keywords) & set(topic_keywords))
            similarity = overlap / max(len(keywords), len(topic_keywords))
            
            if similarity >= threshold:
                similar_topics.append(topic[0])
        
        conn.close()
        return similar_topics

class LearningEngine:
    """Learns from research patterns and optimizes future searches."""
    
    def __init__(self, memory_db_path: Path):
        self.db_path = memory_db_path
        self.patterns_cache = {}
        self.insights_cache = []
        self._init_learning_db()
    
    def _init_learning_db(self):
        """Initialize the learning database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Search patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_patterns (
                pattern_id TEXT PRIMARY KEY,
                query_keywords TEXT,
                successful_sources TEXT,
                optimal_parameters TEXT,
                success_rate REAL,
                usage_count INTEGER,
                last_used TEXT,
                effectiveness_score REAL
            )
        ''')
        
        # Learning insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_insights (
                insight_id TEXT PRIMARY KEY,
                insight_type TEXT,
                description TEXT,
                confidence REAL,
                supporting_evidence TEXT,
                created_at TEXT,
                applications TEXT
            )
        ''')
        
        # Research strategies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_strategies (
                strategy_id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                query_patterns TEXT,
                source_priorities TEXT,
                parameter_optimizations TEXT,
                success_metrics TEXT,
                created_at TEXT,
                usage_count INTEGER
            )
        ''')
        
        # Performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                metric_id TEXT PRIMARY KEY,
                project_id TEXT,
                query TEXT,
                source TEXT,
                results_count INTEGER,
                avg_relevance_score REAL,
                execution_time REAL,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_search_performance(self, project_id: str, query: str, 
                                 results_by_source: Dict[str, List], 
                                 execution_times: Dict[str, float]):
        """Analyze the performance of a search and learn from it."""
        
        # Calculate metrics for each source
        for source, results in results_by_source.items():
            if not results:
                continue
            
            avg_relevance = sum(r.relevance_score for r in results) / len(results)
            execution_time = execution_times.get(source, 0)
            
            # Store performance metrics
            self._store_performance_metric(
                project_id, query, source, len(results), 
                avg_relevance, execution_time
            )
            
            # Update or create search pattern
            self._update_search_pattern(query, source, avg_relevance, len(results))
        
        # Generate insights from the search
        self._generate_search_insights(query, results_by_source)
    
    def _store_performance_metric(self, project_id: str, query: str, source: str,
                                results_count: int, avg_relevance: float, 
                                execution_time: float):
        """Store performance metrics for analysis."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        metric_id = hashlib.md5(f"{project_id}_{source}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        cursor.execute('''
            INSERT INTO performance_metrics 
            (metric_id, project_id, query, source, results_count, avg_relevance_score, execution_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metric_id, project_id, query, source, results_count, 
            avg_relevance, execution_time, datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def _update_search_pattern(self, query: str, source: str, 
                             avg_relevance: float, results_count: int):
        """Update or create a search pattern based on performance."""
        
        # Extract keywords from query
        keywords = [word.lower().strip() for word in query.split() if len(word) > 2]
        pattern_key = "_".join(sorted(keywords))
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if pattern exists
        cursor.execute('SELECT * FROM search_patterns WHERE pattern_id = ?', (pattern_key,))
        existing_pattern = cursor.fetchone()
        
        if existing_pattern:
            # Update existing pattern
            current_success_rate = existing_pattern[4]
            current_usage_count = existing_pattern[5]
            
            # Calculate new success rate (weighted average)
            new_success_rate = (current_success_rate * current_usage_count + avg_relevance) / (current_usage_count + 1)
            new_usage_count = current_usage_count + 1
            
            # Update successful sources
            current_sources = json.loads(existing_pattern[2])
            if source not in current_sources:
                current_sources.append(source)
            
            cursor.execute('''
                UPDATE search_patterns 
                SET successful_sources = ?, success_rate = ?, usage_count = ?, 
                    last_used = ?, effectiveness_score = ?
                WHERE pattern_id = ?
            ''', (
                json.dumps(current_sources),
                new_success_rate,
                new_usage_count,
                datetime.now().isoformat(),
                new_success_rate * results_count,  # Simple effectiveness metric
                pattern_key
            ))
        else:
            # Create new pattern
            cursor.execute('''
                INSERT INTO search_patterns 
                (pattern_id, query_keywords, successful_sources, optimal_parameters, 
                 success_rate, usage_count, last_used, effectiveness_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern_key,
                json.dumps(keywords),
                json.dumps([source]),
                json.dumps({}),  # Will be populated with optimal parameters later
                avg_relevance,
                1,
                datetime.now().isoformat(),
                avg_relevance * results_count
            ))
        
        conn.commit()
        conn.close()
    
    def _generate_search_insights(self, query: str, results_by_source: Dict[str, List]):
        """Generate insights from search results."""
        
        insights = []
        
        # Source effectiveness insight
        source_scores = {}
        for source, results in results_by_source.items():
            if results:
                avg_score = sum(r.relevance_score for r in results) / len(results)
                source_scores[source] = avg_score
        
        if source_scores:
            best_source = max(source_scores, key=source_scores.get)
            worst_source = min(source_scores, key=source_scores.get)
            
            if source_scores[best_source] - source_scores[worst_source] > 0.3:
                insight = LearningInsight(
                    insight_type="source_effectiveness",
                    description=f"For queries like '{query}', {best_source} performs significantly better than {worst_source}",
                    confidence=0.8,
                    supporting_evidence=[f"{best_source}: {source_scores[best_source]:.2f}", f"{worst_source}: {source_scores[worst_source]:.2f}"],
                    created_at=datetime.now(),
                    applications=["source_prioritization", "search_optimization"]
                )
                insights.append(insight)
        
        # Query complexity insight
        query_words = len(query.split())
        total_results = sum(len(results) for results in results_by_source.values())
        
        if query_words > 5 and total_results < 10:
            insight = LearningInsight(
                insight_type="query_complexity",
                description=f"Complex queries with {query_words} words tend to return fewer results",
                confidence=0.6,
                supporting_evidence=[f"Query length: {query_words}", f"Total results: {total_results}"],
                created_at=datetime.now(),
                applications=["query_simplification", "search_strategy"]
            )
            insights.append(insight)
        
        # Store insights
        for insight in insights:
            self._store_insight(insight)
    
    def _store_insight(self, insight: LearningInsight):
        """Store a learning insight."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        insight_id = hashlib.md5(f"{insight.insight_type}_{insight.description}_{insight.created_at.isoformat()}".encode()).hexdigest()[:12]
        
        cursor.execute('''
            INSERT OR REPLACE INTO learning_insights 
            (insight_id, insight_type, description, confidence, supporting_evidence, created_at, applications)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            insight_id,
            insight.insight_type,
            insight.description,
            insight.confidence,
            json.dumps(insight.supporting_evidence),
            insight.created_at.isoformat(),
            json.dumps(insight.applications)
        ))
        
        conn.commit()
        conn.close()
    
    def get_optimization_recommendations(self, query: str) -> Dict[str, Any]:
        """Get optimization recommendations based on learned patterns."""
        
        keywords = [word.lower().strip() for word in query.split() if len(word) > 2]
        
        recommendations = {
            'source_priorities': {},
            'query_suggestions': [],
            'parameter_optimizations': {},
            'confidence': 0.0
        }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find similar patterns
        cursor.execute('SELECT * FROM search_patterns ORDER BY effectiveness_score DESC')
        patterns = cursor.fetchall()
        
        matching_patterns = []
        for pattern in patterns:
            pattern_keywords = json.loads(pattern[1])
            overlap = len(set(keywords) & set(pattern_keywords))
            similarity = overlap / max(len(keywords), len(pattern_keywords)) if keywords and pattern_keywords else 0
            
            if similarity > 0.3:  # Threshold for similarity
                matching_patterns.append((pattern, similarity))
        
        if matching_patterns:
            # Sort by similarity and effectiveness
            matching_patterns.sort(key=lambda x: x[1] * x[0][7], reverse=True)  # similarity * effectiveness_score
            
            # Aggregate recommendations from top patterns
            source_votes = defaultdict(float)
            total_weight = 0
            
            for pattern, similarity in matching_patterns[:5]:  # Top 5 patterns
                weight = similarity * pattern[7]  # similarity * effectiveness_score
                total_weight += weight
                
                successful_sources = json.loads(pattern[2])
                for source in successful_sources:
                    source_votes[source] += weight
            
            # Normalize source priorities
            if total_weight > 0:
                for source, votes in source_votes.items():
                    recommendations['source_priorities'][source] = votes / total_weight
                
                recommendations['confidence'] = min(total_weight / len(matching_patterns), 1.0)
        
        # Get insights-based recommendations
        cursor.execute('''
            SELECT * FROM learning_insights 
            WHERE confidence > 0.5 
            ORDER BY confidence DESC
        ''')
        insights = cursor.fetchall()
        
        for insight in insights[:3]:  # Top 3 insights
            if insight[1] == "source_effectiveness":
                # Extract source recommendation from description
                description = insight[2]
                if "performs significantly better" in description:
                    # Simple parsing - can be enhanced
                    parts = description.split()
                    if len(parts) > 5:
                        recommended_source = parts[5]  # Rough extraction
                        if recommended_source in recommendations['source_priorities']:
                            recommendations['source_priorities'][recommended_source] *= 1.2  # Boost
            
            elif insight[1] == "query_complexity":
                recommendations['query_suggestions'].append("Consider simplifying the query for better results")
        
        conn.close()
        return recommendations
    
    def create_optimized_strategy(self, query: str, research_type: str) -> Optional[ResearchStrategy]:
        """Create an optimized research strategy based on learned patterns."""
        
        recommendations = self.get_optimization_recommendations(query)
        
        if recommendations['confidence'] < 0.3:
            return None  # Not enough confidence to create strategy
        
        strategy_id = hashlib.md5(f"{query}_{research_type}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        strategy = ResearchStrategy(
            strategy_id=strategy_id,
            name=f"Optimized Strategy for {research_type}",
            description=f"Auto-generated strategy based on learned patterns for queries similar to '{query}'",
            query_patterns=[query],
            source_priorities=recommendations['source_priorities'],
            parameter_optimizations=recommendations['parameter_optimizations'],
            success_metrics={'confidence': recommendations['confidence']},
            created_at=datetime.now(),
            usage_count=0
        )
        
        # Store the strategy
        self._store_strategy(strategy)
        
        return strategy
    
    def _store_strategy(self, strategy: ResearchStrategy):
        """Store a research strategy."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO research_strategies 
            (strategy_id, name, description, query_patterns, source_priorities, 
             parameter_optimizations, success_metrics, created_at, usage_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            strategy.strategy_id,
            strategy.name,
            strategy.description,
            json.dumps(strategy.query_patterns),
            json.dumps(strategy.source_priorities),
            json.dumps(strategy.parameter_optimizations),
            json.dumps(strategy.success_metrics),
            strategy.created_at.isoformat(),
            strategy.usage_count
        ))
        
        conn.commit()
        conn.close()

class AdvancedMemorySystem:
    """Advanced memory system that combines storage, learning, and knowledge graphs."""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.db_path = self.data_dir / "advanced_memory.db"
        self.knowledge_graph = KnowledgeGraph(self.db_path)
        self.learning_engine = LearningEngine(self.db_path)
        
        # Initialize main database
        self._init_main_db()
        
        logger.info("Advanced Memory System initialized")
    
    def _init_main_db(self):
        """Initialize the main memory database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enhanced projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                query TEXT NOT NULL,
                description TEXT,
                sources TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                results_count INTEGER DEFAULT 0,
                avg_relevance_score REAL,
                research_type TEXT,
                methodology TEXT,
                tags TEXT,
                parent_project_id TEXT
            )
        ''')
        
        # Enhanced search results table
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
                quality_score REAL,
                processed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (project_id) REFERENCES projects (project_id)
            )
        ''')
        
        # Search sessions table for tracking individual searches
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_sessions (
                session_id TEXT PRIMARY KEY,
                project_id TEXT,
                query TEXT,
                sources_used TEXT,
                start_time TEXT,
                end_time TEXT,
                total_results INTEGER,
                avg_quality_score REAL,
                strategy_used TEXT,
                FOREIGN KEY (project_id) REFERENCES projects (project_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_research_session(self, project_id: str, query: str, 
                             sources_used: List[str], results: List,
                             strategy_used: str = None) -> str:
        """Store a complete research session with learning analysis."""
        
        session_id = hashlib.md5(f"{project_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        
        # Calculate session metrics
        total_results = len(results)
        avg_quality = sum(r.relevance_score for r in results) / total_results if results else 0
        
        # Store session
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO search_sessions 
            (session_id, project_id, query, sources_used, start_time, end_time, 
             total_results, avg_quality_score, strategy_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            project_id,
            query,
            json.dumps(sources_used),
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            total_results,
            avg_quality,
            strategy_used
        ))
        
        conn.commit()
        conn.close()
        
        # Analyze performance for learning
        results_by_source = defaultdict(list)
        for result in results:
            results_by_source[result.source].append(result)
        
        execution_times = {source: 1.0 for source in sources_used}  # Placeholder
        
        self.learning_engine.analyze_search_performance(
            project_id, query, dict(results_by_source), execution_times
        )
        
        # Update knowledge graph
        self._update_knowledge_graph(query, results)
        
        return session_id
    
    def _update_knowledge_graph(self, query: str, results: List):
        """Update the knowledge graph with new research data."""
        
        # Create topic entity for the query
        topic_id = hashlib.md5(query.encode()).hexdigest()[:12]
        keywords = [word.lower().strip() for word in query.split() if len(word) > 2]
        
        self.knowledge_graph.add_entity(
            topic_id, 
            "topic", 
            query,
            {"keywords": keywords, "result_count": len(results)}
        )
        
        # Add relationships between topic and sources
        source_counts = Counter(r.source for r in results)
        for source, count in source_counts.items():
            source_id = f"source_{source}"
            self.knowledge_graph.add_entity(source_id, "source", source)
            
            # Relationship strength based on result count and quality
            avg_quality = sum(r.relevance_score for r in results if r.source == source) / count
            strength = (count / len(results)) * avg_quality
            
            self.knowledge_graph.add_relationship(
                topic_id, source_id, "found_in", strength,
                {"result_count": count, "avg_quality": avg_quality}
            )
    
    def get_research_recommendations(self, query: str, research_type: str = None) -> Dict[str, Any]:
        """Get comprehensive research recommendations based on memory and learning."""
        
        recommendations = {
            'optimized_strategy': None,
            'source_priorities': {},
            'similar_topics': [],
            'query_suggestions': [],
            'expected_quality': 0.0,
            'confidence': 0.0
        }
        
        # Get learning-based recommendations
        learning_recs = self.learning_engine.get_optimization_recommendations(query)
        recommendations.update(learning_recs)
        
        # Get knowledge graph recommendations
        keywords = [word.lower().strip() for word in query.split() if len(word) > 2]
        similar_topics = self.knowledge_graph.find_similar_topics(keywords)
        
        if similar_topics:
            recommendations['similar_topics'] = similar_topics[:5]
            
            # Get successful sources from similar topics
            for topic_id in similar_topics[:3]:
                related_sources = self.knowledge_graph.get_related_entities(topic_id, "found_in")
                for source_info in related_sources:
                    source_name = source_info['name']
                    strength = source_info['strength']
                    
                    if source_name in recommendations['source_priorities']:
                        recommendations['source_priorities'][source_name] = max(
                            recommendations['source_priorities'][source_name], strength
                        )
                    else:
                        recommendations['source_priorities'][source_name] = strength
        
        # Create optimized strategy if confidence is high enough
        if recommendations['confidence'] > 0.5:
            strategy = self.learning_engine.create_optimized_strategy(query, research_type or "general")
            recommendations['optimized_strategy'] = strategy
        
        return recommendations
    
    def get_memory_insights(self) -> Dict[str, Any]:
        """Get insights about the memory system's knowledge and patterns."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        insights = {
            'total_projects': 0,
            'total_results': 0,
            'avg_project_quality': 0.0,
            'most_successful_sources': [],
            'research_trends': [],
            'learning_insights_count': 0,
            'knowledge_entities': 0
        }
        
        # Basic statistics
        cursor.execute('SELECT COUNT(*) FROM projects')
        insights['total_projects'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM search_results')
        insights['total_results'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(avg_relevance_score) FROM projects WHERE avg_relevance_score IS NOT NULL')
        result = cursor.fetchone()[0]
        insights['avg_project_quality'] = result if result else 0.0
        
        # Most successful sources
        cursor.execute('''
            SELECT source, AVG(relevance_score) as avg_score, COUNT(*) as count
            FROM search_results 
            GROUP BY source 
            ORDER BY avg_score DESC, count DESC
            LIMIT 5
        ''')
        insights['most_successful_sources'] = [
            {'source': row[0], 'avg_score': row[1], 'count': row[2]}
            for row in cursor.fetchall()
        ]
        
        # Learning insights count
        cursor.execute('SELECT COUNT(*) FROM learning_insights')
        insights['learning_insights_count'] = cursor.fetchone()[0]
        
        # Knowledge graph entities
        cursor.execute('SELECT COUNT(*) FROM entities')
        insights['knowledge_entities'] = cursor.fetchone()[0]
        
        # Research trends (projects over time)
        cursor.execute('''
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM projects 
            WHERE created_at >= date('now', '-30 days')
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        ''')
        insights['research_trends'] = [
            {'date': row[0], 'count': row[1]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return insights
    
    def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old data while preserving learning insights."""
        
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Archive old projects (don't delete, just mark as archived)
        cursor.execute('''
            UPDATE projects 
            SET status = 'archived' 
            WHERE created_at < ? AND status != 'archived'
        ''', (cutoff_date,))
        
        # Keep learning data and insights - they're valuable for future research
        # Only clean up raw search results for archived projects
        cursor.execute('''
            DELETE FROM search_results 
            WHERE project_id IN (
                SELECT project_id FROM projects 
                WHERE status = 'archived' AND created_at < ?
            )
        ''', (cutoff_date,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Cleaned up data older than {days_to_keep} days")

# Example usage
async def test_advanced_memory():
    """Test the advanced memory system."""
    
    memory = AdvancedMemorySystem(Path("./test_memory"))
    
    # Simulate storing research sessions
    from prompt_researcher import SearchResult
    
    # Mock results
    results = [
        SearchResult(
            title="Test Result 1",
            url="https://example.com/1",
            content="This is test content about AI frameworks",
            source="github",
            timestamp=datetime.now(),
            metadata={"stars": 1000, "forks": 200},
            relevance_score=0.8
        ),
        SearchResult(
            title="Test Result 2", 
            url="https://example.com/2",
            content="Another test about machine learning",
            source="web",
            timestamp=datetime.now(),
            metadata={"type": "article"},
            relevance_score=0.6
        )
    ]
    
    # Store research session
    session_id = memory.store_research_session(
        "test_project_1",
        "AI frameworks Python",
        ["github", "web"],
        results,
        "technology_analysis"
    )
    
    print(f"Stored session: {session_id}")
    
    # Get recommendations
    recommendations = memory.get_research_recommendations("Python machine learning frameworks")
    print(f"Recommendations: {json.dumps(recommendations, indent=2, default=str)}")
    
    # Get memory insights
    insights = memory.get_memory_insights()
    print(f"Memory insights: {json.dumps(insights, indent=2)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_advanced_memory())
