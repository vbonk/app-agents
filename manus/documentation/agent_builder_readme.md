---

# Agent-Builder: A Framework for Creating AI Agents

**Agent-Builder** is a comprehensive, interactive, and opinionated framework designed to assist developers in building robust, reliable, and well-documented AI agents. It incorporates the latest best practices from leading AI research organizations and the open-source community to provide a structured and guided development experience.

This framework is not just a collection of tools; it is an active agent that collaborates with you to design, scaffold, test, and document new AI agents, ensuring that they are built on a foundation of proven architectural patterns and safety principles.

## Core Principles

The design of the `agent-builder` is guided by a synthesis of best practices from **OpenAI** [1], **Anthropic** [2], **Google** [3], and the **`agents.md`** specification [4]. It is built upon the following core principles:

1.  **Guided & Interactive Development**: The `agent-builder` uses a conversational interface to guide you through the agent creation process, from initial design to final implementation. It asks questions, provides recommendations, and helps you make informed decisions at each step.

2.  **Modularity and Composability**: Following the principle of using simple, composable patterns over complex frameworks, the `agent-builder` helps you create agents from modular, reusable components. This makes your agents easier to understand, maintain, and extend.

3.  **Best-Practice by Default**: The framework embeds best practices directly into the generated code and project structure. This includes robust error handling, clear tool definitions with documentation, human-in-the-loop checkpoints, and comprehensive logging.

4.  **Documentation-First Approach**: The `agent-builder` treats documentation as a first-class citizen. It automatically generates and maintains a detailed `agents.md` file, ensuring that your agent is well-documented and understandable to both humans and other AI agents.

5.  **Test-Driven Development (TDD) for Agents**: To promote reliability, the `agent-builder` facilitates a TDD workflow. It generates test templates alongside your agent's components, encouraging you to write tests early and often.

## Features

The `agent-builder` provides a set of interactive commands to manage the lifecycle of your agent development process:

| Command | Description |
| :--- | :--- |
| `new-agent` | Initializes a new agent project with a guided setup process. |
| `design-agent` | Interactively defines the agent's architecture, roles, and tools. |
| `scaffold-project` | Generates the complete project structure, including boilerplate code and documentation. |
| `add-tool` | A guided workflow for adding new tools to your agent, including code and documentation generation. |
| `run-tests` | Executes the test suite for your agent and provides feedback. |
| `update-docs` | Automatically updates the `agents.md` and `README.md` files to reflect changes in your agent. |
| `publish-agent` | Provides a checklist and guidance for publishing your agent to platforms like GitHub. |

## Getting Started

To start building your first agent with the `agent-builder`, you will typically follow these steps:

1.  **Initialize a new agent project**:
    ```bash
    agent-builder new-agent
    ```

2.  **Design your agent's architecture**:
    ```bash
    agent-builder design-agent
    ```

3.  **Scaffold the project structure**:
    ```bash
    agent-builder scaffold-project
    ```

4.  **Add tools to your agent**:
    ```bash
    agent-builder add-tool
    ```

5.  **Implement your agent's logic and tests**.

6.  **Test your agent**:
    ```bash
    agent-builder run-tests
    ```

7.  **Update your documentation**:
    ```bash
    agent-builder update-docs
    ```

For a more detailed walkthrough, please refer to the [Getting Started Guide](docs/getting-started.md).

## Contributing

We welcome contributions to the `agent-builder` project! If you are interested in contributing, please read our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## References

[1] OpenAI. (2024). *A practical guide to building agents*. [https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

[2] Anthropic. (2024). *Building effective agents*. [https://www.anthropic.com/research/building-effective-agents](https://www.anthropic.com/research/building-effective-agents)

[3] Google. (2024). *Agent Development Kit (ADK)*. [https://google.github.io/adk-docs/](https://google.github.io/adk-docs/)

[4] OpenAI, et al. (2024). *AGENTS.md*. [https://agents.md/](https://agents.md/)

