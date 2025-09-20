#!/usr/bin/env python3
"""
Research Methodology and Configuration System for Prompt-Researcher Agent

This module defines the research methodologies, scoring systems, and 
configuration management for comprehensive multi-source research.
"""

import json
import yaml
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ResearchType(Enum):
    """Types of research that can be conducted."""
    TECHNOLOGY_ANALYSIS = "technology_analysis"
    MARKET_RESEARCH = "market_research"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    TREND_ANALYSIS = "trend_analysis"
    ACADEMIC_RESEARCH = "academic_research"
    PRODUCT_RESEARCH = "product_research"

class SourcePriority(Enum):
    """Priority levels for different sources."""
    HIGH = 3
    MEDIUM = 2
    LOW = 1

@dataclass
class SourceConfig:
    """Configuration for a research source."""
    name: str
    enabled: bool
    priority: SourcePriority
    rate_limit: int  # requests per minute
    max_results: int
    quality_weight: float
    metadata_fields: List[str]
    search_parameters: Dict[str, Any]

@dataclass
class ResearchMethodology:
    """Defines a complete research methodology."""
    name: str
    description: str
    research_type: ResearchType
    sources: List[str]
    scoring_weights: Dict[str, float]
    quality_thresholds: Dict[str, float]
    enrichment_strategies: List[str]
    analysis_dimensions: List[str]

class ScoringSystem:
    """Advanced scoring system for research results."""
    
    def __init__(self):
        self.scoring_criteria = {
            'relevance': {
                'weight': 0.30,
                'description': 'How relevant the content is to the search query'
            },
            'authority': {
                'weight': 0.25,
                'description': 'Authority and credibility of the source'
            },
            'recency': {
                'weight': 0.20,
                'description': 'How recent the information is'
            },
            'engagement': {
                'weight': 0.15,
                'description': 'Community engagement (stars, votes, comments)'
            },
            'completeness': {
                'weight': 0.10,
                'description': 'Completeness and depth of information'
            }
        }
    
    def calculate_relevance_score(self, result_title: str, result_content: str, query: str) -> float:
        """Calculate relevance score based on keyword matching and semantic similarity."""
        query_terms = query.lower().split()
        title_lower = result_title.lower()
        content_lower = result_content.lower()
        
        # Simple keyword matching (can be enhanced with semantic similarity)
        title_matches = sum(1 for term in query_terms if term in title_lower)
        content_matches = sum(1 for term in query_terms if term in content_lower)
        
        title_score = min(title_matches / len(query_terms), 1.0) * 2  # Title matches are weighted higher
        content_score = min(content_matches / len(query_terms), 1.0)
        
        return min((title_score + content_score) / 3, 1.0)
    
    def calculate_authority_score(self, source: str, metadata: Dict[str, Any]) -> float:
        """Calculate authority score based on source type and metadata."""
        source_authority = {
            'github': 0.9,
            'academic': 0.95,
            'web': 0.7,
            'reddit': 0.6,
            'youtube': 0.5,
            'blog': 0.6,
            'forum': 0.5
        }
        
        base_score = source_authority.get(source, 0.5)
        
        # Adjust based on metadata
        if source == 'github':
            stars = metadata.get('stars', 0)
            forks = metadata.get('forks', 0)
            # Normalize GitHub metrics
            star_score = min(stars / 1000, 1.0) * 0.3
            fork_score = min(forks / 100, 1.0) * 0.2
            base_score = min(base_score + star_score + fork_score, 1.0)
        
        elif source == 'reddit':
            score = metadata.get('score', 0)
            comments = metadata.get('num_comments', 0)
            # Normalize Reddit metrics
            score_boost = min(score / 100, 1.0) * 0.2
            comment_boost = min(comments / 50, 1.0) * 0.1
            base_score = min(base_score + score_boost + comment_boost, 1.0)
        
        return base_score
    
    def calculate_recency_score(self, timestamp_str: str) -> float:
        """Calculate recency score based on how recent the content is."""
        from datetime import datetime, timedelta
        
        try:
            if isinstance(timestamp_str, str):
                # Try to parse various timestamp formats
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%SZ']:
                    try:
                        timestamp = datetime.strptime(timestamp_str[:19], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return 0.5  # Default score if parsing fails
            else:
                timestamp = timestamp_str
            
            now = datetime.now()
            age = now - timestamp
            
            # Score based on age (newer is better)
            if age <= timedelta(days=30):
                return 1.0
            elif age <= timedelta(days=90):
                return 0.8
            elif age <= timedelta(days=365):
                return 0.6
            elif age <= timedelta(days=730):
                return 0.4
            else:
                return 0.2
        except Exception:
            return 0.5  # Default score if calculation fails
    
    def calculate_engagement_score(self, source: str, metadata: Dict[str, Any]) -> float:
        """Calculate engagement score based on community interaction."""
        if source == 'github':
            stars = metadata.get('stars', 0)
            forks = metadata.get('forks', 0)
            watchers = metadata.get('watchers', 0)
            
            # Normalize and combine metrics
            star_score = min(stars / 500, 1.0) * 0.5
            fork_score = min(forks / 100, 1.0) * 0.3
            watcher_score = min(watchers / 50, 1.0) * 0.2
            
            return star_score + fork_score + watcher_score
        
        elif source == 'reddit':
            score = metadata.get('score', 0)
            comments = metadata.get('num_comments', 0)
            
            score_norm = min(score / 50, 1.0) * 0.6
            comment_norm = min(comments / 25, 1.0) * 0.4
            
            return score_norm + comment_norm
        
        elif source == 'youtube':
            views = metadata.get('views', 0)
            likes = metadata.get('likes', 0)
            
            view_score = min(views / 10000, 1.0) * 0.7
            like_score = min(likes / 100, 1.0) * 0.3
            
            return view_score + like_score
        
        return 0.5  # Default score for other sources
    
    def calculate_completeness_score(self, content: str, metadata: Dict[str, Any]) -> float:
        """Calculate completeness score based on content length and metadata richness."""
        content_length = len(content.strip())
        metadata_richness = len([v for v in metadata.values() if v is not None and v != ''])
        
        # Score based on content length
        length_score = min(content_length / 1000, 1.0) * 0.7
        
        # Score based on metadata richness
        metadata_score = min(metadata_richness / 10, 1.0) * 0.3
        
        return length_score + metadata_score
    
    def calculate_overall_score(self, result, query: str) -> float:
        """Calculate overall score for a search result."""
        scores = {}
        
        # Calculate individual scores
        scores['relevance'] = self.calculate_relevance_score(
            result.title, result.content, query
        )
        scores['authority'] = self.calculate_authority_score(
            result.source, result.metadata
        )
        scores['recency'] = self.calculate_recency_score(
            result.timestamp.isoformat()
        )
        scores['engagement'] = self.calculate_engagement_score(
            result.source, result.metadata
        )
        scores['completeness'] = self.calculate_completeness_score(
            result.content, result.metadata
        )
        
        # Calculate weighted overall score
        overall_score = sum(
            scores[criterion] * self.scoring_criteria[criterion]['weight']
            for criterion in scores
        )
        
        # Store individual scores in metadata for analysis
        result.metadata['scoring_breakdown'] = scores
        result.metadata['overall_score'] = overall_score
        
        return overall_score

class DatasetManager:
    """Manages dataset creation, enrichment, and analysis."""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)
    
    def create_comprehensive_dataset(self, project_id: str, results: List, methodology: ResearchMethodology) -> Dict[str, Any]:
        """Create a comprehensive dataset with multiple analysis dimensions."""
        
        # Organize results by source
        results_by_source = {}
        for result in results:
            source = result.source
            if source not in results_by_source:
                results_by_source[source] = []
            results_by_source[source].append(result)
        
        # Create main dataset
        dataset = {
            'metadata': {
                'project_id': project_id,
                'methodology': methodology.name,
                'research_type': methodology.research_type.value,
                'total_results': len(results),
                'sources_used': list(results_by_source.keys()),
                'analysis_dimensions': methodology.analysis_dimensions
            },
            'results': [],
            'analysis': {},
            'insights': []
        }
        
        # Process each result
        for result in results:
            result_data = {
                'title': result.title,
                'url': result.url,
                'content': result.content,
                'source': result.source,
                'timestamp': result.timestamp.isoformat(),
                'relevance_score': result.relevance_score,
                'metadata': result.metadata
            }
            dataset['results'].append(result_data)
        
        # Perform analysis by dimension
        for dimension in methodology.analysis_dimensions:
            dataset['analysis'][dimension] = self._analyze_dimension(results, dimension)
        
        # Generate insights
        dataset['insights'] = self._generate_insights(results, methodology)
        
        return dataset
    
    def _analyze_dimension(self, results: List, dimension: str) -> Dict[str, Any]:
        """Analyze results along a specific dimension."""
        analysis = {
            'dimension': dimension,
            'summary': {},
            'trends': [],
            'top_results': []
        }
        
        if dimension == 'popularity':
            # Analyze by engagement metrics
            sorted_results = sorted(
                results, 
                key=lambda r: r.metadata.get('scoring_breakdown', {}).get('engagement', 0),
                reverse=True
            )
            analysis['top_results'] = [
                {
                    'title': r.title,
                    'source': r.source,
                    'engagement_score': r.metadata.get('scoring_breakdown', {}).get('engagement', 0),
                    'url': r.url
                }
                for r in sorted_results[:10]
            ]
        
        elif dimension == 'recency':
            # Analyze by recency
            sorted_results = sorted(
                results,
                key=lambda r: r.metadata.get('scoring_breakdown', {}).get('recency', 0),
                reverse=True
            )
            analysis['top_results'] = [
                {
                    'title': r.title,
                    'source': r.source,
                    'recency_score': r.metadata.get('scoring_breakdown', {}).get('recency', 0),
                    'timestamp': r.timestamp.isoformat(),
                    'url': r.url
                }
                for r in sorted_results[:10]
            ]
        
        elif dimension == 'authority':
            # Analyze by source authority
            sorted_results = sorted(
                results,
                key=lambda r: r.metadata.get('scoring_breakdown', {}).get('authority', 0),
                reverse=True
            )
            analysis['top_results'] = [
                {
                    'title': r.title,
                    'source': r.source,
                    'authority_score': r.metadata.get('scoring_breakdown', {}).get('authority', 0),
                    'url': r.url
                }
                for r in sorted_results[:10]
            ]
        
        return analysis
    
    def _generate_insights(self, results: List, methodology: ResearchMethodology) -> List[Dict[str, Any]]:
        """Generate insights from the research results."""
        insights = []
        
        # Source distribution insight
        source_counts = {}
        for result in results:
            source_counts[result.source] = source_counts.get(result.source, 0) + 1
        
        insights.append({
            'type': 'source_distribution',
            'title': 'Source Distribution Analysis',
            'description': f'Results were found across {len(source_counts)} different sources',
            'data': source_counts,
            'recommendation': f"The most productive source was {max(source_counts, key=source_counts.get)} with {max(source_counts.values())} results"
        })
        
        # Quality insight
        avg_score = sum(r.relevance_score for r in results) / len(results) if results else 0
        high_quality_count = sum(1 for r in results if r.relevance_score > 0.7)
        
        insights.append({
            'type': 'quality_analysis',
            'title': 'Result Quality Analysis',
            'description': f'Average relevance score: {avg_score:.2f}',
            'data': {
                'average_score': avg_score,
                'high_quality_results': high_quality_count,
                'total_results': len(results)
            },
            'recommendation': f"{high_quality_count} out of {len(results)} results ({high_quality_count/len(results)*100:.1f}%) are high quality"
        })
        
        # Recency insight
        recent_results = sum(
            1 for r in results 
            if r.metadata.get('scoring_breakdown', {}).get('recency', 0) > 0.8
        )
        
        insights.append({
            'type': 'recency_analysis',
            'title': 'Content Recency Analysis',
            'description': f'{recent_results} results are very recent (within 30 days)',
            'data': {
                'recent_results': recent_results,
                'total_results': len(results)
            },
            'recommendation': 'Consider setting up alerts for ongoing monitoring of new developments'
        })
        
        return insights

class ConfigurationManager:
    """Manages research configurations and methodologies."""
    
    def __init__(self, config_dir: Path):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.sources_config_path = self.config_dir / "sources.yaml"
        self.methodologies_config_path = self.config_dir / "methodologies.yaml"
        
        self._initialize_default_configs()
    
    def _initialize_default_configs(self):
        """Initialize default configuration files."""
        
        # Default source configurations
        default_sources = {
            'github': {
                'name': 'GitHub',
                'enabled': True,
                'priority': 'HIGH',
                'rate_limit': 60,
                'max_results': 20,
                'quality_weight': 0.9,
                'metadata_fields': ['stars', 'forks', 'language', 'updated_at', 'topics'],
                'search_parameters': {
                    'sort': 'stars',
                    'order': 'desc'
                }
            },
            'web': {
                'name': 'Web Search',
                'enabled': True,
                'priority': 'MEDIUM',
                'rate_limit': 30,
                'max_results': 15,
                'quality_weight': 0.7,
                'metadata_fields': ['source_name', 'type'],
                'search_parameters': {}
            },
            'reddit': {
                'name': 'Reddit',
                'enabled': True,
                'priority': 'MEDIUM',
                'rate_limit': 60,
                'max_results': 15,
                'quality_weight': 0.6,
                'metadata_fields': ['subreddit', 'score', 'num_comments', 'author'],
                'search_parameters': {
                    'sort': 'relevance',
                    't': 'all'
                }
            }
        }
        
        # Default methodologies
        default_methodologies = {
            'technology_analysis': {
                'name': 'Technology Analysis',
                'description': 'Comprehensive analysis of technologies, frameworks, and tools',
                'research_type': 'TECHNOLOGY_ANALYSIS',
                'sources': ['github', 'web', 'reddit'],
                'scoring_weights': {
                    'relevance': 0.30,
                    'authority': 0.25,
                    'recency': 0.20,
                    'engagement': 0.15,
                    'completeness': 0.10
                },
                'quality_thresholds': {
                    'minimum_score': 0.4,
                    'high_quality_score': 0.7
                },
                'enrichment_strategies': [
                    'cross_reference_validation',
                    'trend_analysis',
                    'community_sentiment'
                ],
                'analysis_dimensions': [
                    'popularity',
                    'recency',
                    'authority',
                    'community_engagement'
                ]
            },
            'market_research': {
                'name': 'Market Research',
                'description': 'Market analysis and competitive intelligence',
                'research_type': 'MARKET_RESEARCH',
                'sources': ['web', 'reddit'],
                'scoring_weights': {
                    'relevance': 0.35,
                    'authority': 0.30,
                    'recency': 0.25,
                    'engagement': 0.10,
                    'completeness': 0.00
                },
                'quality_thresholds': {
                    'minimum_score': 0.5,
                    'high_quality_score': 0.8
                },
                'enrichment_strategies': [
                    'competitive_analysis',
                    'market_sizing',
                    'trend_identification'
                ],
                'analysis_dimensions': [
                    'market_size',
                    'competition',
                    'trends',
                    'opportunities'
                ]
            }
        }
        
        # Write default configs if they don't exist
        if not self.sources_config_path.exists():
            with open(self.sources_config_path, 'w') as f:
                yaml.dump(default_sources, f, default_flow_style=False)
        
        if not self.methodologies_config_path.exists():
            with open(self.methodologies_config_path, 'w') as f:
                yaml.dump(default_methodologies, f, default_flow_style=False)
    
    def load_source_config(self, source_name: str) -> Optional[SourceConfig]:
        """Load configuration for a specific source."""
        try:
            with open(self.sources_config_path, 'r') as f:
                sources = yaml.safe_load(f)
            
            if source_name in sources:
                config_data = sources[source_name]
                return SourceConfig(
                    name=config_data['name'],
                    enabled=config_data['enabled'],
                    priority=SourcePriority[config_data['priority']],
                    rate_limit=config_data['rate_limit'],
                    max_results=config_data['max_results'],
                    quality_weight=config_data['quality_weight'],
                    metadata_fields=config_data['metadata_fields'],
                    search_parameters=config_data['search_parameters']
                )
            return None
        except Exception as e:
            logger.error(f"Failed to load source config for {source_name}: {e}")
            return None
    
    def load_methodology(self, methodology_name: str) -> Optional[ResearchMethodology]:
        """Load a research methodology by name."""
        try:
            with open(self.methodologies_config_path, 'r') as f:
                methodologies = yaml.safe_load(f)
            
            if methodology_name in methodologies:
                config_data = methodologies[methodology_name]
                return ResearchMethodology(
                    name=config_data['name'],
                    description=config_data['description'],
                    research_type=ResearchType[config_data['research_type']],
                    sources=config_data['sources'],
                    scoring_weights=config_data['scoring_weights'],
                    quality_thresholds=config_data['quality_thresholds'],
                    enrichment_strategies=config_data['enrichment_strategies'],
                    analysis_dimensions=config_data['analysis_dimensions']
                )
            return None
        except Exception as e:
            logger.error(f"Failed to load methodology {methodology_name}: {e}")
            return None
    
    def get_available_methodologies(self) -> List[str]:
        """Get list of available research methodologies."""
        try:
            with open(self.methodologies_config_path, 'r') as f:
                methodologies = yaml.safe_load(f)
            return list(methodologies.keys())
        except Exception as e:
            logger.error(f"Failed to get available methodologies: {e}")
            return []
    
    def save_custom_methodology(self, methodology: ResearchMethodology) -> bool:
        """Save a custom research methodology."""
        try:
            # Load existing methodologies
            with open(self.methodologies_config_path, 'r') as f:
                methodologies = yaml.safe_load(f)
            
            # Add new methodology
            methodologies[methodology.name.lower().replace(' ', '_')] = {
                'name': methodology.name,
                'description': methodology.description,
                'research_type': methodology.research_type.value,
                'sources': methodology.sources,
                'scoring_weights': methodology.scoring_weights,
                'quality_thresholds': methodology.quality_thresholds,
                'enrichment_strategies': methodology.enrichment_strategies,
                'analysis_dimensions': methodology.analysis_dimensions
            }
            
            # Save updated methodologies
            with open(self.methodologies_config_path, 'w') as f:
                yaml.dump(methodologies, f, default_flow_style=False)
            
            return True
        except Exception as e:
            logger.error(f"Failed to save custom methodology: {e}")
            return False
