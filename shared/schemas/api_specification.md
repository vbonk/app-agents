

# Agent Data Management API Specification

This document defines the API for managing agent data. The API is built using FastAPI and interacts with a PostgreSQL database via Prisma ORM.

## 1. Authentication

All API endpoints are secured using OAuth 2.0. A valid access token must be included in the `Authorization` header of all requests.

## 2. Data Models

The API exposes the following data models:

-   `Agent`: Represents an AI agent.
-   `Prompt`: Represents a version of an agent's prompt.
-   `Log`: Represents a log entry for an agent.
-   `Config`: Represents a configuration setting for an agent.
-   `Metric`: Represents a performance metric for an agent.
-   `ToolUsage`: Represents an instance of an agent using a tool.
-   `Dataset`: Represents a dataset used by an agent.
-   `Embedding`: Represents a vector embedding for a piece of content in a dataset.

## 3. API Endpoints

### 3.1. Agents

-   **`GET /agents`**: Get a list of all agents.
-   **`GET /agents/{agent_id}`**: Get a specific agent by ID.
-   **`POST /agents`**: Create a new agent.
-   **`PUT /agents/{agent_id}`**: Update an existing agent.
-   **`DELETE /agents/{agent_id}`**: Delete an agent.

### 3.2. Prompts

-   **`GET /agents/{agent_id}/prompts`**: Get all prompts for an agent.
-   **`GET /agents/{agent_id}/prompts/{version}`**: Get a specific prompt version for an agent.
-   **`POST /agents/{agent_id}/prompts`**: Create a new prompt for an agent.

### 3.3. Logs

-   **`GET /agents/{agent_id}/logs`**: Get all logs for an agent.
-   **`POST /agents/{agent_id}/logs`**: Create a new log entry for an agent.

### 3.4. Configs

-   **`GET /agents/{agent_id}/configs`**: Get all configs for an agent.
-   **`GET /agents/{agent_id}/configs/{key}`**: Get a specific config for an agent.
-   **`POST /agents/{agent_id}/configs`**: Create or update a config for an agent.

### 3.5. Metrics

-   **`GET /agents/{agent_id}/metrics`**: Get all metrics for an agent.
-   **`POST /agents/{agent_id}/metrics`**: Create a new metric for an agent.

### 3.6. Tool Usage

-   **`GET /agents/{agent_id}/tool-usage`**: Get all tool usage records for an agent.
-   **`POST /agents/{agent_id}/tool-usage`**: Create a new tool usage record for an agent.

### 3.7. Datasets

-   **`GET /agents/{agent_id}/datasets`**: Get all datasets for an agent.
-   **`GET /agents/{agent_id}/datasets/{dataset_id}`**: Get a specific dataset for an agent.
-   **`POST /agents/{agent_id}/datasets`**: Create a new dataset for an agent.
-   **`PUT /agents/{agent_id}/datasets/{dataset_id}`**: Update an existing dataset.
-   **`DELETE /agents/{agent_id}/datasets/{dataset_id}`**: Delete a dataset.

### 3.8. Embeddings

-   **`GET /datasets/{dataset_id}/embeddings`**: Get all embeddings for a dataset.
-   **`POST /datasets/{dataset_id}/embeddings`**: Create new embeddings for a dataset.

