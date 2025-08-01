# Add human-in-the-loop controls

<Note>
  This tutorial builds on [Add Memory](/langgraph-platform/langgraph-basics/3-add-memory).
</Note>

Agents can be unreliable and may need human input to successfully accomplish tasks. Similarly, for some actions, you may want to require human approval before running to ensure that everything is running as intended.

LangGraph's [persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/) layer supports **human-in-the-loop** workflows, allowing execution to pause and resume based on user feedback. The primary interface to this functionality is the [`interrupt`](/langgraph-platform/add-human-in-the-loop) function. Calling `interrupt` inside a node will pause execution. Execution can be resumed, together with new input from a human, by passing in a [Command](https://langchain-ai.github.io/langgraph/concepts/low_level/#command). `interrupt` is ergonomically similar to Python's built-in `input()`, [with some caveats](/langgraph-platform/add-human-in-the-loop).

## 1. Add the `human_assistance` tool

Starting with the existing code from the [Add memory to the chatbot](/langgraph-platform/langgraph-basics/3-add-memory) tutorial, add the `human_assistance` tool to the chatbot. This tool uses `interrupt` to receive information from a human.

Let's first select a chat model:

<Tabs>
  <Tab title="OpenAI">
    ```shell
    pip install -U "langchain[openai]"
    ```

    ```python
    import os
    from langchain.chat_models import init_chat_model

    os.environ["OPENAI_API_KEY"] = "sk-..."

    llm = init_chat_model("openai:gpt-4.1")
    ```

    👉 Read the [OpenAI integration docs](https://python.langchain.com/docs/integrations/chat/openai/)
  </Tab>

  <Tab title="Anthropic">
    ```shell
    pip install -U "langchain[anthropic]"
    ```

    ```python
    import os
    from langchain.chat_models import init_chat_model

    os.environ["ANTHROPIC_API_KEY"] = "sk-..."

    llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    ```

    👉 Read the [Anthropic integration docs](https://python.langchain.com/docs/integrations/chat/anthropic/)
  </Tab>

  <Tab title="Azure">
    ```shell
    pip install -U "langchain[openai]"
    ```

    ```python
    import os
    from langchain.chat_models import init_chat_model

    os.environ["AZURE_OPENAI_API_KEY"] = "..."
    os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
    os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

    llm = init_chat_model(
        "azure_openai:gpt-4.1",
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    )
    ```

    👉 Read the [Azure integration docs](https://python.langchain.com/docs/integrations/chat/azure_chat_openai/)
  </Tab>

  <Tab title="Google Gemini">
    ```shell
    pip install -U "langchain[google-genai]"
    ```

    ```python
    import os
    from langchain.chat_models import init_chat_model

    os.environ["GOOGLE_API_KEY"] = "..."

    llm = init_chat_model("google_genai:gemini-2.0-flash")
    ```

    👉 Read the [Google GenAI integration docs](https://python.langchain.com/docs/integrations/chat/google_generative_ai/)
  </Tab>

  <Tab title="AWS Bedrock">
    ```shell
    pip install -U "langchain[aws]"
    ```

    ```python
    from langchain.chat_models import init_chat_model

    # Follow the steps here to configure your credentials:
    # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

    llm = init_chat_model(
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_provider="bedrock_converse",
    )
    ```

    👉 Read the [AWS Bedrock integration docs](https://python.langchain.com/docs/integrations/chat/bedrock/)
  </Tab>
</Tabs>

{/* ```python
  from langchain.chat_models import init_chat_model

  llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
  ``` */}

We can now incorporate it into our `StateGraph` with an additional tool:

```python hl_lines="12 19 20 21 22 23"
from typing import Annotated

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.types import Command, interrupt

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tool = TavilySearch(max_results=2)
tools = [tool, human_assistance]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
```

<Tip>
  For more information and examples of human-in-the-loop workflows, see [Human-in-the-loop](/langgraph-platform/add-human-in-the-loop).
</Tip>

## 2. Compile the graph

We compile the graph with a checkpointer, as before:

```python
memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)
```

<a id="optional" />

## 3. Visualize the graph

Visualizing the graph, you get the same layout as before – just with the added tool!

```python
from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass
```

![chatbot-with-tools-diagram](https://mintlify.s3.us-west-1.amazonaws.com/langchain-5e9cc07a/langgraph-platform/langgraph-basics/chatbot-with-tools.png)

## 4. Prompt the chatbot

Now, prompt the chatbot with a question that will engage the new `human_assistance` tool:

```python
user_input = "I need some expert guidance for building an AI agent. Could you request assistance for me?"
config = {"configurable": {"thread_id": "1"}}

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
```

```
================================ Human Message =================================

I need some expert guidance for building an AI agent. Could you request assistance for me?
================================== Ai Message ==================================

[{'text': "Certainly! I'd be happy to request expert assistance for you regarding building an AI agent. To do this, I'll use the human_assistance function to relay your request. Let me do that for you now.", 'type': 'text'}, {'id': 'toolu_01ABUqneqnuHNuo1vhfDFQCW', 'input': {'query': 'A user is requesting expert guidance for building an AI agent. Could you please provide some expert advice or resources on this topic?'}, 'name': 'human_assistance', 'type': 'tool_use'}]
Tool Calls:
  human_assistance (toolu_01ABUqneqnuHNuo1vhfDFQCW)
 Call ID: toolu_01ABUqneqnuHNuo1vhfDFQCW
  Args:
    query: A user is requesting expert guidance for building an AI agent. Could you please provide some expert advice or resources on this topic?
```

The chatbot generated a tool call, but then execution has been interrupted. If you inspect the graph state, you see that it stopped at the tools node:

```python
snapshot = graph.get_state(config)
snapshot.next
```

```
('tools',)
```

<Info>
  **Additional information**
  Take a closer look at the `human_assistance` tool:

  ```python
  @tool
  def human_assistance(query: str) -> str:
      """Request assistance from a human."""
      human_response = interrupt({"query": query})
      return human_response["data"]
  ```

  Similar to Python's built-in `input()` function, calling `interrupt` inside the tool will pause execution. Progress is persisted based on the [checkpointer](https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpointer-libraries); so if it is persisting with Postgres, it can resume at any time as long as the database is alive. In this example, it is persisting with the in-memory checkpointer and can resume any time if the Python kernel is running.
</Info>

## 5. Resume execution

To resume execution, pass a [`Command`](https://langchain-ai.github.io/langgraph/concepts/low_level/#command) object containing data expected by the tool. The format of this data can be customized based on needs. For this example, use a dict with a key `"data"`:

```python
human_response = (
    "We, the experts are here to help! We'd recommend you check out LangGraph to build your agent."
    " It's much more reliable and extensible than simple autonomous agents."
)

human_command = Command(resume={"data": human_response})

events = graph.stream(human_command, config, stream_mode="values")
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()
```

```
================================== Ai Message ==================================

[{'text': "Certainly! I'd be happy to request expert assistance for you regarding building an AI agent. To do this, I'll use the human_assistance function to relay your request. Let me do that for you now.", 'type': 'text'}, {'id': 'toolu_01ABUqneqnuHNuo1vhfDFQCW', 'input': {'query': 'A user is requesting expert guidance for building an AI agent. Could you please provide some expert advice or resources on this topic?'}, 'name': 'human_assistance', 'type': 'tool_use'}]
Tool Calls:
  human_assistance (toolu_01ABUqneqnuHNuo1vhfDFQCW)
 Call ID: toolu_01ABUqneqnuHNuo1vhfDFQCW
  Args:
    query: A user is requesting expert guidance for building an AI agent. Could you please provide some expert advice or resources on this topic?
================================= Tool Message =================================
Name: human_assistance

We, the experts are here to help! We'd recommend you check out LangGraph to build your agent. It's much more reliable and extensible than simple autonomous agents.
================================== Ai Message ==================================

Thank you for your patience. I've received some expert advice regarding your request for guidance on building an AI agent. Here's what the experts have suggested:

The experts recommend that you look into LangGraph for building your AI agent. They mention that LangGraph is a more reliable and extensible option compared to simple autonomous agents.

LangGraph is likely a framework or library designed specifically for creating AI agents with advanced capabilities. Here are a few points to consider based on this recommendation:

1. Reliability: The experts emphasize that LangGraph is more reliable than simpler autonomous agent approaches. This could mean it has better stability, error handling, or consistent performance.

2. Extensibility: LangGraph is described as more extensible, which suggests that it probably offers a flexible architecture that allows you to easily add new features or modify existing ones as your agent's requirements evolve.

3. Advanced capabilities: Given that it's recommended over "simple autonomous agents," LangGraph likely provides more sophisticated tools and techniques for building complex AI agents.
...
2. Look for tutorials or guides specifically focused on building AI agents with LangGraph.
3. Check if there are any community forums or discussion groups where you can ask questions and get support from other developers using LangGraph.

If you'd like more specific information about LangGraph or have any questions about this recommendation, please feel free to ask, and I can request further assistance from the experts.
Output is truncated. View as a scrollable element or open in a text editor. Adjust cell output settings...
```

The input has been received and processed as a tool message. Review this call's [LangSmith trace](https://smith.langchain.com/public/9f0f87e3-56a7-4dde-9c76-b71675624e91/r) to see the exact work that was done in the above call. Notice that the state is loaded in the first step so that our chatbot can continue where it left off.

**Congratulations!** You've used an `interrupt` to add human-in-the-loop execution to your chatbot, allowing for human oversight and intervention when needed. This opens up the potential UIs you can create with your AI systems. Since you have already added a **checkpointer**, as long as the underlying persistence layer is running, the graph can be paused **indefinitely** and resumed at any time as if nothing had happened.

Check out the code snippet below to review the graph from this tutorial:

<Tabs>
  <Tab title="OpenAI">
    ```shell
    pip install -U "langchain[openai]"
    ```

    ```python
    import os
    from langchain.chat_models import init_chat_model

    os.environ["OPENAI_API_KEY"] = "sk-..."

    llm = init_chat_model("openai:gpt-4.1")
    ```

    👉 Read the [OpenAI integration docs](https://python.langchain.com/docs/integrations/chat/openai/)
  </Tab>

  <Tab title="Anthropic">
    ```shell
    pip install -U "langchain[anthropic]"
    ```

    ```python
    import os
    from langchain.chat_models import init_chat_model

    os.environ["ANTHROPIC_API_KEY"] = "sk-..."

    llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    ```

    👉 Read the [Anthropic integration docs](https://python.langchain.com/docs/integrations/chat/anthropic/)
  </Tab>

  <Tab title="Azure">
    ```shell
    pip install -U "langchain[openai]"
    ```

    ```python
    import os
    from langchain.chat_models import init_chat_model

    os.environ["AZURE_OPENAI_API_KEY"] = "..."
    os.environ["AZURE_OPENAI_ENDPOINT"] = "..."
    os.environ["OPENAI_API_VERSION"] = "2025-03-01-preview"

    llm = init_chat_model(
        "azure_openai:gpt-4.1",
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    )
    ```

    👉 Read the [Azure integration docs](https://python.langchain.com/docs/integrations/chat/azure_chat_openai/)
  </Tab>

  <Tab title="Google Gemini">
    ```shell
    pip install -U "langchain[google-genai]"
    ```

    ```python
    import os
    from langchain.chat_models import init_chat_model

    os.environ["GOOGLE_API_KEY"] = "..."

    llm = init_chat_model("google_genai:gemini-2.0-flash")
    ```

    👉 Read the [Google GenAI integration docs](https://python.langchain.com/docs/integrations/chat/google_generative_ai/)
  </Tab>

  <Tab title="AWS Bedrock">
    ```shell
    pip install -U "langchain[aws]"
    ```

    ```python
    from langchain.chat_models import init_chat_model

    # Follow the steps here to configure your credentials:
    # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

    llm = init_chat_model(
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        model_provider="bedrock_converse",
    )
    ```

    👉 Read the [AWS Bedrock integration docs](https://python.langchain.com/docs/integrations/chat/bedrock/)
  </Tab>
</Tabs>

```python
from typing import Annotated

from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]

tool = TavilySearch(max_results=2)
tools = [tool, human_assistance]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert(len(message.tool_calls) <= 1)
    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
```

## Next steps

So far, the tutorial examples have relied on a simple state with one entry: a list of messages. You can go far with this simple state, but if you want to define complex behavior without relying on the message list, you can [add additional fields to the state](/langgraph-platform/langgraph-basics/5-customize-state).