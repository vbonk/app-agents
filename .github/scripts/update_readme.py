#!/usr/bin/env python3
"""
Automatic README.md Updater for App Agents Repository

This script scans the agents/ directory and automatically updates the README.md
file with current agent information, including descriptions, capabilities,
datasets, and performance metrics.

Author: Manus AI
Created: 2025-09-20
"""

import os
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd

class AgentInfo:
    """Represents information about an agent."""
    
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.description = ""
        self.overview = ""
        self.special_functions = []
        self.datasets = []
        self.use_cases = []
        self.category = "General"
        self.performance_metrics = {}
        
    def load_from_agents_md(self) -> bool:
        """Load agent information from agents.md file."""
        agents_md_path = self.path / "agents.md"
        if not agents_md_path.exists():
            return False
            
        try:
            with open(agents_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract description
            desc_match = re.search(r'## Description\s*\n\n(.*?)(?=\n##|\n\n##|$)', content, re.DOTALL)
            if desc_match:
                self.description = desc_match.group(1).strip()
                
            # Extract capabilities/functions
            cap_match = re.search(r'## Capabilities\s*\n(.*?)(?=\n##|$)', content, re.DOTALL)
            if cap_match:
                cap_content = cap_match.group(1)
                # Extract bullet points or list items
                functions = re.findall(r'[-*]\s*\*\*(.*?)\*\*:?\s*(.*?)(?=\n[-*]|\n\n|$)', cap_content, re.DOTALL)
                self.special_functions = [f"{func.strip()}: {desc.strip()}" for func, desc in functions]
                
            return True
            
        except Exception as e:
            print(f"Error reading agents.md for {self.name}: {e}")
            return False
    
    def load_from_readme(self) -> bool:
        """Load agent information from README.md file."""
        readme_path = self.path / "README.md"
        if not readme_path.exists():
            return False
            
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract description from first paragraph or summary
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('#') and not line.startswith('**'):
                    # Found first content line
                    desc_lines = []
                    for j in range(i, len(lines)):
                        if lines[j].strip() == '' or lines[j].startswith('#'):
                            break
                        desc_lines.append(lines[j].strip())
                    self.description = ' '.join(desc_lines)
                    break
                    
            # Extract overview from ## Overview section if exists
            overview_match = re.search(r'## .*Overview.*\s*\n\n(.*?)(?=\n##|\n\n##|$)', content, re.DOTALL | re.IGNORECASE)
            if overview_match:
                self.overview = overview_match.group(1).strip()
            else:
                # Use description as overview if no separate overview section
                self.overview = self.description
                
            return True
            
        except Exception as e:
            print(f"Error reading README.md for {self.name}: {e}")
            return False
    
    def detect_datasets(self) -> None:
        """Detect dataset files in the agent directory."""
        dataset_extensions = ['.xlsx', '.csv', '.json', '.yaml', '.yml']
        
        # Check docs directory
        docs_path = self.path / "docs"
        if docs_path.exists():
            for file_path in docs_path.rglob("*"):
                if file_path.suffix.lower() in dataset_extensions:
                    self.datasets.append({
                        "name": file_path.name,
                        "path": str(file_path.relative_to(self.path)),
                        "type": file_path.suffix.lower()[1:]  # Remove the dot
                    })
        
        # Check root agent directory
        for file_path in self.path.glob("*"):
            if file_path.suffix.lower() in dataset_extensions:
                self.datasets.append({
                    "name": file_path.name,
                    "path": str(file_path.relative_to(self.path)),
                    "type": file_path.suffix.lower()[1:]
                })
    
    def infer_category(self) -> None:
        """Infer agent category based on name and description."""
        name_lower = self.name.lower()
        desc_lower = self.description.lower()
        
        if any(word in name_lower or word in desc_lower for word in ['crawl', 'scrape', 'extract', 'research', 'analysis']):
            self.category = "Research & Analysis"
        elif any(word in name_lower or word in desc_lower for word in ['ui', 'ux', 'design', 'interface', 'visual']):
            self.category = "Design & UX"
        elif any(word in name_lower or word in desc_lower for word in ['code', 'develop', 'architect', 'build', 'generate']):
            self.category = "Development"
        elif any(word in name_lower or word in desc_lower for word in ['content', 'write', 'document', 'communication']):
            self.category = "Content & Communication"
        else:
            self.category = "General"

class ReadmeUpdater:
    """Updates README.md with current agent information."""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.agents_dir = repo_root / "agents"
        self.readme_path = repo_root / "README.md"
        self.agents: List[AgentInfo] = []
        
    def scan_agents(self) -> None:
        """Scan the agents directory for available agents."""
        if not self.agents_dir.exists():
            print("No agents directory found")
            return
            
        for agent_dir in self.agents_dir.iterdir():
            if agent_dir.is_dir() and not agent_dir.name.startswith('.'):
                agent = AgentInfo(agent_dir.name, agent_dir)
                
                # Try to load from agents.md first, then README.md
                if not agent.load_from_agents_md():
                    agent.load_from_readme()
                
                # Detect datasets and infer category
                agent.detect_datasets()
                agent.infer_category()
                
                self.agents.append(agent)
                print(f"Found agent: {agent.name} ({agent.category})")
    
    def generate_agent_section(self, agent: AgentInfo) -> str:
        """Generate markdown section for an agent."""
        # Clean up the name for display
        display_name = agent.name.replace('-', ' ').replace('_', ' ').title()
        if display_name.endswith(' Agent'):
            display_name = display_name[:-6]  # Remove ' Agent' suffix
        
        section = f"### {display_name}\n"
        
        # Add subtitle based on description
        if agent.description:
            # Extract first sentence or phrase as subtitle
            first_sentence = agent.description.split('.')[0].strip()
            if len(first_sentence) > 100:
                first_sentence = first_sentence[:97] + "..."
            section += f"**{first_sentence}**\n\n"
        
        # Description
        if agent.description:
            section += f"- **Description**: {agent.description}\n"
        
        # Overview
        if agent.overview and agent.overview != agent.description:
            section += f"- **Overview**: {agent.overview}\n"
        
        # Special Functions
        if agent.special_functions:
            section += "- **Special Functions**:\n"
            for func in agent.special_functions[:6]:  # Limit to 6 functions
                section += f"  - {func}\n"
        
        # Datasets
        if agent.datasets:
            section += "- **Dataset(s)**:\n"
            for dataset in agent.datasets:
                section += f"  - `{dataset['name']}` ({dataset['type'].upper()}) - "
                # Add description based on filename
                if 'sample' in dataset['name'].lower():
                    section += "Example data structure and format\n"
                elif 'research' in dataset['name'].lower():
                    section += "Comprehensive research database\n"
                elif 'crawl' in dataset['name'].lower():
                    section += "Web crawling results and analysis\n"
                else:
                    section += "Agent-specific dataset\n"
        
        # Use Cases (inferred from category and description)
        use_cases = self.infer_use_cases(agent)
        if use_cases:
            section += f"- **Use Cases**: {', '.join(use_cases)}\n"
        
        section += "\n"
        return section
    
    def infer_use_cases(self, agent: AgentInfo) -> List[str]:
        """Infer use cases based on agent information."""
        use_cases = []
        
        name_lower = agent.name.lower()
        desc_lower = agent.description.lower()
        
        if 'crawl' in name_lower or 'crawl' in desc_lower:
            use_cases.extend(["Web scraping", "Data extraction", "Competitive analysis"])
        
        if 'ui' in name_lower or 'design' in desc_lower:
            use_cases.extend(["Interface design", "User experience optimization", "Accessibility auditing"])
        
        if 'architect' in name_lower or 'architect' in desc_lower:
            use_cases.extend(["System design", "Architecture planning", "Best practices guidance"])
        
        if 'research' in desc_lower:
            use_cases.extend(["Research analysis", "Data synthesis"])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_use_cases = []
        for use_case in use_cases:
            if use_case not in seen:
                seen.add(use_case)
                unique_use_cases.append(use_case)
        
        return unique_use_cases[:5]  # Limit to 5 use cases
    
    def generate_category_table(self) -> str:
        """Generate the agent categories table."""
        categories = {}
        
        for agent in self.agents:
            if agent.category not in categories:
                categories[agent.category] = []
            categories[agent.category].append(agent.name.replace('-', ' ').replace('_', ' ').title())
        
        table = "| Category | Agents | Focus Area |\n"
        table += "|----------|--------|------------|\n"
        
        category_descriptions = {
            "Research & Analysis": "Web crawling, data extraction, competitive analysis",
            "Design & UX": "Interface design, user experience, accessibility",
            "Development": "Code generation, architecture guidance, testing",
            "Content & Communication": "Content creation, documentation, technical writing"
        }
        
        for category, agents in categories.items():
            agents_str = ", ".join(agents)
            focus = category_descriptions.get(category, "Specialized domain expertise")
            table += f"| **{category}** | {agents_str} | {focus} |\n"
        
        # Add placeholder categories if no agents exist yet
        for category, focus in category_descriptions.items():
            if category not in categories:
                table += f"| **{category}** | *Coming Soon* | {focus} |\n"
        
        return table
    
    def update_readme(self) -> bool:
        """Update the README.md file with current agent information."""
        if not self.readme_path.exists():
            print("README.md not found")
            return False
        
        try:
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate new agents section
            agents_section = "## 🤖 Available Agents\n\n"
            agents_section += "This repository currently contains the following specialized AI agents:\n\n"
            
            # Sort agents by category and name
            sorted_agents = sorted(self.agents, key=lambda x: (x.category, x.name))
            
            for agent in sorted_agents:
                agents_section += self.generate_agent_section(agent)
            
            # Generate categories table
            categories_section = "## 🎯 Agent Categories\n\n"
            categories_section += "Our agents are organized into specialized categories:\n\n"
            categories_section += self.generate_category_table()
            
            # Replace existing sections
            # Find and replace the agents section
            agents_pattern = r'## 🤖 Available Agents.*?(?=## 🎯 Agent Categories|## 📊 Agent Performance Metrics|## Getting Started|$)'
            if re.search(agents_pattern, content, re.DOTALL):
                content = re.sub(agents_pattern, agents_section, content, flags=re.DOTALL)
            else:
                # Insert after repository structure if agents section doesn't exist
                structure_end = content.find("## Getting Started")
                if structure_end != -1:
                    content = content[:structure_end] + agents_section + "\n" + content[structure_end:]
            
            # Replace categories section
            categories_pattern = r'## 🎯 Agent Categories.*?(?=## 📊 Agent Performance Metrics|## Getting Started|$)'
            if re.search(categories_pattern, content, re.DOTALL):
                content = re.sub(categories_pattern, categories_section, content, flags=re.DOTALL)
            else:
                # Insert after agents section
                agents_end = content.find("## 📊 Agent Performance Metrics")
                if agents_end == -1:
                    agents_end = content.find("## Getting Started")
                if agents_end != -1:
                    content = content[:agents_end] + categories_section + "\n" + content[agents_end:]
            
            # Write updated content
            with open(self.readme_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated README.md with {len(self.agents)} agents")
            return True
            
        except Exception as e:
            print(f"Error updating README.md: {e}")
            return False

def main():
    """Main function to update README with agent information."""
    repo_root = Path.cwd()
    
    print("🔄 Scanning for agents and updating README.md...")
    
    updater = ReadmeUpdater(repo_root)
    updater.scan_agents()
    
    if not updater.agents:
        print("⚠️ No agents found in the repository")
        return
    
    success = updater.update_readme()
    
    if success:
        print("✅ README.md successfully updated!")
        print(f"📊 Summary:")
        print(f"   - Total agents: {len(updater.agents)}")
        
        categories = {}
        for agent in updater.agents:
            categories[agent.category] = categories.get(agent.category, 0) + 1
        
        for category, count in categories.items():
            print(f"   - {category}: {count} agent(s)")
    else:
        print("❌ Failed to update README.md")
        exit(1)

if __name__ == "__main__":
    main()
