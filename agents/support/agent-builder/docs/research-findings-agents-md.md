# AGENTS.md Specification - Key Findings

## Core Concept
**Definition**: "Think of AGENTS.md as a README for agents: a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project."

## Purpose and Philosophy

**Complementary Design**: AGENTS.md complements README.md files by containing extra, detailed context coding agents need that might clutter a README or aren't relevant to human contributors.

**Key Principles**:
- Give agents a clear, predictable place for instructions
- Keep READMEs concise and focused on human contributors  
- Provide precise, agent-focused guidance that complements existing README and docs

## Adoption and Ecosystem
- Used by over 20k open-source projects
- Compatible with growing ecosystem of AI coding agents and tools
- Emerged from collaborative efforts across AI development ecosystem including OpenAI Codex, Amp, Jules from Google, Cursor, and Factory

## Content Structure

**Popular Sections**:
- Project overview
- Build and test commands
- Code style guidelines
- Testing instructions
- Security considerations
- Commit message guidelines
- Pull request guidelines
- Deployment steps

**Example Content Areas**:
- Dev environment tips
- Testing instructions with specific commands
- PR formatting requirements
- Package management workflows

## Technical Implementation

**Format**: Standard Markdown with no required fields
**Hierarchy**: Supports nested AGENTS.md files for monorepos - closest file to edited code takes precedence
**Integration**: Agents automatically read nearest file in directory tree

## Agent Integration Examples
- Aider: Configure in `.aider.conf.yml` with `read: AGENTS.md`
- Gemini CLI: Configure in `.gemini/settings.json` with `"contextFileName": "AGENTS.md"`

## Key Benefits
- Standardized format across different AI coding tools
- Living documentation that can be updated as projects evolve
- Automatic execution of testing commands by agents
- Clear separation of human vs. agent-focused documentation
