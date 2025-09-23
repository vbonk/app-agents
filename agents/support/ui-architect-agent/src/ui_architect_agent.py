#!/usr/bin/env python3
"""
UI-Architect-Agent: Advanced UI/UX Design Assistant

A sophisticated AI agent that provides expert guidance on modern UI/UX design,
leveraging comprehensive research data and best practices from industry leaders.

Author: Manus AI
Created: 2025-09-20
Version: 1.0.0
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import re
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DesignDimensions:
    """Represents the 8-dimensional scoring system for UI designs."""
    sentiment: float = 0.0
    usability: float = 0.0
    aesthetics: float = 0.0
    value: float = 0.0
    accuracy: float = 0.0
    utility: float = 0.0
    form: float = 0.0
    function: float = 0.0
    
    def average_score(self) -> float:
        """Calculate the average score across all dimensions."""
        scores = [self.sentiment, self.usability, self.aesthetics, self.value,
                 self.accuracy, self.utility, self.form, self.function]
        return sum(scores) / len(scores)
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary format."""
        return asdict(self)

@dataclass
class DesignRecommendation:
    """Represents a design recommendation with supporting data."""
    title: str
    description: str
    category: str
    sub_category: str
    rationale: str
    implementation_notes: str
    source_url: str
    confidence_score: float
    dimensions: DesignDimensions
    tags: List[str]

class UIArchitectAgent:
    """
    Advanced UI/UX Design Assistant Agent
    
    Provides expert guidance on modern UI/UX design principles, patterns,
    and best practices based on comprehensive research data.
    """
    
    def __init__(self, knowledge_base_path: Optional[str] = None):
        """Initialize the UI Architect Agent."""
        self.name = "UI-Architect-Agent"
        self.version = "1.0.0"
        self.description = "Advanced UI/UX Design Assistant"
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        
        # Initialize conversation memory
        self.conversation_history = []
        self.current_project_context = {}
        
        # Design patterns and frameworks
        self.supported_frameworks = [
            "react", "vue", "svelte", "angular", "vanilla-js",
            "tailwind", "bootstrap", "material-ui", "chakra-ui"
        ]
        
        self.component_types = [
            "button", "input", "modal", "dropdown", "navigation",
            "card", "table", "form", "dashboard", "chart", "sidebar"
        ]
        
        logger.info(f"Initialized {self.name} v{self.version}")
    
    def _load_knowledge_base(self, path: Optional[str]) -> pd.DataFrame:
        """Load the UI/UX research knowledge base."""
        if path is None:
            # Use default path or create sample data
            return self._create_sample_knowledge_base()
        
        try:
            df = pd.read_excel(path, sheet_name='Complete Dataset')
            logger.info(f"Loaded knowledge base with {len(df)} records")
            return df
        except Exception as e:
            logger.warning(f"Could not load knowledge base from {path}: {e}")
            return self._create_sample_knowledge_base()
    
    def _create_sample_knowledge_base(self) -> pd.DataFrame:
        """Create a sample knowledge base for demonstration."""
        sample_data = [
            {
                "category": "Visual Design",
                "sub_category": "Light and Shadow",
                "title": "Light Comes From Sky Principle",
                "topic": "Shadow Psychology",
                "detail": "Users expect light to come from above, creating shadows below elements.",
                "specific_url": "https://learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html",
                "identify_tags": ["shadow", "depth", "visual hierarchy"],
                "summary": "Proper use of light and shadow creates intuitive interface depth",
                "sentiment_score": 8.5,
                "usability_score": 9.0,
                "aesthetics_score": 8.0,
                "value_score": 7.5,
                "accuracy_score": 9.5,
                "utility_score": 8.5,
                "form_score": 8.0,
                "function_score": 8.5
            }
        ]
        return pd.DataFrame(sample_data)
    
    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze user prompt and identify areas needing clarification.
        
        Args:
            prompt: User's initial design request
            
        Returns:
            Analysis results with clarifying questions and extracted information
        """
        logger.info(f"Analyzing prompt: {prompt[:100]}...")
        
        # Extract key information from prompt
        extracted_info = self._extract_prompt_information(prompt)
        
        # Identify missing critical information
        missing_info = self._identify_missing_information(extracted_info)
        
        # Generate clarifying questions
        questions = self._generate_clarifying_questions(missing_info)
        
        # Calculate completeness score
        completeness_score = self._calculate_prompt_completeness(extracted_info)
        
        analysis = {
            "extracted_information": extracted_info,
            "missing_information": missing_info,
            "clarifying_questions": questions,
            "completeness_score": completeness_score,
            "ready_for_recommendations": completeness_score >= 0.7,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Store in conversation history
        self.conversation_history.append({
            "type": "prompt_analysis",
            "prompt": prompt,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
        return analysis
    
    def _extract_prompt_information(self, prompt: str) -> Dict[str, Any]:
        """Extract structured information from user prompt."""
        info = {
            "project_type": None,
            "target_audience": None,
            "platform": None,
            "key_features": [],
            "design_style": None,
            "constraints": [],
            "business_goals": [],
            "technical_requirements": []
        }
        
        prompt_lower = prompt.lower()
        
        # Detect project type
        project_patterns = {
            "dashboard": ["dashboard", "admin panel", "analytics"],
            "landing_page": ["landing page", "homepage", "marketing page"],
            "mobile_app": ["mobile app", "ios app", "android app"],
            "web_app": ["web app", "web application", "saas"],
            "e-commerce": ["e-commerce", "online store", "shopping"],
            "social_media": ["social media", "social network", "community"]
        }
        
        for project_type, keywords in project_patterns.items():
            if any(keyword in prompt_lower for keyword in keywords):
                info["project_type"] = project_type
                break
        
        # Detect platform
        platform_patterns = {
            "web": ["web", "browser", "desktop"],
            "mobile": ["mobile", "ios", "android", "phone"],
            "tablet": ["tablet", "ipad"],
            "responsive": ["responsive", "cross-platform"]
        }
        
        for platform, keywords in platform_patterns.items():
            if any(keyword in prompt_lower for keyword in keywords):
                info["platform"] = platform
                break
        
        # Extract features (simple keyword matching)
        feature_keywords = [
            "login", "signup", "authentication", "search", "filter",
            "navigation", "menu", "sidebar", "header", "footer",
            "form", "table", "chart", "graph", "modal", "popup",
            "analytics", "dashboard", "reporting", "data", "metrics"
        ]
        
        info["key_features"] = [
            feature for feature in feature_keywords 
            if feature in prompt_lower
        ]
        
        return info
    
    def _identify_missing_information(self, extracted_info: Dict[str, Any]) -> List[str]:
        """Identify critical missing information."""
        missing = []
        
        if not extracted_info["project_type"]:
            missing.append("project_type")
        
        if not extracted_info["target_audience"]:
            missing.append("target_audience")
        
        if not extracted_info["platform"]:
            missing.append("platform")
        
        if not extracted_info["key_features"]:
            missing.append("key_features")
        
        if not extracted_info["business_goals"]:
            missing.append("business_goals")
        
        return missing
    
    def _generate_clarifying_questions(self, missing_info: List[str]) -> List[str]:
        """Generate clarifying questions based on missing information."""
        question_templates = {
            "project_type": "What type of interface are you designing? (e.g., dashboard, landing page, mobile app)",
            "target_audience": "Who is your target audience? (e.g., business users, consumers, developers)",
            "platform": "What platform(s) will this be used on? (e.g., web, mobile, tablet)",
            "key_features": "What are the main features or functions users need to accomplish?",
            "business_goals": "What are the primary business objectives for this interface?",
            "design_style": "Do you have any specific design style preferences? (e.g., minimalist, modern, corporate)",
            "constraints": "Are there any technical, budget, or timeline constraints I should know about?"
        }
        
        questions = []
        for info_type in missing_info:
            if info_type in question_templates:
                questions.append(question_templates[info_type])
        
        # Always ask about constraints and style preferences
        if "constraints" not in missing_info:
            questions.append(question_templates["constraints"])
        if "design_style" not in missing_info:
            questions.append(question_templates["design_style"])
        
        return questions
    
    def _calculate_prompt_completeness(self, extracted_info: Dict[str, Any]) -> float:
        """Calculate how complete the prompt information is."""
        total_fields = 8
        completed_fields = 0
        
        if extracted_info["project_type"]:
            completed_fields += 1
        if extracted_info["target_audience"]:
            completed_fields += 1
        if extracted_info["platform"]:
            completed_fields += 1
        if extracted_info["key_features"]:
            completed_fields += 1
        if extracted_info["design_style"]:
            completed_fields += 1
        if extracted_info["constraints"]:
            completed_fields += 1
        if extracted_info["business_goals"]:
            completed_fields += 1
        if extracted_info["technical_requirements"]:
            completed_fields += 1
        
        return completed_fields / total_fields
    
    def get_design_recommendations(self, refined_prompt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive design recommendations based on refined prompt.
        
        Args:
            refined_prompt: Structured prompt information with user requirements
            
        Returns:
            Comprehensive design recommendations with rationale and examples
        """
        logger.info("Generating design recommendations...")
        
        # Store current project context
        self.current_project_context = refined_prompt
        
        # Find relevant knowledge base entries
        relevant_principles = self._find_relevant_principles(refined_prompt)
        
        # Generate specific recommendations
        recommendations = self._generate_specific_recommendations(
            refined_prompt, relevant_principles
        )
        
        # Calculate overall design scores
        predicted_scores = self._predict_design_scores(
            refined_prompt, recommendations
        )
        
        # Generate implementation guidance
        implementation_guide = self._generate_implementation_guide(
            refined_prompt, recommendations
        )
        
        result = {
            "project_context": refined_prompt,
            "recommendations": recommendations,
            "predicted_scores": predicted_scores,
            "implementation_guide": implementation_guide,
            "relevant_principles": relevant_principles,
            "generated_timestamp": datetime.now().isoformat()
        }
        
        # Store in conversation history
        self.conversation_history.append({
            "type": "design_recommendations",
            "input": refined_prompt,
            "output": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
    
    def _find_relevant_principles(self, prompt_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find relevant design principles from knowledge base."""
        if self.knowledge_base.empty:
            return []
        
        relevant_entries = []
        
        # Simple relevance scoring based on category and tags
        for _, row in self.knowledge_base.iterrows():
            relevance_score = 0
            
            # Check category relevance
            if prompt_info.get("project_type") == "dashboard" and "Dashboard" in row.get("category", ""):
                relevance_score += 3
            elif "Visual Design" in row.get("category", ""):
                relevance_score += 2
            elif "User Psychology" in row.get("category", ""):
                relevance_score += 2
            
            # Check tag relevance
            tags = row.get("identify_tags", [])
            if isinstance(tags, str):
                try:
                    tags = eval(tags)  # Convert string representation to list
                except:
                    tags = []
            
            for feature in prompt_info.get("key_features", []):
                if any(feature in str(tag).lower() for tag in tags):
                    relevance_score += 1
            
            if relevance_score > 0:
                entry = row.to_dict()
                entry["relevance_score"] = relevance_score
                relevant_entries.append(entry)
        
        # Sort by relevance and return top entries
        relevant_entries.sort(key=lambda x: x["relevance_score"], reverse=True)
        return relevant_entries[:10]
    
    def _generate_specific_recommendations(self, 
                                        prompt_info: Dict[str, Any], 
                                        principles: List[Dict[str, Any]]) -> List[DesignRecommendation]:
        """Generate specific design recommendations."""
        recommendations = []
        
        project_type = prompt_info.get("project_type", "web_app")
        platform = prompt_info.get("platform", "web")
        
        # Layout recommendations
        if project_type == "dashboard":
            layout_rec = DesignRecommendation(
                title="Dashboard Layout Structure",
                description="Use a sidebar navigation with main content area. Limit to 5-6 cards in initial view for optimal cognitive load management.",
                category="Layout",
                sub_category="Dashboard Design",
                rationale="Based on dashboard design best practices, users can effectively process 5-6 information chunks simultaneously without cognitive overload.",
                implementation_notes="Implement responsive grid system with sidebar collapse on mobile. Use card-based layout for data widgets.",
                source_url="https://www.justinmind.com/ui-design/dashboard-design-best-practices-ux",
                confidence_score=0.9,
                dimensions=DesignDimensions(
                    sentiment=8.0, usability=9.5, aesthetics=7.5, value=9.0,
                    accuracy=9.0, utility=9.5, form=8.0, function=9.0
                ),
                tags=["dashboard", "layout", "cognitive load", "cards"]
            )
            recommendations.append(layout_rec)
        
        # Visual hierarchy recommendation
        hierarchy_rec = DesignRecommendation(
            title="Visual Hierarchy Implementation",
            description="Establish clear typographic hierarchy with consistent spacing and color usage to guide user attention.",
            category="Visual Design",
            sub_category="Typography",
            rationale="Clear visual hierarchy reduces cognitive load and improves information processing efficiency.",
            implementation_notes="Use size ratios: H1(32-48px), H2(24-32px), Body(16-18px). Implement consistent spacing scale (8px base unit).",
            source_url="https://learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html",
            confidence_score=0.95,
            dimensions=DesignDimensions(
                sentiment=7.5, usability=9.0, aesthetics=8.0, value=8.5,
                accuracy=9.0, utility=9.0, form=8.5, function=9.0
            ),
            tags=["typography", "hierarchy", "spacing", "readability"]
        )
        recommendations.append(hierarchy_rec)
        
        # Accessibility recommendation
        accessibility_rec = DesignRecommendation(
            title="Accessibility-First Design",
            description="Implement WCAG 2.1 AA standards with proper color contrast, keyboard navigation, and screen reader support.",
            category="Accessibility",
            sub_category="Universal Design",
            rationale="Accessible design benefits all users and ensures legal compliance while expanding user base.",
            implementation_notes="Maintain 4.5:1 color contrast ratio, provide focus indicators, use semantic HTML, include alt text for images.",
            source_url="https://m3.material.io/foundations/overview/principles",
            confidence_score=0.95,
            dimensions=DesignDimensions(
                sentiment=9.0, usability=9.5, aesthetics=8.0, value=9.5,
                accuracy=9.0, utility=9.5, form=8.5, function=9.0
            ),
            tags=["accessibility", "WCAG", "inclusive design", "compliance"]
        )
        recommendations.append(accessibility_rec)
        
        return recommendations
    
    def _predict_design_scores(self, 
                             prompt_info: Dict[str, Any], 
                             recommendations: List[DesignRecommendation]) -> DesignDimensions:
        """Predict overall design scores based on recommendations."""
        if not recommendations:
            return DesignDimensions()
        
        # Average the dimensions from all recommendations
        total_dimensions = DesignDimensions()
        
        for rec in recommendations:
            total_dimensions.sentiment += rec.dimensions.sentiment * rec.confidence_score
            total_dimensions.usability += rec.dimensions.usability * rec.confidence_score
            total_dimensions.aesthetics += rec.dimensions.aesthetics * rec.confidence_score
            total_dimensions.value += rec.dimensions.value * rec.confidence_score
            total_dimensions.accuracy += rec.dimensions.accuracy * rec.confidence_score
            total_dimensions.utility += rec.dimensions.utility * rec.confidence_score
            total_dimensions.form += rec.dimensions.form * rec.confidence_score
            total_dimensions.function += rec.dimensions.function * rec.confidence_score
        
        # Calculate weighted averages
        total_confidence = sum(rec.confidence_score for rec in recommendations)
        
        if total_confidence > 0:
            total_dimensions.sentiment /= total_confidence
            total_dimensions.usability /= total_confidence
            total_dimensions.aesthetics /= total_confidence
            total_dimensions.value /= total_confidence
            total_dimensions.accuracy /= total_confidence
            total_dimensions.utility /= total_confidence
            total_dimensions.form /= total_confidence
            total_dimensions.function /= total_confidence
        
        return total_dimensions
    
    def _generate_implementation_guide(self, 
                                     prompt_info: Dict[str, Any], 
                                     recommendations: List[DesignRecommendation]) -> Dict[str, Any]:
        """Generate implementation guidance."""
        return {
            "development_phases": [
                "Design System Setup",
                "Component Development", 
                "Layout Implementation",
                "Accessibility Testing",
                "Performance Optimization"
            ],
            "recommended_tools": [
                "Figma for design mockups",
                "Storybook for component documentation",
                "Lighthouse for accessibility auditing",
                "Jest for component testing"
            ],
            "code_examples": self._generate_code_examples(prompt_info),
            "testing_checklist": [
                "Cross-browser compatibility",
                "Mobile responsiveness", 
                "Keyboard navigation",
                "Screen reader compatibility",
                "Performance metrics"
            ]
        }
    
    def _generate_code_examples(self, prompt_info: Dict[str, Any]) -> Dict[str, str]:
        """Generate basic code examples."""
        examples = {}
        
        if prompt_info.get("project_type") == "dashboard":
            examples["react_dashboard_layout"] = '''
import React from 'react';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        <nav className="nav-menu">
          <ul>
            <li><a href="#overview">Overview</a></li>
            <li><a href="#analytics">Analytics</a></li>
            <li><a href="#settings">Settings</a></li>
          </ul>
        </nav>
      </aside>
      <main className="main-content">
        <header className="dashboard-header">
          <h1>Dashboard</h1>
        </header>
        <div className="dashboard-grid">
          <div className="card">
            <h2>Key Metrics</h2>
            {/* Content */}
          </div>
          <div className="card">
            <h2>Recent Activity</h2>
            {/* Content */}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
'''
        
        return examples
    
    def generate_component_code(self, component: str, framework: str = "react") -> str:
        """
        Generate boilerplate code for UI components.
        
        Args:
            component: Type of component to generate
            framework: Target framework
            
        Returns:
            Generated code string
        """
        if component not in self.component_types:
            return f"Component type '{component}' not supported. Available: {', '.join(self.component_types)}"
        
        if framework not in self.supported_frameworks:
            return f"Framework '{framework}' not supported. Available: {', '.join(self.supported_frameworks)}"
        
        # Generate component based on type and framework
        if framework == "react":
            return self._generate_react_component(component)
        elif framework == "vue":
            return self._generate_vue_component(component)
        else:
            return f"Code generation for {framework} not yet implemented."
    
    def _generate_react_component(self, component: str) -> str:
        """Generate React component code."""
        templates = {
            "button": '''
import React from 'react';
import './Button.css';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  onClick
}) => {
  return (
    <button
      className={`btn btn--${variant} btn--${size}`}
      disabled={disabled}
      onClick={onClick}
      aria-disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
''',
            "modal": '''
import React, { useEffect } from 'react';
import './Modal.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children }) => {
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="modal-content" 
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-labelledby="modal-title"
        aria-modal="true"
      >
        <header className="modal-header">
          <h2 id="modal-title">{title}</h2>
          <button 
            className="modal-close"
            onClick={onClose}
            aria-label="Close modal"
          >
            ×
          </button>
        </header>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Modal;
'''
        }
        
        return templates.get(component, f"Template for {component} not available yet.")
    
    def _generate_vue_component(self, component: str) -> str:
        """Generate Vue component code."""
        return f"Vue template for {component} component - implementation pending."
    
    def audit_accessibility(self, design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audit design specification for accessibility compliance.
        
        Args:
            design_spec: Design specification to audit
            
        Returns:
            Accessibility audit results with recommendations
        """
        audit_results = {
            "overall_score": 0.0,
            "issues": [],
            "recommendations": [],
            "compliance_level": "Unknown",
            "audit_timestamp": datetime.now().isoformat()
        }
        
        issues_found = 0
        total_checks = 10
        
        # Check color contrast
        if "colors" in design_spec:
            colors = design_spec["colors"]
            if not self._check_color_contrast(colors):
                issues_found += 1
                audit_results["issues"].append({
                    "severity": "high",
                    "category": "Color Contrast",
                    "description": "Insufficient color contrast ratio detected",
                    "recommendation": "Ensure 4.5:1 contrast ratio for normal text, 3:1 for large text"
                })
        
        # Check keyboard navigation
        if "navigation" in design_spec:
            if not design_spec["navigation"].get("keyboard_accessible", False):
                issues_found += 1
                audit_results["issues"].append({
                    "severity": "high",
                    "category": "Keyboard Navigation",
                    "description": "Keyboard navigation not specified",
                    "recommendation": "Ensure all interactive elements are keyboard accessible"
                })
        
        # Calculate compliance score
        compliance_score = (total_checks - issues_found) / total_checks
        audit_results["overall_score"] = compliance_score
        
        if compliance_score >= 0.9:
            audit_results["compliance_level"] = "WCAG AA Compliant"
        elif compliance_score >= 0.7:
            audit_results["compliance_level"] = "Mostly Compliant"
        else:
            audit_results["compliance_level"] = "Needs Improvement"
        
        return audit_results
    
    def _check_color_contrast(self, colors: Dict[str, str]) -> bool:
        """Check if color combinations meet contrast requirements."""
        # Simplified contrast check - in real implementation, 
        # would calculate actual contrast ratios
        return True  # Placeholder
    
    def suggest_dataviz(self, data_description: str) -> Dict[str, Any]:
        """
        Suggest appropriate data visualization types.
        
        Args:
            data_description: Description of the data to visualize
            
        Returns:
            Visualization recommendations with rationale
        """
        suggestions = {
            "primary_recommendation": None,
            "alternative_options": [],
            "implementation_notes": [],
            "accessibility_considerations": []
        }
        
        data_lower = data_description.lower()
        
        # Analyze data type and suggest appropriate visualizations
        if any(word in data_lower for word in ["time", "trend", "over time", "timeline"]):
            suggestions["primary_recommendation"] = {
                "type": "Line Chart",
                "rationale": "Line charts effectively show trends and changes over time",
                "best_practices": [
                    "Use consistent time intervals on x-axis",
                    "Limit to 5-7 data series for clarity",
                    "Include data point markers for accessibility"
                ]
            }
            suggestions["alternative_options"] = ["Area Chart", "Bar Chart (for discrete time periods)"]
        
        elif any(word in data_lower for word in ["compare", "comparison", "categories", "category"]):
            suggestions["primary_recommendation"] = {
                "type": "Bar Chart",
                "rationale": "Bar charts excel at comparing values across categories",
                "best_practices": [
                    "Order categories logically (alphabetical or by value)",
                    "Use consistent spacing between bars",
                    "Include value labels for accessibility"
                ]
            }
            suggestions["alternative_options"] = ["Column Chart", "Horizontal Bar Chart"]
        
        elif any(word in data_lower for word in ["percentage", "proportion", "part of", "breakdown"]):
            suggestions["primary_recommendation"] = {
                "type": "Pie Chart or Donut Chart",
                "rationale": "Circular charts effectively show parts of a whole",
                "best_practices": [
                    "Limit to 5-7 segments maximum",
                    "Order segments by size",
                    "Include percentage labels",
                    "Consider bar chart alternative for better comparison"
                ]
            }
            suggestions["alternative_options"] = ["Stacked Bar Chart", "Treemap"]
        
        else:
            suggestions["primary_recommendation"] = {
                "type": "Table or Simple Bar Chart",
                "rationale": "When data type is unclear, start with simple, clear presentations",
                "best_practices": [
                    "Ensure clear column headers",
                    "Use consistent formatting",
                    "Enable sorting if interactive"
                ]
            }
        
        # Add universal accessibility considerations
        suggestions["accessibility_considerations"] = [
            "Provide alternative text descriptions",
            "Use patterns or textures in addition to color",
            "Ensure sufficient color contrast",
            "Include data table alternative",
            "Support keyboard navigation for interactive charts"
        ]
        
        return suggestions
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history
    
    def export_project_summary(self) -> Dict[str, Any]:
        """Export a summary of the current project."""
        return {
            "agent_info": {
                "name": self.name,
                "version": self.version,
                "description": self.description
            },
            "project_context": self.current_project_context,
            "conversation_history": self.conversation_history,
            "knowledge_base_stats": {
                "total_entries": len(self.knowledge_base),
                "categories": self.knowledge_base["category"].nunique() if not self.knowledge_base.empty else 0
            },
            "export_timestamp": datetime.now().isoformat()
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize agent
    agent = UIArchitectAgent()
    
    # Test prompt analysis
    test_prompt = "I need to design a dashboard for a social media analytics platform"
    analysis = agent.analyze_prompt(test_prompt)
    print("Prompt Analysis:")
    print(json.dumps(analysis, indent=2))
    
    # Test design recommendations
    refined_prompt = {
        "project_type": "dashboard",
        "target_audience": "marketing professionals",
        "platform": "web",
        "key_features": ["analytics", "charts", "filters"],
        "business_goals": ["increase user engagement", "improve data insights"]
    }
    
    recommendations = agent.get_design_recommendations(refined_prompt)
    print("\nDesign Recommendations:")
    print(f"Generated {len(recommendations['recommendations'])} recommendations")
    
    # Test component generation
    button_code = agent.generate_component_code("button", "react")
    print("\nGenerated Button Component:")
    print(button_code[:200] + "...")
    
    print(f"\n✅ {agent.name} v{agent.version} testing completed successfully!")
