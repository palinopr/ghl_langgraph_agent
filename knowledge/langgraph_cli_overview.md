# LangGraph CLI

**LangGraph CLI** is a multi-platform command-line tool for building and running the [LangGraph API server](/langgraph-platform/langgraph-server) locally. The resulting server includes all API endpoints for your graph's runs, threads, assistants, etc. as well as the other services required to run your agent, including a managed database for checkpointing and storage.

## Installation

The LangGraph CLI can be installed via pip or [Homebrew](https://brew.sh/):

<Tabs>
  <Tab title="pip">
    ```bash
    pip install langgraph-cli
    ```
  </Tab>

  <Tab title="Homebrew">
    ```bash
    brew install langgraph-cli
    ```
  </Tab>
</Tabs>

## Commands

LangGraph CLI provides the following core functionality:

| Command                                                      | Description                                                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`langgraph build`](/langgraph-platform/cli#build)           | Builds a Docker image for the [LangGraph API server](/langgraph-platform/langgraph-server) that can be directly deployed.                                                                                                                                                                             |
| [`langgraph dev`](/langgraph-platform/cli#dev)               | Starts a lightweight development server that requires no Docker installation. This server is ideal for rapid development and testing. This is available in version 0.1.55 and up.                                                                                                                     |
| [`langgraph dockerfile`](/langgraph-platform/cli#dockerfile) | Generates a [Dockerfile](https://docs.docker.com/reference/dockerfile/) that can be used to build images for and deploy instances of the [LangGraph API server](/langgraph-platform/langgraph-server). This is useful if you want to further customize the dockerfile or deploy in a more custom way. |
| [`langgraph up`](/langgraph-platform/cli#up)                 | Starts an instance of the [LangGraph API server](/langgraph-platform/langgraph-server) locally in a docker container. This requires the docker server to be running locally. It also requires a LangSmith API key for local development or a license key for production use.                          |

For more information, see the [LangGraph CLI Reference](/langgraph-platform/cli).