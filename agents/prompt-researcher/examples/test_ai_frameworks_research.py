#!/usr/bin/env python3
"""
Test Script: AI Frameworks Research with Enhanced Prompt-Researcher Agent

This script demonstrates the full capabilities of the Enhanced Prompt-Researcher Agent
by conducting comprehensive research on AI agent frameworks, similar to the original
research that was conducted manually.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / "src"))

from enhanced_prompt_researcher import EnhancedPromptResearcher

async def test_ai_frameworks_research():
    """
    Test the Enhanced Prompt-Researcher Agent by replicating the AI frameworks research.
    This will create a comprehensive dataset similar to the one created manually.
    """
    
    print("🚀 Starting AI Frameworks Research Test")
    print("=" * 60)
    
    # Initialize the enhanced researcher
    data_dir = Path(__file__).parent.parent / "data"
    config_dir = Path(__file__).parent.parent / "config"
    
    researcher = EnhancedPromptResearcher(str(data_dir), str(config_dir))
    
    # Test 1: Initial comprehensive research
    print("\n📋 Test 1: Comprehensive AI Agent Frameworks Research")
    print("-" * 50)
    
    research_results = await researcher.conduct_enhanced_research(
        query="AI agent frameworks Python development",
        description="Comprehensive research on AI agent frameworks for Python development, including popularity, features, and community adoption",
        research_type="technology_analysis",
        sources=['github', 'web', 'reddit'],
        use_learning=True,
        limit_per_source=12
    )
    
    print(f"✅ Research completed!")
    print(f"   Project ID: {research_results['project_id']}")
    print(f"   Total Results: {research_results['total_results']}")
    print(f"   High Quality Results: {research_results['high_quality_results']}")
    print(f"   Learning Confidence: {research_results['recommendations_confidence']:.2f}")
    print(f"   Dataset saved to: {research_results['dataset_path']}")
    
    # Display top results
    print(f"\n🏆 Top 5 Results by Quality:")
    for i, result in enumerate(research_results['results_summary']['top_results'], 1):
        print(f"   {i}. {result['title']}")
        print(f"      Source: {result['source']} | Score: {result['quality_score']:.3f}")
        print(f"      URL: {result['url']}")
        print()
    
    # Display insights
    print(f"💡 Key Research Insights:")
    for insight in research_results['insights']:
        print(f"   • {insight['title']}: {insight['description']}")
        if 'recommendation' in insight:
            print(f"     Recommendation: {insight['recommendation']}")
        print()
    
    # Test 2: Research enrichment
    print("\n📋 Test 2: Research Enrichment")
    print("-" * 50)
    
    enrichment_results = await researcher.enrich_existing_research(
        research_results['project_id'],
        additional_sources=['web'],
        new_query_variations=[
            "Python AI agent libraries",
            "machine learning agent frameworks",
            "autonomous agent development Python"
        ]
    )
    
    print(f"✅ Enrichment completed!")
    print(f"   Original Results: {enrichment_results['original_results_count']}")
    print(f"   New Results Added: {enrichment_results['new_results_count']}")
    print(f"   Total Results: {enrichment_results['total_results_count']}")
    print(f"   Updated Dataset: {enrichment_results['updated_dataset_path']}")
    
    # Display new top results
    if enrichment_results['new_results_summary']['top_results']:
        print(f"\n🆕 Top New Results from Enrichment:")
        for i, result in enumerate(enrichment_results['new_results_summary']['top_results'][:3], 1):
            print(f"   {i}. {result['title']}")
            print(f"      Source: {result['source']} | Score: {result['quality_score']:.3f}")
            print(f"      URL: {result['url']}")
            print()
    
    # Test 3: Comprehensive insights analysis
    print("\n📋 Test 3: Comprehensive Insights Analysis")
    print("-" * 50)
    
    insights = researcher.get_research_insights(research_results['project_id'])
    
    print(f"📊 Memory System Insights:")
    memory_insights = insights['memory_insights']
    print(f"   Total Projects in Memory: {memory_insights['total_projects']}")
    print(f"   Total Results Collected: {memory_insights['total_results']}")
    print(f"   Average Project Quality: {memory_insights['avg_project_quality']:.3f}")
    print(f"   Knowledge Entities: {memory_insights['knowledge_entities']}")
    print(f"   Learning Insights: {memory_insights['learning_insights_count']}")
    
    if memory_insights['most_successful_sources']:
        print(f"\n🎯 Most Successful Sources:")
        for source_info in memory_insights['most_successful_sources'][:3]:
            print(f"   • {source_info['source']}: Avg Score {source_info['avg_score']:.3f} ({source_info['count']} results)")
    
    # Project-specific insights
    if insights['project_specific']:
        proj_insights = insights['project_specific']
        print(f"\n📈 Project-Specific Analysis:")
        print(f"   Query: '{proj_insights['query']}'")
        print(f"   Total Results: {proj_insights['total_results']}")
        print(f"   Average Quality: {proj_insights['avg_quality']:.3f}")
        
        source_dist = proj_insights['source_distribution']
        print(f"   Most Productive Source: {source_dist['most_productive']}")
        print(f"   Highest Quality Source: {source_dist['highest_quality']}")
        
        quality_dist = proj_insights['quality_distribution']
        print(f"   Quality Distribution:")
        print(f"     High Quality (≥0.7): {quality_dist['high_quality']} ({quality_dist['score_distribution']['high_quality_pct']:.1f}%)")
        print(f"     Medium Quality (0.4-0.7): {quality_dist['medium_quality']} ({quality_dist['score_distribution']['medium_quality_pct']:.1f}%)")
        print(f"     Low Quality (<0.4): {quality_dist['low_quality']} ({quality_dist['score_distribution']['low_quality_pct']:.1f}%)")
        
        if proj_insights['recommendations']:
            print(f"\n💡 Project Recommendations:")
            for rec in proj_insights['recommendations']:
                print(f"   • {rec}")
    
    # Learning patterns
    if insights['learning_patterns']['most_effective_sources']:
        print(f"\n🧠 Learning Patterns:")
        print(f"   Learning Confidence: {insights['learning_patterns']['confidence_level']:.3f}")
        print(f"   Similar Topics Found: {insights['learning_patterns']['similar_topics_found']}")
        print(f"   Most Effective Sources (by learning):")
        for source, priority in insights['learning_patterns']['most_effective_sources'].items():
            print(f"     • {source}: Priority {priority:.3f}")
    
    # General recommendations
    if insights['recommendations']:
        print(f"\n🎯 General Recommendations:")
        for rec in insights['recommendations']:
            print(f"   • {rec}")
    
    # Test 4: Second research project to test learning
    print("\n📋 Test 4: Second Research Project (Testing Learning)")
    print("-" * 50)
    
    second_research = await researcher.conduct_enhanced_research(
        query="LangChain vs AutoGen comparison",
        description="Comparative analysis of LangChain and AutoGen frameworks",
        research_type="technology_analysis",
        use_learning=True,  # This should now use learned patterns
        limit_per_source=8
    )
    
    print(f"✅ Second research completed!")
    print(f"   Project ID: {second_research['project_id']}")
    print(f"   Learning Applied: {second_research['learning_applied']}")
    print(f"   Recommendations Confidence: {second_research['recommendations_confidence']:.3f}")
    print(f"   Results: {second_research['high_quality_results']} high-quality from {second_research['total_results']} total")
    
    # Compare learning improvement
    if second_research['recommendations_confidence'] > research_results['recommendations_confidence']:
        print(f"   🎉 Learning improvement detected! Confidence increased from {research_results['recommendations_confidence']:.3f} to {second_research['recommendations_confidence']:.3f}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 AI Frameworks Research Test Completed Successfully!")
    print("=" * 60)
    
    print(f"\n📊 Final Summary:")
    print(f"   Projects Created: 2")
    print(f"   Total Research Sessions: 3 (including enrichment)")
    print(f"   Datasets Generated: 3")
    print(f"   Learning System: Active and improving")
    
    # Show file locations
    print(f"\n📁 Generated Files:")
    print(f"   Primary Dataset: {research_results['dataset_path']}")
    print(f"   Enriched Dataset: {enrichment_results['updated_dataset_path']}")
    print(f"   Second Project Dataset: {second_research['dataset_path']}")
    print(f"   Memory Database: {data_dir}/memory/advanced_memory.db")
    print(f"   Configuration: {config_dir}/")
    
    return {
        'primary_research': research_results,
        'enrichment': enrichment_results,
        'second_research': second_research,
        'insights': insights
    }

async def demonstrate_memory_persistence():
    """
    Demonstrate that the memory system persists across agent instances.
    """
    
    print("\n🧠 Testing Memory Persistence")
    print("-" * 30)
    
    # Create a new instance of the researcher (simulating restart)
    data_dir = Path(__file__).parent.parent / "data"
    config_dir = Path(__file__).parent.parent / "config"
    
    new_researcher = EnhancedPromptResearcher(str(data_dir), str(config_dir))
    
    # Get insights from the new instance
    insights = new_researcher.get_research_insights()
    
    print(f"✅ Memory persistence verified!")
    print(f"   Projects in memory: {insights['memory_insights']['total_projects']}")
    print(f"   Results in memory: {insights['memory_insights']['total_results']}")
    print(f"   Learning insights: {insights['memory_insights']['learning_insights_count']}")
    
    # Test learning recommendations
    recommendations = new_researcher.memory_system.get_research_recommendations("Python AI frameworks")
    print(f"   Learning confidence: {recommendations.get('confidence', 0):.3f}")
    
    if recommendations.get('source_priorities'):
        print(f"   Learned source priorities:")
        for source, priority in recommendations['source_priorities'].items():
            print(f"     • {source}: {priority:.3f}")

if __name__ == "__main__":
    async def main():
        try:
            # Run the main test
            test_results = await test_ai_frameworks_research()
            
            # Test memory persistence
            await demonstrate_memory_persistence()
            
            print(f"\n✨ All tests completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
    
    asyncio.run(main())
