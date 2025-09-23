# OpenAI Swarm Repository Analysis

## Repository: openai/swarm
- **URL**: https://github.com/openai/swarm
- **Stars**: 20.4k
- **Forks**: 2.2k
- **Recent Activity**: Moderate (commits 6 months ago)
- **Latest Release**: No releases published
- **Total Commits**: 28

## Description
Educational framework exploring ergonomic, lightweight multi-agent orchestration. Managed by OpenAI Solution team.

## Important Note
Swarm is now replaced by the OpenAI Agents SDK, which is a production-ready evolution of Swarm. The Agents SDK features key improvements and will be actively maintained by the OpenAI team. OpenAI recommends migrating to the Agents SDK for all production use cases.

## Key Features
Swarm focuses on making agent coordination and execution lightweight, highly controllable, and easily testable. It accomplishes this through two primitive abstractions: Agents and handoffs. An Agent encompasses instructions and tools, and can at any point choose to hand off a conversation to another Agent.

The framework explores patterns that are lightweight, scalable, and highly customizable by design. Approaches similar to Swarm are best suited for situations dealing with a large number of independent capabilities and instructions that are difficult to encode into a single prompt.

Swarm runs almost entirely on the client and, much like the Chat Completions API, does not store state between calls. It is powered entirely by the Chat Completions API and is stateless between calls.

## Use Cases
- Educational exploration of multi-agent orchestration
- Lightweight agent coordination
- Highly controllable agent execution
- Testable multi-agent systems
- Learning about agent handoffs and coordination patterns
