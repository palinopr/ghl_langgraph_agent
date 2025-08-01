# Run application

## Prerequisites

* [Running agents](https://langchain-ai.github.io/langgraph/agents/run_agents/)

This guide shows how to submit a [run](/langgraph-platform/assistants#execution) to your application.

## Graph mode

### Specify input

First define the input to your graph with in the "Input" section on the left side of the page, below the graph interface.

Studio will attempt to render a form for your input based on the graph's defined [state schema](https://langchain-ai.github.io/langgraph/concepts/low_level/#schema). To disable this, click the "View Raw" button, which will present you with a JSON editor.

Click the up/down arrows at the top of the "Input" section to toggle through and use previously submitted inputs.

### Run settings

#### Assistant

To specify the [assistant](/langgraph-platform/assistants) that is used for the run click the settings button in the bottom left corner. If an assistant is currently selected the button will also list the assistant name. If no assistant is selected it will say "Manage Assistants".

Select the assistant to run and click the "Active" toggle at the top of the modal to activate it. [See here](/langgraph-platform/manage-assistants-studio) for more information on managing assistants.

#### Streaming

Click the dropdown next to "Submit" and click the toggle to enable/disable streaming.

#### Breakpoints

To run your graph with breakpoints, click the "Interrupt" button. Select a node and whether to pause before and/or after that node has executed. Click "Continue" in the thread log to resume execution.

For more information on breakpoints see [here](/langgraph-platform/add-human-in-the-loop).

### Submit run

To submit the run with the specified input and run settings, click the "Submit" button. This will add a [run](/langgraph-platform/assistants#execution) to the existing selected [thread](https://langchain-ai.github.io/langgraph/concepts/persistence/#threads). If no thread is currently selected, a new one will be created.

To cancel the ongoing run, click the "Cancel" button.

## Chat mode

Specify the input to your chat application in the bottom of the conversation panel. Click the "Send message" button to submit the input as a Human message and have the response streamed back.

To cancel the ongoing run, click the "Cancel" button. Click the "Show tool calls" toggle to hide/show tool calls in the conversation.

## Learn more

To run your application from a specific checkpoint in an existing thread, see [this guide](/langgraph-platform/threads-studio#edit-thread-history).