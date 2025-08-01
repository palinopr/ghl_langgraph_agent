# Assistants

**Assistants** allow you to manage configurations (like prompts, LLM selection, tools) separately from your graph's core logic, enabling rapid changes that don't alter the graph architecture. It is a way to create multiple specialized versions of the same graph architecture, each optimized for different use cases through configuration variations rather than structural changes.

For example, imagine a general-purpose writing agent built on a common graph architecture. While the structure remains the same, different writing styles—such as blog posts and tweets—require tailored configurations to optimize performance. To support these variations, you can create multiple assistants (e.g., one for blogs and another for tweets) that share the underlying graph but differ in model selection and system prompt.

![assistant versions](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/langgraph-platform/images/assistants.png)

The LangGraph Cloud API provides several endpoints for creating and managing assistants and their versions. See the [API reference](https://langchain-ai.github.io/langgraph/cloud/reference/api/api_ref/#tag/assistants) for more details.

<Info>
  Assistants are a [LangGraph Platform](/langgraph-platform/index) concept. They are not available in the open source LangGraph library.
</Info>

## Configuration

Assistants build on the LangGraph open source concept of [configuration](https://langchain-ai.github.io/langgraph/concepts/low_level/#configuration).
While configuration is available in the open source LangGraph library, assistants are only present in [LangGraph Platform](/langgraph-platform/index). This is due to the fact that assistants are tightly coupled to your deployed graph. Upon deployment, LangGraph Server will automatically create a default assistant for each graph using the graph's default configuration settings.

In practice, an assistant is just an *instance* of a graph with a specific configuration. Therefore, multiple assistants can reference the same graph but can contain different configurations (e.g. prompts, models, tools). The LangGraph Server API provides several endpoints for creating and managing assistants. See the [API reference](https://langchain-ai.github.io/langgraph/cloud/reference/api/api_ref/) and [this how-to](/langgraph-platform/configuration-cloud) for more details on how to create assistants.

## Versioning

Assistants support versioning to track changes over time.
Once you've created an assistant, subsequent edits to that assistant will create new versions. See [this how-to](/langgraph-platform/configuration-cloud#create-a-new-version-for-your-assistant) for more details on how to manage assistant versions.

## Execution

A **run** is an invocation of an assistant. Each run may have its own input, configuration, and metadata, which may affect execution and output of the underlying graph. A run can optionally be executed on a [thread](https://langchain-ai.github.io/langgraph/concepts/persistence/#threads).

The LangGraph Platform API provides several endpoints for creating and managing runs. See the [API reference](https://langchain-ai.github.io/langgraph/cloud/reference/api/api_ref/) for more details.