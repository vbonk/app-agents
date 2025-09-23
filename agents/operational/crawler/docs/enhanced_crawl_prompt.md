# Enhanced Web Crawling and Research Prompt for AI Agent Training Dataset Creation

## Mission Statement

You are tasked with conducting a comprehensive analysis of software application website(s) to create a detailed, structured dataset that will serve as training data for AI coding agents. Your goal is to capture every aspect of the software that would enable an AI agent to understand the application's architecture, features, functionality, design principles, workflows, and implementation details at a level sufficient for autonomous development work.

## Target Analysis Scope

**Primary Targets:** [Insert specific website URLs here]

**Secondary Targets:** Related documentation sites, API references, developer portals, design systems, community resources, and any associated repositories or technical resources.

## Comprehensive Analysis Framework

### Phase 1: Discovery and Mapping

Systematically crawl and map the entire digital presence of the software application. This includes the main website, all subdomains, documentation portals, API references, design system documentation, developer resources, community forums, and any associated technical resources. Create a comprehensive site map that identifies all available information sources.

Pay particular attention to discovering hidden or less obvious resources such as developer tools, administrative interfaces, API documentation, SDK references, and technical blog posts that may contain implementation details not found in standard user documentation.

### Phase 2: Content Categorization and Prioritization

Analyze each discovered page and resource to determine its information value and categorize it according to the database schema. Prioritize content that provides insights into software architecture, technical implementation, design decisions, user workflows, integration capabilities, and development processes.

Focus especially on content that reveals the "why" behind design decisions, not just the "what" of features. This includes architectural decision records, design rationale, performance considerations, security implementations, and scalability approaches.

### Phase 3: Deep Information Extraction

For each piece of content, extract information according to the following systematic approach:

**Architectural Understanding:** Capture system architecture details, technology stack information, data flow patterns, integration points, security implementations, performance optimizations, and scalability considerations. Document how different components interact and depend on each other.

**Feature Analysis:** Document not only what features exist but how they work internally, what problems they solve, how they integrate with other features, what configuration options are available, and what limitations or constraints exist. Include information about feature evolution and planned enhancements.

**User Experience Mapping:** Capture user workflows, interface design patterns, interaction models, accessibility considerations, responsive design approaches, and user journey optimization strategies. Document how the user experience supports business objectives.

**Technical Implementation:** Extract details about APIs, data models, authentication systems, authorization frameworks, caching strategies, database designs, deployment architectures, monitoring approaches, and development workflows. Include information about technical debt, known issues, and optimization opportunities.

**Integration Ecosystem:** Document all third-party integrations, API dependencies, webhook implementations, data synchronization approaches, and external service relationships. Include information about integration patterns and best practices.

**Development Processes:** Capture information about code organization, development workflows, testing strategies, deployment processes, monitoring approaches, documentation standards, and quality assurance practices.

## Database Population Instructions

### Data Structure Requirements

Populate the spreadsheet database with extracted information using the following field specifications:

**Category:** Use primary classifications including Features, Architecture, UI/UX, Use Cases, Integrations, Design, Workflows, Templates, Guidelines, Security, Performance, Data Management, Development Processes, Business Logic, and System Administration.

**Sub-category:** Provide granular classification within each category. Examples include Core Features, Third-party Integrations, Design System Components, Authentication Methods, API Endpoints, Database Schema, Deployment Strategies, and Testing Frameworks.

**Title:** Create descriptive, specific titles that clearly identify the information being documented. Titles should be unique and searchable, enabling quick identification of related content.

**Topic:** Specify the exact aspect or component being described. This should be more specific than the title and identify the particular element, function, or concept being documented.

**Detail:** Provide comprehensive descriptions that include functional specifications, implementation details, configuration options, dependencies, limitations, and contextual information. Include code snippets, configuration examples, and technical specifications where relevant.

**Specific URL:** Record the exact URL where information was found, including anchor links to specific sections when applicable. This enables verification and provides direct access to source material.

**Identify Tags:** Use a consistent tagging system with relevant keywords including technology names, feature categories, user roles, integration types, and functional areas. Tags should support semantic search and relationship mapping.

**Summary:** Create concise overviews that capture the essential information in a format suitable for quick reference and filtering. Summaries should be complete enough to understand the basic concept without reading the full detail.

**Raw Data:** Preserve original content including HTML structures, code examples, configuration snippets, and any other source material that provides additional context or might be useful for future analysis.

### Quality Standards

**Completeness:** Each entry must contain sufficient information for an AI agent to understand the concept, its purpose, its implementation, and its relationships to other system components. Avoid incomplete or superficial descriptions.

**Accuracy:** Verify technical details, validate code examples, and ensure that descriptions accurately reflect the actual functionality. Cross-reference information across multiple sources when possible.

**Consistency:** Use standardized terminology, consistent categorization, and uniform formatting throughout the dataset. Maintain consistency in naming conventions and tagging approaches.

**Depth:** Capture not only functional descriptions but also implementation rationale, design considerations, performance implications, and integration requirements. Include information about edge cases, error handling, and optimization strategies.

**Context:** Provide sufficient context for each entry to be understood independently while also documenting relationships and dependencies with other system components.

## Advanced Analysis Techniques

### Pattern Recognition

Identify recurring patterns in architecture, design, implementation, and user experience. Document these patterns as separate entries that can help AI agents understand the underlying principles and approaches used throughout the application.

### Relationship Mapping

Document relationships between different features, components, and systems. This includes dependencies, data flows, user journey connections, and integration points that help AI agents understand the holistic system architecture.

### Evolution Analysis

Where possible, capture information about how features and systems have evolved over time, including deprecated functionality, migration strategies, and planned enhancements. This helps AI agents understand the trajectory and stability of different components.

### Performance and Scalability Insights

Document performance characteristics, scalability limitations, optimization strategies, and resource requirements. Include information about monitoring approaches and performance tuning techniques.

## Success Criteria

The resulting dataset should enable an AI coding agent to:

- Understand the complete system architecture and component relationships
- Generate appropriate code that follows established patterns and conventions
- Make informed decisions about feature implementation and integration
- Understand user needs and business requirements that drive technical decisions
- Navigate the codebase and documentation effectively
- Implement new features that align with existing design principles
- Optimize performance and address scalability requirements
- Follow established development and deployment processes
- Integrate with existing systems and third-party services appropriately
- Maintain code quality and adhere to established standards

## Implementation Notes

This analysis should be conducted with the understanding that the resulting dataset will be used to train AI agents for autonomous development work. Therefore, the level of detail and the types of information captured should reflect what a skilled developer would need to know to work effectively with the application.

The analysis should be iterative, with initial broad coverage followed by deeper analysis of high-value areas. The goal is to create a comprehensive knowledge base that captures both explicit documentation and implicit knowledge that experienced developers would accumulate through working with the system.

Remember that AI agents will use this dataset to make decisions about code generation, system modification, and feature implementation. The quality and completeness of this dataset directly impacts the effectiveness of AI agents trained on it.
