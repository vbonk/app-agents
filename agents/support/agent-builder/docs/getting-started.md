---

# Getting Started with Agent-Builder

This guide provides a detailed walkthrough of how to use the `agent-builder` to create, design, and implement a new AI agent. We will build a simple "weather-agent" as an example.

## 1. Initialize a New Agent Project

The first step is to create a new project for your agent. The `new-agent` command will ask you for some basic information about your agent and create a new directory for it.

```bash
agent-builder new-agent
```

**Example Interaction:**

```
> What is the name of your agent? (e.g., weather-agent)
weather-agent
> Provide a brief, one-sentence description of your agent.
An agent that can retrieve the current weather for a given location.
> Agent project "weather-agent" created successfully.
```

This will create a new directory named `weather-agent` with a basic project structure.

## 2. Design Your Agent's Architecture

Next, you will use the `design-agent` command to define the architecture of your agent. This is an interactive process where the `agent-builder` will guide you through defining the agent's roles, tools, and other characteristics.

```bash
cd weather-agent
agent-builder design-agent
```

**Example Interaction:**

```
> What is the primary role of the "weather-agent"? (e.g., a helpful assistant, a data analyst, a code generator)
A helpful assistant that provides weather information.
> What tools will the "weather-agent" need? (Provide a comma-separated list, e.g., weather-api, location-service)
weather-api
> Does the agent require human-in-the-loop for any decisions? (yes/no)
no
> Agent design completed successfully.
```

## 3. Scaffold the Project Structure

Now that you have a design, you can use the `scaffold-project` command to generate the complete project structure, including boilerplate code and documentation.

```bash
agent-builder scaffold-project
```

This command will create the following structure within your `weather-agent` directory:

```
weather-agent/
├── agents.md
├── README.md
├── src/
│   ├── agent.py
│   └── tools/
│       └── weather_api.py
└── tests/
    ├── test_agent.py
    └── test_weather_api.py
```

-   `agents.md`: A pre-populated file with the agent's design information.
-   `README.md`: A basic README file for your agent.
-   `src/agent.py`: The main file for your agent's logic.
-   `src/tools/weather_api.py`: A template file for the `weather-api` tool.
-   `tests/test_agent.py`: A test template for your agent.
-   `tests/test_weather_api.py`: A test template for the `weather-api` tool.

## 4. Implement Your Agent's Logic and Tools

With the project scaffolded, you can now implement the logic for your agent and its tools.

-   **Implement the tool**: Open `src/tools/weather_api.py` and add the code to call a weather API and return the weather information.
-   **Implement the agent**: Open `src/agent.py` and add the logic to use the `weather-api` tool to get the weather for a location provided by the user.
-   **Write tests**: Open the files in the `tests/` directory and write tests for your agent and its tool.

## 5. Test Your Agent

Once you have implemented your agent, you can run the test suite using the `run-tests` command.

```bash
agent-builder run-tests
```

This command will execute all the tests in the `tests/` directory and provide a report of the results. If any tests fail, it will provide suggestions for fixing them.

## 6. Update Your Documentation

As you develop your agent, you can use the `update-docs` command to automatically update the `agents.md` and `README.md` files to reflect any changes in your agent's tools or functionality.

```bash
agent-builder update-docs
```

This ensures that your documentation is always up-to-date with your agent's implementation.

## 7. Publish Your Agent

When you are ready to share your agent, the `publish-agent` command will provide a checklist and guidance for publishing your agent to platforms like GitHub.

```bash
agent-builder publish-agent
```

This command will guide you through the process of creating a repository, pushing your code, and creating a release.

