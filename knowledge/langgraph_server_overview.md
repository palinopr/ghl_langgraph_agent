# LangGraph Server

**LangGraph Server** offers an API for creating and managing agent-based applications. It is built on the concept of [assistants](assistants), which are agents configured for specific tasks, and includes built-in [persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/#memory-store) and a **task queue**. This versatile API supports a wide range of agentic application use cases, from background processing to real-time interactions.

Use LangGraph Server to create and manage [assistants](assistants), [threads](https://langchain-ai.github.io/langgraph/concepts/persistence/#threads), [runs](assistants#execution), [cron jobs](cron-jobs), [webhooks](webhooks), and more.

<Tip>
  **API reference**
  For detailed information on the API endpoints and data models, see [LangGraph Platform API reference docs](https://langchain-ai.github.io/langgraph/cloud/reference/api/server-api-ref.html).
</Tip>

To use the `Enterprise` version of the LangGraph Server, you must acquire a license key that you will need to specify when running the Docker image. To acquire a license key, please email [sales@langchain.dev](mailto:sales@langchain.dev).

You can run the `Enterprise` version of the LangGraph Server on the following deployment options:

* Cloud SaaS
* Self-hosted Data Plane
* Self-hosted Control Plane
* Standalone container

## Application structure

To deploy a LangGraph Server application, you need to specify the graph(s) you want to deploy, as well as any relevant configuration settings, such as dependencies and environment variables.

Read the [application structure](./application-structure) guide to learn how to structure your LangGraph application for deployment.

## Parts of a deployment

When you deploy LangGraph Server, you are deploying one or more [graphs](#graphs), a database for [persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/), and a task queue.

### Graphs

When you deploy a graph with LangGraph Server, you are deploying a "blueprint" for an [Assistant](assistants).

An [Assistant](assistants) is a graph paired with specific configuration settings. You can create multiple assistants per graph, each with unique settings to accommodate different use cases
that can be served by the same graph.

Upon deployment, LangGraph Server will automatically create a default assistant for each graph using the graph's default configuration settings.

<Note>
  We often think of a graph as implementing an [agent](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/), but a graph does not necessarily need to implement an agent. For example, a graph could implement a simple
  chatbot that only supports back-and-forth conversation, without the ability to influence any application control flow. In reality, as applications get more complex, a graph will often implement a more complex flow that may use [multiple agents](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) working in tandem.
</Note>

### Persistence and task queue

LangGraph Server leverages a database for [persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/) and a task queue.

Currently, only [Postgres](https://www.postgresql.org/) is supported as a database for LangGraph Server and [Redis](https://redis.io/) as the task queue.

If you're deploying using [LangGraph Platform](cloud), these components are managed for you. If you're deploying LangGraph Server on your own infrastructure, you'll need to set up and manage these components yourself.

Please review the [deployment options](deployment-options) guide for more information on how these components are set up and managed.

## Learn more

* LangGraph [Application Structure](application-structure) guide explains how to structure your LangGraph application for deployment.
* The [LangGraph Platform API Reference](https://langchain-ai.github.io/langgraph/cloud/reference/api/server-api-ref.html) provides detailed information on the API endpoints and data models.