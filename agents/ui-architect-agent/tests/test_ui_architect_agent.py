#!/usr/bin/env python3
"""
Test Suite for UI-Architect-Agent

Comprehensive testing of the UI-Architect-Agent functionality including
prompt analysis, design recommendations, code generation, and accessibility auditing.

Author: Manus AI
Created: 2025-09-20
"""

import unittest
import json
import sys
import os
from unittest.mock import Mock, patch
import pandas as pd

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ui_architect_agent import UIArchitectAgent, DesignDimensions, DesignRecommendation

class TestUIArchitectAgent(unittest.TestCase):
    """Test cases for the UI-Architect-Agent."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.agent = UIArchitectAgent()
        
        # Sample test data
        self.sample_prompt = "I need to design a dashboard for a social media analytics platform"
        self.sample_refined_prompt = {
            "project_type": "dashboard",
            "target_audience": "marketing professionals",
            "platform": "web",
            "key_features": ["analytics", "charts", "filters", "reports"],
            "business_goals": ["increase user engagement", "improve data insights"],
            "design_style": "modern",
            "constraints": ["mobile responsive", "accessibility compliant"]
        }
        
    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertEqual(self.agent.name, "UI-Architect-Agent")
        self.assertEqual(self.agent.version, "1.0.0")
        self.assertIsInstance(self.agent.knowledge_base, pd.DataFrame)
        self.assertIsInstance(self.agent.conversation_history, list)
        self.assertIsInstance(self.agent.current_project_context, dict)
        
    def test_analyze_prompt_basic(self):
        """Test basic prompt analysis functionality."""
        analysis = self.agent.analyze_prompt(self.sample_prompt)
        
        # Check required fields are present
        self.assertIn("extracted_information", analysis)
        self.assertIn("missing_information", analysis)
        self.assertIn("clarifying_questions", analysis)
        self.assertIn("completeness_score", analysis)
        self.assertIn("ready_for_recommendations", analysis)
        
        # Check data types
        self.assertIsInstance(analysis["extracted_information"], dict)
        self.assertIsInstance(analysis["missing_information"], list)
        self.assertIsInstance(analysis["clarifying_questions"], list)
        self.assertIsInstance(analysis["completeness_score"], float)
        self.assertIsInstance(analysis["ready_for_recommendations"], bool)
        
    def test_extract_prompt_information(self):
        """Test information extraction from prompts."""
        info = self.agent._extract_prompt_information(self.sample_prompt)
        
        # Should detect dashboard project type
        self.assertEqual(info["project_type"], "dashboard")
        
        # Should detect some features
        self.assertIn("analytics", info["key_features"])
        
    def test_generate_clarifying_questions(self):
        """Test generation of clarifying questions."""
        missing_info = ["target_audience", "business_goals", "constraints"]
        questions = self.agent._generate_clarifying_questions(missing_info)
        
        self.assertIsInstance(questions, list)
        self.assertGreater(len(questions), 0)
        
        # Should include questions about missing information
        question_text = " ".join(questions).lower()
        self.assertIn("audience", question_text)
        
    def test_calculate_prompt_completeness(self):
        """Test prompt completeness calculation."""
        # Empty info should have low completeness
        empty_info = {
            "project_type": None,
            "target_audience": None,
            "platform": None,
            "key_features": [],
            "design_style": None,
            "constraints": [],
            "business_goals": [],
            "technical_requirements": []
        }
        
        completeness = self.agent._calculate_prompt_completeness(empty_info)
        self.assertEqual(completeness, 0.0)
        
        # Complete info should have high completeness
        complete_info = {
            "project_type": "dashboard",
            "target_audience": "marketers",
            "platform": "web",
            "key_features": ["analytics"],
            "design_style": "modern",
            "constraints": ["responsive"],
            "business_goals": ["engagement"],
            "technical_requirements": ["react"]
        }
        
        completeness = self.agent._calculate_prompt_completeness(complete_info)
        self.assertEqual(completeness, 1.0)
        
    def test_get_design_recommendations(self):
        """Test design recommendation generation."""
        recommendations = self.agent.get_design_recommendations(self.sample_refined_prompt)
        
        # Check structure
        self.assertIn("project_context", recommendations)
        self.assertIn("recommendations", recommendations)
        self.assertIn("predicted_scores", recommendations)
        self.assertIn("implementation_guide", recommendations)
        
        # Check recommendations list
        rec_list = recommendations["recommendations"]
        self.assertIsInstance(rec_list, list)
        self.assertGreater(len(rec_list), 0)
        
        # Check first recommendation structure
        if rec_list:
            first_rec = rec_list[0]
            self.assertIsInstance(first_rec, DesignRecommendation)
            self.assertIsInstance(first_rec.title, str)
            self.assertIsInstance(first_rec.confidence_score, float)
            self.assertIsInstance(first_rec.dimensions, DesignDimensions)
            
    def test_predict_design_scores(self):
        """Test design score prediction."""
        # Create sample recommendations
        sample_rec = DesignRecommendation(
            title="Test Recommendation",
            description="Test description",
            category="Test",
            sub_category="Test Sub",
            rationale="Test rationale",
            implementation_notes="Test notes",
            source_url="https://example.com",
            confidence_score=0.9,
            dimensions=DesignDimensions(
                sentiment=8.0, usability=9.0, aesthetics=7.5, value=8.5,
                accuracy=9.0, utility=8.5, form=8.0, function=8.5
            ),
            tags=["test"]
        )
        
        recommendations = [sample_rec]
        scores = self.agent._predict_design_scores(self.sample_refined_prompt, recommendations)
        
        self.assertIsInstance(scores, DesignDimensions)
        self.assertGreater(scores.usability, 0)
        self.assertLessEqual(scores.usability, 10)
        
    def test_generate_component_code_react(self):
        """Test React component code generation."""
        button_code = self.agent.generate_component_code("button", "react")
        
        self.assertIsInstance(button_code, str)
        self.assertIn("React", button_code)
        self.assertIn("Button", button_code)
        self.assertIn("interface", button_code)  # TypeScript interface
        
    def test_generate_component_code_invalid(self):
        """Test component code generation with invalid inputs."""
        # Invalid component type
        result = self.agent.generate_component_code("invalid_component", "react")
        self.assertIn("not supported", result)
        
        # Invalid framework
        result = self.agent.generate_component_code("button", "invalid_framework")
        self.assertIn("not supported", result)
        
    def test_audit_accessibility(self):
        """Test accessibility auditing functionality."""
        design_spec = {
            "colors": {
                "primary": "#007bff",
                "background": "#ffffff",
                "text": "#333333"
            },
            "navigation": {
                "keyboard_accessible": True
            },
            "images": {
                "alt_text_provided": True
            }
        }
        
        audit = self.agent.audit_accessibility(design_spec)
        
        # Check structure
        self.assertIn("overall_score", audit)
        self.assertIn("issues", audit)
        self.assertIn("recommendations", audit)
        self.assertIn("compliance_level", audit)
        
        # Check data types
        self.assertIsInstance(audit["overall_score"], float)
        self.assertIsInstance(audit["issues"], list)
        self.assertIsInstance(audit["compliance_level"], str)
        
    def test_suggest_dataviz_time_series(self):
        """Test data visualization suggestions for time series data."""
        data_description = "User engagement metrics over the past 12 months showing trends"
        suggestions = self.agent.suggest_dataviz(data_description)
        
        self.assertIn("primary_recommendation", suggestions)
        self.assertIn("alternative_options", suggestions)
        
        # Should recommend line chart for time series
        primary = suggestions["primary_recommendation"]
        self.assertIn("Line Chart", primary["type"])
        
    def test_suggest_dataviz_categorical(self):
        """Test data visualization suggestions for categorical data."""
        data_description = "Comparison of sales performance across different product categories"
        suggestions = self.agent.suggest_dataviz(data_description)
        
        primary = suggestions["primary_recommendation"]
        self.assertIn("Bar Chart", primary["type"])
        
    def test_suggest_dataviz_proportional(self):
        """Test data visualization suggestions for proportional data."""
        data_description = "Market share breakdown showing percentage of total revenue by region"
        suggestions = self.agent.suggest_dataviz(data_description)
        
        primary = suggestions["primary_recommendation"]
        self.assertIn("Pie Chart", primary["type"])
        
    def test_conversation_history(self):
        """Test conversation history tracking."""
        # Initially empty
        history = self.agent.get_conversation_history()
        initial_length = len(history)
        
        # Analyze a prompt
        self.agent.analyze_prompt(self.sample_prompt)
        
        # History should have one more entry
        history = self.agent.get_conversation_history()
        self.assertEqual(len(history), initial_length + 1)
        
        # Entry should have correct structure
        last_entry = history[-1]
        self.assertEqual(last_entry["type"], "prompt_analysis")
        self.assertIn("prompt", last_entry)
        self.assertIn("analysis", last_entry)
        
    def test_export_project_summary(self):
        """Test project summary export."""
        # Set up some context
        self.agent.current_project_context = self.sample_refined_prompt
        self.agent.analyze_prompt(self.sample_prompt)
        
        summary = self.agent.export_project_summary()
        
        # Check structure
        self.assertIn("agent_info", summary)
        self.assertIn("project_context", summary)
        self.assertIn("conversation_history", summary)
        self.assertIn("knowledge_base_stats", summary)
        
        # Check agent info
        agent_info = summary["agent_info"]
        self.assertEqual(agent_info["name"], "UI-Architect-Agent")
        self.assertEqual(agent_info["version"], "1.0.0")
        
    def test_design_dimensions_class(self):
        """Test DesignDimensions data class."""
        dimensions = DesignDimensions(
            sentiment=8.0, usability=9.0, aesthetics=7.5, value=8.5,
            accuracy=9.0, utility=8.5, form=8.0, function=8.5
        )
        
        # Test average calculation
        avg = dimensions.average_score()
        expected_avg = (8.0 + 9.0 + 7.5 + 8.5 + 9.0 + 8.5 + 8.0 + 8.5) / 8
        self.assertAlmostEqual(avg, expected_avg, places=2)
        
        # Test dictionary conversion
        dim_dict = dimensions.to_dict()
        self.assertIsInstance(dim_dict, dict)
        self.assertEqual(dim_dict["sentiment"], 8.0)
        self.assertEqual(dim_dict["usability"], 9.0)
        
    def test_find_relevant_principles(self):
        """Test finding relevant principles from knowledge base."""
        principles = self.agent._find_relevant_principles(self.sample_refined_prompt)
        
        self.assertIsInstance(principles, list)
        # Should find some principles even with sample data
        
        if principles:
            first_principle = principles[0]
            self.assertIn("relevance_score", first_principle)
            self.assertIsInstance(first_principle["relevance_score"], (int, float))
            
    def test_supported_frameworks_and_components(self):
        """Test that supported frameworks and components are properly defined."""
        self.assertIn("react", self.agent.supported_frameworks)
        self.assertIn("vue", self.agent.supported_frameworks)
        self.assertIn("button", self.agent.component_types)
        self.assertIn("modal", self.agent.component_types)
        
    def test_knowledge_base_loading(self):
        """Test knowledge base loading functionality."""
        # Test with non-existent path
        agent_with_invalid_path = UIArchitectAgent("/invalid/path/to/file.xlsx")
        self.assertIsInstance(agent_with_invalid_path.knowledge_base, pd.DataFrame)
        
        # Should fall back to sample data
        self.assertGreater(len(agent_with_invalid_path.knowledge_base), 0)

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.agent = UIArchitectAgent()
        
    def test_complete_design_workflow(self):
        """Test a complete design workflow from prompt to recommendations."""
        # Step 1: Analyze initial prompt
        initial_prompt = "I need to design a mobile app for fitness tracking"
        analysis = self.agent.analyze_prompt(initial_prompt)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn("clarifying_questions", analysis)
        
        # Step 2: Provide refined requirements
        refined_prompt = {
            "project_type": "mobile_app",
            "target_audience": "fitness enthusiasts",
            "platform": "mobile",
            "key_features": ["workout tracking", "progress charts", "social sharing"],
            "business_goals": ["user retention", "engagement"],
            "design_style": "modern minimalist",
            "constraints": ["iOS and Android", "offline capability"]
        }
        
        # Step 3: Get design recommendations
        recommendations = self.agent.get_design_recommendations(refined_prompt)
        
        self.assertIn("recommendations", recommendations)
        self.assertIn("predicted_scores", recommendations)
        
        # Step 4: Generate component code
        button_code = self.agent.generate_component_code("button", "react")
        self.assertIn("Button", button_code)
        
        # Step 5: Audit accessibility
        design_spec = {
            "colors": {"primary": "#007bff", "background": "#ffffff"},
            "navigation": {"keyboard_accessible": True}
        }
        audit = self.agent.audit_accessibility(design_spec)
        self.assertIn("overall_score", audit)
        
        # Step 6: Export summary
        summary = self.agent.export_project_summary()
        self.assertIn("agent_info", summary)
        self.assertGreater(len(self.agent.get_conversation_history()), 0)

if __name__ == "__main__":
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test cases
    test_suite.addTest(unittest.makeSuite(TestUIArchitectAgent))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"UI-Architect-Agent Test Results")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print(f"\n✅ All tests passed successfully!")
    else:
        print(f"\n❌ Some tests failed. Please review the output above.")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
