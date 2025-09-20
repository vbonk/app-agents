
# Anthropic's Guide to Building Effective Agents - Key Findings

## Publication Details
- Title: "Building effective agents"
- Published: December 19, 2024
- Source: Anthropic Engineering

## Core Philosophy
**Key Insight**: "We've worked with dozens of teams building LLM agents across industries. Consistently, the most successful implementations use simple, composable patterns rather than complex frameworks."

## Anthropic's Agent Definitions

**Agentic Systems**: Anthropic categorizes all agent variations as "agentic systems" but draws an important architectural distinction:

- **Workflows**: Systems where LLMs and tools are orchestrated through predefined code paths
- **Agents**: Systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks

## Agent Architecture Principles

**Core Agent Loop**: Agents are typically just LLMs using tools based on environmental feedback in a loop.

**Key Components**:
1. **Initialization**: Agents begin with either a command from, or interactive discussion with, the human user
2. **Planning**: Once the task is clear, agents plan and operate independently
3. **Execution**: During execution, agents must gain "ground truth" from the environment at each step (tool call results, code execution)
4. **Checkpoints**: Agents can pause for human feedback at checkpoints or when encountering blockers
5. **Termination**: Tasks terminate upon completion, with stopping conditions (maximum iterations) to maintain control

## When to Use Agents

**Ideal Use Cases**: 
- Open-ended problems where it's difficult or impossible to predict the required number of steps
- Situations where you can't hardcode a fixed path
- Tasks requiring many LLM turns with trusted decision-making
- Scaling tasks in trusted environments

**Considerations**:
- Higher costs due to autonomous nature
- Potential for compounding errors
- Requires extensive testing in sandboxed environments
- Need appropriate guardrails

## Tool Design Principles

**Critical Insight**: "It is crucial to design toolsets and their documentation clearly and thoughtfully."

## Real-World Examples
- Coding agents for SWE-bench tasks (multi-file edits)
- Computer use implementations where Claude uses a computer to accomplish tasks
