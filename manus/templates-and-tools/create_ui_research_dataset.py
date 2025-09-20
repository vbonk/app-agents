#!/usr/bin/env python3
"""
UI/UX Research Dataset Generator

Creates a comprehensive spreadsheet dataset of UI/UX design principles, patterns,
and best practices for training the UI-Architect-Agent.

Author: Manus AI
Created: 2025-09-20
"""

import pandas as pd
import json
from datetime import datetime

def create_ui_research_dataset():
    """Create comprehensive UI/UX research dataset with multiple dimensions."""
    
    # Define the comprehensive dataset structure
    dataset = []
    
    # Visual Design Principles
    visual_design_data = [
        {
            "category": "Visual Design",
            "sub_category": "Light and Shadow",
            "title": "Light Comes From Sky Principle",
            "topic": "Shadow Psychology",
            "detail": "Users expect light to come from above, creating shadows below elements. Inset elements (text fields, pressed buttons) appear recessed, while outset elements (buttons, cards) appear raised. This creates intuitive depth perception.",
            "specific_url": "https://learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html",
            "identify_tags": ["shadow", "depth", "visual hierarchy", "skeuomorphism", "flat design"],
            "summary": "Proper use of light and shadow creates intuitive interface depth and hierarchy",
            "raw_data": "Inset: text fields, pressed buttons, slider tracks, checkboxes. Outset: unpressed buttons, cards, dropdowns, popups",
            "sentiment_score": 8.5,
            "usability_score": 9.0,
            "aesthetics_score": 8.0,
            "value_score": 7.5,
            "accuracy_score": 9.5,
            "utility_score": 8.5,
            "form_score": 8.0,
            "function_score": 8.5
        },
        {
            "category": "Visual Design",
            "sub_category": "Color Theory",
            "title": "Material Design Color System",
            "topic": "Color Psychology and Hierarchy",
            "detail": "Higher surfaces are brighter to simulate light reflection. Color conveys elevation and importance. Strategic use of color creates visual hierarchy and guides user attention through interfaces.",
            "specific_url": "https://m3.material.io/foundations",
            "identify_tags": ["color theory", "material design", "hierarchy", "elevation", "psychology"],
            "summary": "Color systems create consistent visual hierarchy and emotional responses",
            "raw_data": "Primary colors for main actions, secondary for supporting actions, surface colors indicate elevation levels",
            "sentiment_score": 8.0,
            "usability_score": 8.5,
            "aesthetics_score": 9.0,
            "value_score": 8.0,
            "accuracy_score": 8.5,
            "utility_score": 8.0,
            "form_score": 9.0,
            "function_score": 7.5
        },
        {
            "category": "Visual Design",
            "sub_category": "Typography",
            "title": "Typographic Hierarchy",
            "topic": "Information Architecture",
            "detail": "Clear typographic hierarchy guides users through content. Font size, weight, and spacing create scannable content structure. Consistent typography improves readability and comprehension.",
            "specific_url": "https://learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html",
            "identify_tags": ["typography", "hierarchy", "readability", "information architecture"],
            "summary": "Typographic hierarchy creates clear information structure and improves content comprehension",
            "raw_data": "H1: 32-48px, H2: 24-32px, H3: 20-24px, Body: 16-18px, Caption: 12-14px",
            "sentiment_score": 7.5,
            "usability_score": 9.0,
            "aesthetics_score": 8.0,
            "value_score": 8.5,
            "accuracy_score": 9.0,
            "utility_score": 9.0,
            "form_score": 8.5,
            "function_score": 9.0
        }
    ]
    
    # Dashboard Design Patterns
    dashboard_data = [
        {
            "category": "Dashboard Design",
            "sub_category": "Operational Dashboards",
            "title": "Real-time Status Display",
            "topic": "Current State Visualization",
            "detail": "Show critical time-relevant information with most important data at top-left. Focus on snapshot overview rather than detailed analysis. Use minimal graphical elements for quick comprehension.",
            "specific_url": "https://www.justinmind.com/ui-design/dashboard-design-best-practices-ux",
            "identify_tags": ["dashboard", "real-time", "operational", "status", "overview"],
            "summary": "Operational dashboards provide immediate status overview with critical information prioritized",
            "raw_data": "5-6 cards maximum, single screen approach, top-left priority placement",
            "sentiment_score": 8.0,
            "usability_score": 9.5,
            "aesthetics_score": 7.5,
            "value_score": 9.0,
            "accuracy_score": 9.0,
            "utility_score": 9.5,
            "form_score": 8.0,
            "function_score": 9.0
        },
        {
            "category": "Dashboard Design",
            "sub_category": "Analytical Dashboards",
            "title": "Performance Analysis Interface",
            "topic": "Data-Centric Visualization",
            "detail": "Present key datasets against previous performance. Data-centric approach with multiple relevant views. Lead with key metrics front and center, minimize decorative elements.",
            "specific_url": "https://www.justinmind.com/ui-design/dashboard-design-best-practices-ux",
            "identify_tags": ["analytics", "performance", "data visualization", "trends", "comparison"],
            "summary": "Analytical dashboards focus on data trends and performance comparison with minimal decoration",
            "raw_data": "Multiple data views, historical comparison, key metrics prominence, minimal graphics",
            "sentiment_score": 7.5,
            "usability_score": 8.5,
            "aesthetics_score": 7.0,
            "value_score": 9.5,
            "accuracy_score": 9.5,
            "utility_score": 9.0,
            "form_score": 7.5,
            "function_score": 9.0
        },
        {
            "category": "Dashboard Design",
            "sub_category": "Strategic Dashboards",
            "title": "KPI Tracking Interface",
            "topic": "Goal-Oriented Metrics",
            "detail": "Focus exclusively on key performance indicators and strategic goals. Clean presentation with goal-oriented metrics. Avoid information overload by showing only strategic-level data.",
            "specific_url": "https://www.justinmind.com/ui-design/dashboard-design-best-practices-ux",
            "identify_tags": ["KPI", "strategic", "goals", "metrics", "executive"],
            "summary": "Strategic dashboards track high-level KPIs with clean, goal-focused presentation",
            "raw_data": "KPI-only focus, strategic goals tracking, executive-level metrics, clean presentation",
            "sentiment_score": 8.0,
            "usability_score": 8.0,
            "aesthetics_score": 8.5,
            "value_score": 9.0,
            "accuracy_score": 9.0,
            "utility_score": 8.5,
            "form_score": 8.5,
            "function_score": 8.5
        }
    ]
    
    # Enterprise UX Patterns
    enterprise_data = [
        {
            "category": "Enterprise UX",
            "sub_category": "Navigation Patterns",
            "title": "Hierarchical Information Architecture",
            "topic": "Complex System Navigation",
            "detail": "Organize features into logical categories with clear hierarchies. Provide comprehensive sidebar navigation while maintaining visual clarity. Enable contextual switching between different user scopes.",
            "specific_url": "https://vercel.com/docs/dashboard-features",
            "identify_tags": ["navigation", "hierarchy", "enterprise", "sidebar", "context switching"],
            "summary": "Enterprise navigation requires clear hierarchies and contextual scope management",
            "raw_data": "Sidebar categories: API, Build & Deploy, CDN, Collaboration, Compute. Scope selector for team/personal context",
            "sentiment_score": 7.5,
            "usability_score": 9.0,
            "aesthetics_score": 7.5,
            "value_score": 9.0,
            "accuracy_score": 8.5,
            "utility_score": 9.5,
            "form_score": 8.0,
            "function_score": 9.0
        },
        {
            "category": "Enterprise UX",
            "sub_category": "Search and Discovery",
            "title": "Multi-Modal Search Systems",
            "topic": "Information Retrieval",
            "detail": "Implement global search with keyboard shortcuts (⌘K). Provide contextual results spanning multiple content types. Enable rapid navigation for power users while remaining discoverable for new users.",
            "specific_url": "https://vercel.com/docs/dashboard-features",
            "identify_tags": ["search", "keyboard shortcuts", "power users", "discovery", "navigation"],
            "summary": "Enterprise search systems balance power user efficiency with new user discoverability",
            "raw_data": "Global search: teams, projects, deployments, pages, settings. Keyboard shortcut: ⌘K/Ctrl+K",
            "sentiment_score": 8.5,
            "usability_score": 9.0,
            "aesthetics_score": 8.0,
            "value_score": 9.0,
            "accuracy_score": 9.0,
            "utility_score": 9.5,
            "form_score": 8.0,
            "function_score": 9.0
        },
        {
            "category": "Enterprise UX",
            "sub_category": "Progressive Disclosure",
            "title": "Layered Information Architecture",
            "topic": "Complexity Management",
            "detail": "Start with high-level overview and provide easy paths to increase granularity. Use card-based layouts with both overview and detailed views. Balance accessibility with comprehensive functionality.",
            "specific_url": "https://vercel.com/docs/dashboard-features",
            "identify_tags": ["progressive disclosure", "information architecture", "complexity", "layered design"],
            "summary": "Progressive disclosure manages complexity by revealing information in appropriate layers",
            "raw_data": "Card/list view toggle, recent previews panel, drill-down to deployment details",
            "sentiment_score": 8.0,
            "usability_score": 9.0,
            "aesthetics_score": 8.0,
            "value_score": 8.5,
            "accuracy_score": 8.5,
            "utility_score": 9.0,
            "form_score": 8.0,
            "function_score": 8.5
        }
    ]
    
    # Accessibility and Inclusive Design
    accessibility_data = [
        {
            "category": "Accessibility",
            "sub_category": "Universal Design",
            "title": "Inclusive Interface Principles",
            "topic": "Diverse Ability Support",
            "detail": "Design enables users with diverse abilities to navigate, understand, and enjoy interfaces. Accessibility benefits all users, not just those with specific needs. Build accessibility into design foundation rather than as afterthought.",
            "specific_url": "https://m3.material.io/foundations/overview/principles",
            "identify_tags": ["accessibility", "inclusive design", "universal design", "diverse abilities"],
            "summary": "Inclusive design principles ensure interfaces work for users with diverse abilities and needs",
            "raw_data": "WCAG compliance, screen reader support, keyboard navigation, color contrast ratios",
            "sentiment_score": 9.0,
            "usability_score": 9.5,
            "aesthetics_score": 8.0,
            "value_score": 9.5,
            "accuracy_score": 9.0,
            "utility_score": 9.5,
            "form_score": 8.5,
            "function_score": 9.0
        },
        {
            "category": "Accessibility",
            "sub_category": "Assistive Technology",
            "title": "Screen Reader Optimization",
            "topic": "Technology Integration",
            "detail": "Ensure interfaces work effectively with screen readers, voice control, and other assistive technologies. Provide proper semantic markup and alternative text. Design for keyboard-only navigation.",
            "specific_url": "https://m3.material.io/foundations/overview/principles",
            "identify_tags": ["screen readers", "assistive technology", "semantic markup", "keyboard navigation"],
            "summary": "Assistive technology integration ensures interfaces work with diverse interaction methods",
            "raw_data": "ARIA labels, semantic HTML, keyboard focus indicators, alternative text for images",
            "sentiment_score": 8.5,
            "usability_score": 9.5,
            "aesthetics_score": 7.5,
            "value_score": 9.0,
            "accuracy_score": 9.5,
            "utility_score": 9.5,
            "form_score": 8.0,
            "function_score": 9.5
        }
    ]
    
    # User Psychology and Cognitive Principles
    psychology_data = [
        {
            "category": "User Psychology",
            "sub_category": "Cognitive Load",
            "title": "Information Processing Limits",
            "topic": "Memory and Attention",
            "detail": "People can hold approximately 7 chunks of information in short-term memory. Present information in meaningful chunks. Reduce extraneous cognitive load to improve usability. Design for human cognitive limitations.",
            "specific_url": "https://www.nngroup.com/articles/psychology-study-guide/",
            "identify_tags": ["cognitive load", "memory limits", "information chunking", "attention"],
            "summary": "Understanding cognitive limitations enables design that works with human mental capacity",
            "raw_data": "7±2 rule for information chunks, progressive disclosure, clear visual hierarchy",
            "sentiment_score": 8.0,
            "usability_score": 9.5,
            "aesthetics_score": 7.5,
            "value_score": 9.0,
            "accuracy_score": 9.5,
            "utility_score": 9.0,
            "form_score": 8.0,
            "function_score": 9.0
        },
        {
            "category": "User Psychology",
            "sub_category": "Mental Models",
            "title": "User Expectation Alignment",
            "topic": "Interaction Patterns",
            "detail": "How people think something works influences how they interact with it. Align interfaces with existing mental models rather than forcing new learning. Leverage familiar patterns and conventions.",
            "specific_url": "https://www.nngroup.com/articles/psychology-study-guide/",
            "identify_tags": ["mental models", "user expectations", "interaction patterns", "conventions"],
            "summary": "Successful interfaces align with users' existing mental frameworks and expectations",
            "raw_data": "Familiar interaction patterns, conventional UI elements, predictable behavior",
            "sentiment_score": 8.5,
            "usability_score": 9.0,
            "aesthetics_score": 8.0,
            "value_score": 8.5,
            "accuracy_score": 9.0,
            "utility_score": 9.0,
            "form_score": 8.0,
            "function_score": 9.0
        },
        {
            "category": "User Psychology",
            "sub_category": "Interaction Cost",
            "title": "Effort Minimization Principle",
            "topic": "User Efficiency",
            "detail": "Total resources required (mental and physical) for any interaction constitute interaction cost. Higher costs reduce likelihood of action completion. Streamline workflows and minimize friction.",
            "specific_url": "https://www.nngroup.com/articles/psychology-study-guide/",
            "identify_tags": ["interaction cost", "user effort", "workflow optimization", "friction reduction"],
            "summary": "Minimizing interaction cost increases user engagement and task completion rates",
            "raw_data": "Reduced clicks, simplified forms, clear pathways, minimal cognitive overhead",
            "sentiment_score": 8.5,
            "usability_score": 9.5,
            "aesthetics_score": 7.5,
            "value_score": 9.0,
            "accuracy_score": 9.0,
            "utility_score": 9.5,
            "form_score": 8.0,
            "function_score": 9.5
        },
        {
            "category": "User Psychology",
            "sub_category": "Cognitive Biases",
            "title": "Predictable Behavior Patterns",
            "topic": "Decision Making",
            "detail": "Users exhibit predictable biases: confirmation bias (seeking agreeable information), availability heuristic (overweighting recent information), anchoring bias (influenced by initial exposure). Design can leverage or mitigate these biases.",
            "specific_url": "https://www.nngroup.com/articles/psychology-study-guide/",
            "identify_tags": ["cognitive biases", "decision making", "confirmation bias", "anchoring"],
            "summary": "Understanding cognitive biases enables more effective and persuasive interface design",
            "raw_data": "Confirmation bias, availability heuristic, anchoring bias, framing effects",
            "sentiment_score": 7.5,
            "usability_score": 8.5,
            "aesthetics_score": 7.0,
            "value_score": 8.5,
            "accuracy_score": 9.0,
            "utility_score": 8.5,
            "form_score": 7.5,
            "function_score": 8.5
        }
    ]
    
    # Design System Principles
    design_system_data = [
        {
            "category": "Design Systems",
            "sub_category": "Component Architecture",
            "title": "Systematic Design Approach",
            "topic": "Scalable Design",
            "detail": "Adaptable system of guidelines, components, and tools supporting UI design best practices. Component-based architecture with clear hierarchies. Enables collaboration between designers and developers.",
            "specific_url": "https://m3.material.io/",
            "identify_tags": ["design systems", "components", "scalability", "collaboration"],
            "summary": "Design systems provide systematic approaches to creating consistent, scalable interfaces",
            "raw_data": "Component library, design tokens, style guides, documentation, version control",
            "sentiment_score": 8.0,
            "usability_score": 8.5,
            "aesthetics_score": 8.5,
            "value_score": 9.0,
            "accuracy_score": 9.0,
            "utility_score": 9.0,
            "form_score": 8.5,
            "function_score": 8.5
        },
        {
            "category": "Design Systems",
            "sub_category": "Design Tokens",
            "title": "Systematic Design Decisions",
            "topic": "Consistency Management",
            "detail": "Design tokens provide systematic way to manage design decisions across platforms. Enable consistent application of colors, typography, spacing while allowing customization and brand adaptation.",
            "specific_url": "https://m3.material.io/foundations",
            "identify_tags": ["design tokens", "consistency", "cross-platform", "customization"],
            "summary": "Design tokens ensure consistent design application while enabling customization and adaptation",
            "raw_data": "Color tokens, typography tokens, spacing tokens, elevation tokens, motion tokens",
            "sentiment_score": 7.5,
            "usability_score": 8.5,
            "aesthetics_score": 8.0,
            "value_score": 9.0,
            "accuracy_score": 9.5,
            "utility_score": 9.0,
            "form_score": 8.5,
            "function_score": 8.5
        }
    ]
    
    # Combine all data
    dataset.extend(visual_design_data)
    dataset.extend(dashboard_data)
    dataset.extend(enterprise_data)
    dataset.extend(accessibility_data)
    dataset.extend(psychology_data)
    dataset.extend(design_system_data)
    
    return dataset

def create_spreadsheet(dataset, filename="ui_ux_research_dataset.xlsx"):
    """Create comprehensive Excel spreadsheet with multiple sheets and analysis."""
    
    # Create main dataframe
    df = pd.DataFrame(dataset)
    
    # Create Excel writer with multiple sheets
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'top',
            'border': 1
        })
        
        score_format = workbook.add_format({
            'num_format': '0.0',
            'align': 'center',
            'border': 1
        })
        
        # Main dataset sheet
        df.to_excel(writer, sheet_name='Complete Dataset', index=False)
        worksheet = writer.sheets['Complete Dataset']
        
        # Format headers
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Set column widths and formats
        column_widths = {
            'A': 15,  # category
            'B': 20,  # sub_category
            'C': 30,  # title
            'D': 25,  # topic
            'E': 50,  # detail
            'F': 40,  # specific_url
            'G': 30,  # identify_tags
            'H': 40,  # summary
            'I': 40,  # raw_data
            'J': 12,  # sentiment_score
            'K': 12,  # usability_score
            'L': 12,  # aesthetics_score
            'M': 12,  # value_score
            'N': 12,  # accuracy_score
            'O': 12,  # utility_score
            'P': 12,  # form_score
            'Q': 12   # function_score
        }
        
        for col, width in column_widths.items():
            worksheet.set_column(f'{col}:{col}', width)
        
        # Format score columns
        score_columns = ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
        for col in score_columns:
            worksheet.set_column(f'{col}:{col}', 12, score_format)
        
        # Category analysis sheet
        category_analysis = df.groupby('category').agg({
            'sentiment_score': ['mean', 'std', 'count'],
            'usability_score': ['mean', 'std'],
            'aesthetics_score': ['mean', 'std'],
            'value_score': ['mean', 'std'],
            'accuracy_score': ['mean', 'std'],
            'utility_score': ['mean', 'std'],
            'form_score': ['mean', 'std'],
            'function_score': ['mean', 'std']
        }).round(2)
        
        category_analysis.to_excel(writer, sheet_name='Category Analysis')
        
        # Sub-category breakdown
        subcategory_analysis = df.groupby(['category', 'sub_category']).agg({
            'sentiment_score': 'mean',
            'usability_score': 'mean',
            'aesthetics_score': 'mean',
            'value_score': 'mean',
            'accuracy_score': 'mean',
            'utility_score': 'mean',
            'form_score': 'mean',
            'function_score': 'mean'
        }).round(2)
        
        subcategory_analysis.to_excel(writer, sheet_name='Subcategory Analysis')
        
        # Top performers by dimension
        top_performers = pd.DataFrame({
            'Top Sentiment': df.nlargest(5, 'sentiment_score')[['title', 'sentiment_score']].values.tolist(),
            'Top Usability': df.nlargest(5, 'usability_score')[['title', 'usability_score']].values.tolist(),
            'Top Aesthetics': df.nlargest(5, 'aesthetics_score')[['title', 'aesthetics_score']].values.tolist(),
            'Top Value': df.nlargest(5, 'value_score')[['title', 'value_score']].values.tolist(),
            'Top Utility': df.nlargest(5, 'utility_score')[['title', 'utility_score']].values.tolist()
        })
        
        # Tags analysis
        all_tags = []
        for tags_str in df['identify_tags']:
            if isinstance(tags_str, list):
                all_tags.extend(tags_str)
            else:
                # Handle string representation of list
                import ast
                try:
                    tags_list = ast.literal_eval(tags_str)
                    all_tags.extend(tags_list)
                except:
                    pass
        
        tag_counts = pd.Series(all_tags).value_counts().head(20)
        tag_analysis = pd.DataFrame({
            'Tag': tag_counts.index,
            'Frequency': tag_counts.values
        })
        
        tag_analysis.to_excel(writer, sheet_name='Tag Analysis', index=False)
        
        # Summary statistics
        summary_stats = df[['sentiment_score', 'usability_score', 'aesthetics_score', 
                           'value_score', 'accuracy_score', 'utility_score', 
                           'form_score', 'function_score']].describe().round(2)
        
        summary_stats.to_excel(writer, sheet_name='Summary Statistics')
        
        # Metadata sheet
        metadata = pd.DataFrame({
            'Attribute': ['Dataset Created', 'Total Records', 'Categories', 'Sub-categories', 
                         'Unique Sources', 'Average Scores Range', 'Purpose'],
            'Value': [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                len(df),
                df['category'].nunique(),
                df['sub_category'].nunique(),
                df['specific_url'].nunique(),
                f"{df[['sentiment_score', 'usability_score', 'aesthetics_score', 'value_score', 'accuracy_score', 'utility_score', 'form_score', 'function_score']].min().min():.1f} - {df[['sentiment_score', 'usability_score', 'aesthetics_score', 'value_score', 'accuracy_score', 'utility_score', 'form_score', 'function_score']].max().max():.1f}",
                'Training dataset for UI-Architect-Agent development'
            ]
        })
        
        metadata.to_excel(writer, sheet_name='Metadata', index=False)
    
    print(f"✅ Created comprehensive UI/UX research dataset: {filename}")
    print(f"📊 Total records: {len(df)}")
    print(f"🏷️  Categories: {df['category'].nunique()}")
    print(f"📂 Sub-categories: {df['sub_category'].nunique()}")
    print(f"🔗 Unique sources: {df['specific_url'].nunique()}")
    
    return filename

if __name__ == "__main__":
    print("🎨 Creating comprehensive UI/UX research dataset...")
    
    # Generate dataset
    dataset = create_ui_research_dataset()
    
    # Create spreadsheet
    filename = create_spreadsheet(dataset)
    
    print(f"\n📈 Dataset analysis:")
    df = pd.DataFrame(dataset)
    
    print(f"Average scores across all dimensions:")
    score_columns = ['sentiment_score', 'usability_score', 'aesthetics_score', 
                    'value_score', 'accuracy_score', 'utility_score', 
                    'form_score', 'function_score']
    
    for col in score_columns:
        avg_score = df[col].mean()
        print(f"  {col.replace('_score', '').title()}: {avg_score:.2f}")
    
    print(f"\n🎯 Top categories by average usability score:")
    category_usability = df.groupby('category')['usability_score'].mean().sort_values(ascending=False)
    for category, score in category_usability.items():
        print(f"  {category}: {score:.2f}")
    
    print(f"\n✨ Dataset ready for UI-Architect-Agent training!")
