# Overview

<Info>
  **Prerequisites**

  * [LangGraph Platform](/langgraph-platform/index)
  * [LangGraph Server](/langgraph-platform/langgraph-server)
  * [LangGraph CLI](/langgraph-platform/langgraph-cli)
</Info>

LangGraph Studio is a specialized agent IDE that enables visualization, interaction, and debugging of agentic systems that implement the LangGraph Server API protocol. Studio also integrates with LangSmith to enable tracing, evaluation, and prompt engineering.

![](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/langgraph-platform/images/lg-platform.png)

## Features

Key features of LangGraph Studio:

* Visualize your graph architecture
* [Run and interact with your agent](/langgraph-platform/invoke-studio)
* [Manage assistants](/langgraph-platform/manage-assistants-studio)
* [Manage threads](/langgraph-platform/threads-studio)
* [Iterate on prompts](/langgraph-platform/iterate-graph-studio)
* [Run experiments over a dataset](/langgraph-platform/run-evals-studio)
* Manage [long term memory](https://langchain-ai.github.io/langgraph/concepts/memory/)
* Debug agent state via [time travel](https://langchain-ai.github.io/langgraph/concepts/time-travel/)

LangGraph Studio works for graphs that are deployed on [LangGraph Platform](/langgraph-platform/deployment-quickstart) or for graphs that are running locally via the [LangGraph Server](/langgraph-platform/local-server).

Studio supports two modes:

### Graph mode

Graph mode exposes the full feature-set of Studio and is useful when you would like as many details about the execution of your agent, including the nodes traversed, intermediate states, and LangSmith integrations (such as adding to datasets and playground).

### Chat mode

Chat mode is a simpler UI for iterating on and testing chat-specific agents. It is useful for business users and those who want to test overall agent behavior. Chat mode is only supported for graph's whose state includes or extends [`MessagesState`](https://langchain-ai.github.io/langgraph/how-tos/graph-api/#messagesstate).

## Learn more

* See this guide on how to [get started](/langgraph-platform/quick-start-studio) with LangGraph Studio.