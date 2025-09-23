#!/usr/bin/env python3
"""
Enhanced Prompt-Researcher Agent: Complete Integration

This is the main enhanced agent that integrates all components:
- Multi-source search capabilities
- Advanced memory system with learning
- Research methodology framework
- Comprehensive dataset management
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import pandas as pd

# Import our custom modules
from prompt_researcher import PromptResearcher, SearchResult, ResearchProject
from memory_system import AdvancedMemorySystem, LearningEngine, KnowledgeGraph
from research_methodology import (
    ScoringSystem, DatasetManager, ConfigurationManager,
    ResearchMethodology, ResearchType
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedPromptResearcher:
    """
    Enhanced Prompt-Researcher Agent with advanced capabilities:
    - Multi-source research with intelligent prioritization
    - Learning from past research patterns
    - Comprehensive memory and knowledge management
    - Iterative dataset enrichment
    - Automated strategy optimization
    """
    
    def __init__(self, data_dir: str = "data", config_dir: str = "config"):
        self.data_dir = Path(data_dir)
        self.config_dir = Path(config_dir)
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize core components
        self.base_researcher = PromptResearcher(str(self.data_dir))
        self.memory_system = AdvancedMemorySystem(self.data_dir / "memory")
        self.scoring_system = ScoringSystem()
        self.dataset_manager = DatasetManager(self.data_dir)
        self.config_manager = ConfigurationManager(self.config_dir)
        
        # Agent state
        self.current_project_id = None
        self.research_history = []
        
        logger.info("Enhanced Prompt-Researcher Agent initialized")
    
    async def conduct_enhanced_research(self, 
                                      query: str,
                                      description: str = "",
                                      research_type: str = "technology_analysis",
                                      sources: Optional[List[str]] = None,
                                      use_learning: bool = True,
                                      limit_per_source: int = 15) -> Dict[str, Any]:
        """
        Conduct enhanced research with learning and optimization.
        
        Args:
            query: The research query
            description: Optional description of the research
            research_type: Type of research (technology_analysis, market_research, etc.)
            sources: List of sources to search (if None, uses optimized selection)
            use_learning: Whether to use learned patterns for optimization
            limit_per_source: Maximum results per source
            
        Returns:
            Dictionary containing research results and metadata
        """
        
        logger.info(f"Starting enhanced research: '{query}'")
        logger.info(f"Research type: {research_type}")
        
        # Get research methodology
        methodology = self.config_manager.load_methodology(research_type)
        if not methodology:
            logger.warning(f"Unknown research type '{research_type}', using default")
            methodology = self._create_default_methodology(research_type)
        
        # Get optimization recommendations if learning is enabled
        recommendations = {}
        if use_learning:
            recommendations = self.memory_system.get_research_recommendations(query, research_type)
            logger.info(f"Learning recommendations confidence: {recommendations.get('confidence', 0):.2f}")
        
        # Determine sources to use
        if sources is None:
            if recommendations.get('source_priorities'):
                # Use recommended sources, sorted by priority
                sources = sorted(
                    recommendations['source_priorities'].keys(),
                    key=lambda s: recommendations['source_priorities'][s],
                    reverse=True
                )[:4]  # Top 4 sources
            else:
                sources = methodology.sources
        
        logger.info(f"Using sources: {sources}")
        
        # Conduct base research
        project_id = await self.base_researcher.conduct_research(
            query=query,
            description=description,
            sources=sources,
            limit_per_source=limit_per_source
        )
        
        # Get raw results
        raw_results = self.base_researcher.memory.get_search_results(project_id)
        
        # Apply advanced scoring
        scored_results = []
        for result in raw_results:
            enhanced_score = self.scoring_system.calculate_overall_score(result, query)
            result.relevance_score = enhanced_score
            scored_results.append(result)
        
        # Filter results based on quality thresholds
        quality_threshold = methodology.quality_thresholds.get('minimum_score', 0.3)
        high_quality_results = [r for r in scored_results if r.relevance_score >= quality_threshold]
        
        logger.info(f"Filtered {len(high_quality_results)} high-quality results from {len(scored_results)} total")
        
        # Store research session in advanced memory
        strategy_name = 'default'
        if recommendations and recommendations.get('optimized_strategy'):
            strategy_name = recommendations['optimized_strategy'].get('name', 'default')
        
        session_id = self.memory_system.store_research_session(
            project_id, query, sources, high_quality_results, 
            strategy_used=strategy_name
        )
        
        # Create comprehensive dataset
        comprehensive_dataset = self.dataset_manager.create_comprehensive_dataset(
            project_id, high_quality_results, methodology
        )
        
        # Save enhanced dataset
        dataset_path = self._save_enhanced_dataset(project_id, comprehensive_dataset, methodology)
        
        # Update project metadata
        project = self.base_researcher.memory.get_project(project_id)
        if project:
            project.results_count = len(high_quality_results)
            project.updated_at = datetime.now()
            self.base_researcher.memory.save_project(project)
        
        # Prepare response
        research_results = {
            'project_id': project_id,
            'session_id': session_id,
            'query': query,
            'research_type': research_type,
            'methodology_used': methodology.name,
            'sources_searched': sources,
            'total_results': len(scored_results),
            'high_quality_results': len(high_quality_results),
            'quality_threshold': quality_threshold,
            'dataset_path': dataset_path,
            'learning_applied': use_learning,
            'recommendations_confidence': recommendations.get('confidence', 0),
            'results_summary': self._create_results_summary(high_quality_results),
            'insights': comprehensive_dataset['insights'],
            'analysis': comprehensive_dataset['analysis']
        }
        
        # Store in research history
        self.research_history.append(research_results)
        self.current_project_id = project_id
        
        logger.info(f"Enhanced research completed. Project ID: {project_id}")
        return research_results
    
    async def enrich_existing_research(self, 
                                     project_id: str,
                                     additional_sources: Optional[List[str]] = None,
                                     new_query_variations: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Enrich existing research with additional data and analysis.
        
        Args:
            project_id: ID of the existing research project
            additional_sources: Additional sources to search
            new_query_variations: Variations of the original query to explore
            
        Returns:
            Dictionary containing enrichment results
        """
        
        logger.info(f"Enriching research project: {project_id}")
        
        # Get existing project
        project = self.base_researcher.memory.get_project(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        original_query = project.query
        existing_results = self.base_researcher.memory.get_search_results(project_id)
        
        logger.info(f"Original query: '{original_query}'")
        logger.info(f"Existing results: {len(existing_results)}")
        
        new_results = []
        
        # Search additional sources with original query
        if additional_sources:
            logger.info(f"Searching additional sources: {additional_sources}")
            for source in additional_sources:
                if source in self.base_researcher.adapters:
                    try:
                        source_results = await self.base_researcher.adapters[source].search(original_query, 10)
                        new_results.extend(source_results)
                        logger.info(f"Found {len(source_results)} new results from {source}")
                        await asyncio.sleep(1)  # Rate limiting
                    except Exception as e:
                        logger.error(f"Error searching {source}: {e}")
        
        # Search with query variations
        if new_query_variations:
            logger.info(f"Searching with query variations: {new_query_variations}")
            for variation in new_query_variations:
                for source in project.sources:
                    if source in self.base_researcher.adapters:
                        try:
                            source_results = await self.base_researcher.adapters[source].search(variation, 5)
                            new_results.extend(source_results)
                            logger.info(f"Found {len(source_results)} results for '{variation}' from {source}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            logger.error(f"Error searching {source} with variation '{variation}': {e}")
        
        if not new_results:
            logger.warning("No new results found during enrichment")
            return {'project_id': project_id, 'new_results': 0, 'message': 'No new results found'}
        
        # Score new results
        scored_new_results = []
        for result in new_results:
            enhanced_score = self.scoring_system.calculate_overall_score(result, original_query)
            result.relevance_score = enhanced_score
            scored_new_results.append(result)
        
        # Filter for quality
        quality_threshold = 0.4  # Slightly higher threshold for enrichment
        high_quality_new_results = [r for r in scored_new_results if r.relevance_score >= quality_threshold]
        
        logger.info(f"Found {len(high_quality_new_results)} high-quality new results")
        
        # Save new results
        self.base_researcher.memory.save_search_results(project_id, high_quality_new_results)
        
        # Update project
        project.results_count += len(high_quality_new_results)
        project.updated_at = datetime.now()
        self.base_researcher.memory.save_project(project)
        
        # Store enrichment session
        enrichment_session_id = self.memory_system.store_research_session(
            project_id, f"ENRICHMENT: {original_query}", 
            additional_sources or [], high_quality_new_results,
            strategy_used="enrichment"
        )
        
        # Regenerate comprehensive dataset with all results
        all_results = existing_results + high_quality_new_results
        methodology = self.config_manager.load_methodology("technology_analysis")  # Default
        
        comprehensive_dataset = self.dataset_manager.create_comprehensive_dataset(
            project_id, all_results, methodology
        )
        
        # Save updated dataset
        dataset_path = self._save_enhanced_dataset(project_id, comprehensive_dataset, methodology, suffix="_enriched")
        
        enrichment_results = {
            'project_id': project_id,
            'enrichment_session_id': enrichment_session_id,
            'original_results_count': len(existing_results),
            'new_results_count': len(high_quality_new_results),
            'total_results_count': len(all_results),
            'quality_threshold': quality_threshold,
            'updated_dataset_path': dataset_path,
            'new_results_summary': self._create_results_summary(high_quality_new_results),
            'enrichment_insights': comprehensive_dataset['insights']
        }
        
        logger.info(f"Research enrichment completed. Added {len(high_quality_new_results)} new results")
        return enrichment_results
    
    def get_research_insights(self, project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive insights about research projects and learning patterns.
        
        Args:
            project_id: Specific project to analyze (if None, analyzes all projects)
            
        Returns:
            Dictionary containing insights and recommendations
        """
        
        insights = {
            'memory_insights': self.memory_system.get_memory_insights(),
            'project_specific': {},
            'learning_patterns': {},
            'recommendations': []
        }
        
        if project_id:
            # Get project-specific insights
            project = self.base_researcher.memory.get_project(project_id)
            if project:
                results = self.base_researcher.memory.get_search_results(project_id)
                
                insights['project_specific'] = {
                    'project_id': project_id,
                    'query': project.query,
                    'total_results': len(results),
                    'avg_quality': sum(r.relevance_score for r in results) / len(results) if results else 0,
                    'source_distribution': self._analyze_source_distribution(results),
                    'quality_distribution': self._analyze_quality_distribution(results),
                    'recommendations': self._generate_project_recommendations(project, results)
                }
        
        # Get learning patterns from memory system
        learning_recommendations = self.memory_system.get_research_recommendations("general research")
        insights['learning_patterns'] = {
            'most_effective_sources': learning_recommendations.get('source_priorities', {}),
            'confidence_level': learning_recommendations.get('confidence', 0),
            'similar_topics_found': len(learning_recommendations.get('similar_topics', []))
        }
        
        # Generate general recommendations
        insights['recommendations'] = self._generate_general_recommendations(insights)
        
        return insights
    
    def _create_default_methodology(self, research_type: str) -> ResearchMethodology:
        """Create a default methodology for unknown research types."""
        return ResearchMethodology(
            name=f"Default {research_type}",
            description=f"Default methodology for {research_type}",
            research_type=ResearchType.TECHNOLOGY_ANALYSIS,
            sources=['github', 'web', 'reddit'],
            scoring_weights={
                'relevance': 0.30,
                'authority': 0.25,
                'recency': 0.20,
                'engagement': 0.15,
                'completeness': 0.10
            },
            quality_thresholds={
                'minimum_score': 0.3,
                'high_quality_score': 0.7
            },
            enrichment_strategies=['cross_reference_validation'],
            analysis_dimensions=['popularity', 'recency', 'authority']
        )
    
    def _save_enhanced_dataset(self, project_id: str, dataset: Dict[str, Any], 
                             methodology: ResearchMethodology, suffix: str = "") -> str:
        """Save the enhanced dataset to Excel with multiple sheets."""
        
        filename = f"{project_id}_enhanced_dataset{suffix}.xlsx"
        dataset_path = self.data_dir / "processed" / filename
        
        with pd.ExcelWriter(dataset_path, engine='openpyxl') as writer:
            # Main results sheet
            results_df = pd.DataFrame([
                {
                    'title': r['title'],
                    'url': r['url'],
                    'source': r['source'],
                    'relevance_score': r['relevance_score'],
                    'content_preview': r['content'][:200] + '...' if len(r['content']) > 200 else r['content'],
                    'timestamp': r['timestamp'],
                    **{f"meta_{k}": v for k, v in r['metadata'].items() if isinstance(v, (str, int, float, bool))}
                }
                for r in dataset['results']
            ])
            results_df.to_excel(writer, sheet_name='Research_Results', index=False)
            
            # Metadata sheet
            metadata_df = pd.DataFrame([dataset['metadata']])
            metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
            
            # Analysis sheets
            for dimension, analysis in dataset['analysis'].items():
                if analysis.get('top_results'):
                    analysis_df = pd.DataFrame(analysis['top_results'])
                    sheet_name = f"Analysis_{dimension.title()}"[:31]  # Excel sheet name limit
                    analysis_df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Insights sheet
            insights_df = pd.DataFrame(dataset['insights'])
            insights_df.to_excel(writer, sheet_name='Insights', index=False)
            
            # Methodology sheet
            methodology_data = {
                'methodology_name': [methodology.name],
                'research_type': [methodology.research_type.value],
                'sources_used': [', '.join(methodology.sources)],
                'analysis_dimensions': [', '.join(methodology.analysis_dimensions)],
                'quality_threshold': [methodology.quality_thresholds.get('minimum_score', 0.3)]
            }
            methodology_df = pd.DataFrame(methodology_data)
            methodology_df.to_excel(writer, sheet_name='Methodology', index=False)
        
        return str(dataset_path)
    
    def _create_results_summary(self, results: List[SearchResult]) -> Dict[str, Any]:
        """Create a summary of research results."""
        if not results:
            return {'total': 0, 'sources': {}, 'avg_quality': 0, 'top_results': []}
        
        source_counts = {}
        quality_scores = []
        
        for result in results:
            source_counts[result.source] = source_counts.get(result.source, 0) + 1
            quality_scores.append(result.relevance_score)
        
        # Get top 5 results by quality
        top_results = sorted(results, key=lambda r: r.relevance_score, reverse=True)[:5]
        
        return {
            'total': len(results),
            'sources': source_counts,
            'avg_quality': sum(quality_scores) / len(quality_scores),
            'quality_range': {'min': min(quality_scores), 'max': max(quality_scores)},
            'top_results': [
                {
                    'title': r.title,
                    'source': r.source,
                    'quality_score': r.relevance_score,
                    'url': r.url
                }
                for r in top_results
            ]
        }
    
    def _analyze_source_distribution(self, results: List[SearchResult]) -> Dict[str, Any]:
        """Analyze the distribution of results across sources."""
        source_counts = {}
        source_quality = {}
        
        for result in results:
            source = result.source
            source_counts[source] = source_counts.get(source, 0) + 1
            
            if source not in source_quality:
                source_quality[source] = []
            source_quality[source].append(result.relevance_score)
        
        # Calculate average quality per source
        source_avg_quality = {
            source: sum(scores) / len(scores)
            for source, scores in source_quality.items()
        }
        
        return {
            'counts': source_counts,
            'avg_quality_by_source': source_avg_quality,
            'most_productive': max(source_counts, key=source_counts.get) if source_counts else None,
            'highest_quality': max(source_avg_quality, key=source_avg_quality.get) if source_avg_quality else None
        }
    
    def _analyze_quality_distribution(self, results: List[SearchResult]) -> Dict[str, Any]:
        """Analyze the quality distribution of results."""
        if not results:
            return {'high_quality': 0, 'medium_quality': 0, 'low_quality': 0}
        
        quality_scores = [r.relevance_score for r in results]
        
        high_quality = sum(1 for score in quality_scores if score >= 0.7)
        medium_quality = sum(1 for score in quality_scores if 0.4 <= score < 0.7)
        low_quality = sum(1 for score in quality_scores if score < 0.4)
        
        return {
            'high_quality': high_quality,
            'medium_quality': medium_quality,
            'low_quality': low_quality,
            'avg_score': sum(quality_scores) / len(quality_scores),
            'score_distribution': {
                'high_quality_pct': (high_quality / len(results)) * 100,
                'medium_quality_pct': (medium_quality / len(results)) * 100,
                'low_quality_pct': (low_quality / len(results)) * 100
            }
        }
    
    def _generate_project_recommendations(self, project: ResearchProject, 
                                        results: List[SearchResult]) -> List[str]:
        """Generate recommendations for a specific project."""
        recommendations = []
        
        if not results:
            recommendations.append("No results found. Consider broadening the search query or trying different sources.")
            return recommendations
        
        # Analyze quality
        avg_quality = sum(r.relevance_score for r in results) / len(results)
        if avg_quality < 0.5:
            recommendations.append("Average result quality is low. Consider refining the search query or using different keywords.")
        
        # Analyze source distribution
        source_analysis = self._analyze_source_distribution(results)
        if len(source_analysis['counts']) < 2:
            recommendations.append("Results found from only one source. Consider expanding to additional sources for broader coverage.")
        
        # Check for recent results
        recent_results = sum(1 for r in results if 'recency' in r.metadata.get('scoring_breakdown', {}) and 
                           r.metadata['scoring_breakdown']['recency'] > 0.8)
        if recent_results < len(results) * 0.3:
            recommendations.append("Few recent results found. Consider setting up monitoring for ongoing developments.")
        
        # Check result count
        if len(results) < 10:
            recommendations.append("Limited number of results. Consider using broader search terms or additional sources.")
        elif len(results) > 50:
            recommendations.append("Large number of results found. Consider using more specific search terms for focused analysis.")
        
        return recommendations
    
    def _generate_general_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """Generate general recommendations based on overall insights."""
        recommendations = []
        
        memory_insights = insights['memory_insights']
        
        # Check research activity
        if memory_insights['total_projects'] < 5:
            recommendations.append("Limited research history. Continue conducting research to improve learning and optimization.")
        
        # Check source effectiveness
        if memory_insights['most_successful_sources']:
            top_source = memory_insights['most_successful_sources'][0]
            recommendations.append(f"Consider prioritizing {top_source['source']} (avg score: {top_source['avg_score']:.2f}) for future research.")
        
        # Check learning insights
        if memory_insights['learning_insights_count'] > 10:
            recommendations.append("Rich learning data available. Enable learning mode for optimized research strategies.")
        
        # Check overall quality
        if memory_insights['avg_project_quality'] > 0.7:
            recommendations.append("High-quality research patterns detected. Current methodology is working well.")
        elif memory_insights['avg_project_quality'] < 0.5:
            recommendations.append("Consider adjusting research methodology or quality thresholds to improve results.")
        
        return recommendations

# Example usage and testing
async def main():
    """Example usage of the Enhanced Prompt-Researcher Agent."""
    
    # Initialize the enhanced researcher
    researcher = EnhancedPromptResearcher("./data", "./config")
    
    # Conduct enhanced research
    print("🔍 Conducting enhanced research on AI agent frameworks...")
    results = await researcher.conduct_enhanced_research(
        query="AI agent frameworks Python machine learning",
        description="Comprehensive analysis of AI agent frameworks for Python ML applications",
        research_type="technology_analysis",
        use_learning=True,
        limit_per_source=8
    )
    
    print(f"\n📊 Research Results Summary:")
    print(f"Project ID: {results['project_id']}")
    print(f"Total Results: {results['total_results']}")
    print(f"High Quality Results: {results['high_quality_results']}")
    print(f"Learning Confidence: {results['recommendations_confidence']:.2f}")
    print(f"Dataset Path: {results['dataset_path']}")
    
    # Show top results
    print(f"\n🏆 Top Results:")
    for i, result in enumerate(results['results_summary']['top_results'][:3], 1):
        print(f"{i}. {result['title']} ({result['source']}) - Score: {result['quality_score']:.2f}")
    
    # Show insights
    print(f"\n💡 Key Insights:")
    for insight in results['insights'][:2]:
        print(f"- {insight['title']}: {insight['description']}")
    
    # Enrich the research
    print(f"\n🔄 Enriching research with additional sources...")
    enrichment = await researcher.enrich_existing_research(
        results['project_id'],
        additional_sources=['web'],
        new_query_variations=["Python AI agents", "machine learning agent frameworks"]
    )
    
    print(f"Added {enrichment['new_results_count']} new results")
    print(f"Total results now: {enrichment['total_results_count']}")
    
    # Get comprehensive insights
    print(f"\n📈 Research Insights:")
    insights = researcher.get_research_insights(results['project_id'])
    
    print(f"Memory Statistics:")
    print(f"- Total Projects: {insights['memory_insights']['total_projects']}")
    print(f"- Total Results: {insights['memory_insights']['total_results']}")
    print(f"- Average Quality: {insights['memory_insights']['avg_project_quality']:.2f}")
    
    if insights['project_specific']:
        print(f"\nProject Analysis:")
        proj_insights = insights['project_specific']
        print(f"- Average Quality: {proj_insights['avg_quality']:.2f}")
        print(f"- Most Productive Source: {proj_insights['source_distribution']['most_productive']}")
        print(f"- Recommendations: {len(proj_insights['recommendations'])}")

if __name__ == "__main__":
    asyncio.run(main())
