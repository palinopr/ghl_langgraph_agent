Python SDK Reference

Skip to content
LangGraph Platform docs have moved! Find the LangGraph Platform docs at the new LangChain Docs site.
logo


Search
 
 GitHub
0.6.2
16.6k
2.8k
Copy page
▾
Get started
Guides
Reference
Examples
Additional resources
Reference
LangGraph
Graphs
Functional API
Pregel
Checkpointing
Storage
Caching
Types
Runtime
Config
Errors
Constants
Channels
Prebuilt
Agents
Supervisor
Swarm
MCP Adapters
LangGraph Platform
SDK (Python)
SDK (JS/TS)
RemoteGraph
Table of contents
 LangGraphClient
 HttpClient
 get
 post
 put
 patch
 delete
 stream
 AssistantsClient
 get
 get_graph
 get_schemas
 get_subgraphs
 create
 update
 delete
 search
 get_versions
 set_latest
 ThreadsClient
 get
 create
 update
 delete
 search
 copy
 get_state
 update_state
 get_history
 RunsClient
 stream
 create
 create_batch
 wait
 list
 get
 cancel
 join
 join_stream
 delete
 CronClient
 create_for_thread
 create
 delete
 search
 StoreClient
 put_item
 get_item
 delete_item
 search_items
 list_namespaces
 SyncLangGraphClient
 SyncHttpClient
 get
 post
 put
 patch
 delete
 stream
 SyncAssistantsClient
 get
 get_graph
 get_schemas
 get_subgraphs
 create
 update
 delete
 search
 get_versions
 set_latest
 SyncThreadsClient
 get
 create
 update
 delete
 search
 copy
 get_state
 update_state
 get_history
 SyncRunsClient
 stream
 create
 create_batch
 wait
 list
 get
 cancel
 join
 join_stream
 delete
 SyncCronClient
 create_for_thread
 create
 delete
 search
 SyncStoreClient
 put_item
 get_item
 delete_item
 search_items
 list_namespaces
 get_client
 get_sync_client
 Json
 RunStatus
 ThreadStatus
 StreamMode
 DisconnectMode
 MultitaskStrategy
 OnConflictBehavior
 OnCompletionBehavior
 All
 IfNotExists
 CancelAction
 AssistantSortBy
 ThreadSortBy
 CronSortBy
 SortOrder
 Config
 tags
 recursion_limit
 configurable
 Checkpoint
 thread_id
 checkpoint_ns
 checkpoint_id
 checkpoint_map
 GraphSchema
 graph_id
 input_schema
 output_schema
 state_schema
 config_schema
 context_schema
 AssistantBase
 assistant_id
 graph_id
 config
 context
 created_at
 metadata
 version
 name
 description
 AssistantVersion
 assistant_id
 graph_id
 config
 context
 created_at
 metadata
 version
 name
 description
 Assistant
 updated_at
 assistant_id
 graph_id
 config
 context
 created_at
 metadata
 version
 name
 description
 Interrupt
 value
 id
 Thread
 thread_id
 created_at
 updated_at
 metadata
 status
 values
 interrupts
 ThreadTask
 ThreadState
 values
 next
 checkpoint
 metadata
 created_at
 parent_checkpoint
 tasks
 interrupts
 ThreadUpdateStateResponse
 checkpoint
 Run
 run_id
 thread_id
 assistant_id
 created_at
 updated_at
 status
 metadata
 multitask_strategy
 Cron
 cron_id
 assistant_id
 thread_id
 end_time
 schedule
 created_at
 updated_at
 payload
 user_id
 next_run_date
 metadata
 RunCreate
 thread_id
 assistant_id
 input
 metadata
 config
 context
 checkpoint_id
 interrupt_before
 interrupt_after
 webhook
 multitask_strategy
 Item
 namespace
 key
 value
 created_at
 updated_at
 ListNamespaceResponse
 namespaces
 SearchItem
 namespace
 key
 value
 created_at
 updated_at
 SearchItemsResponse
 items
 StreamPart
 event
 data
 Send
 node
 input
 Command
 goto
 update
 resume
 RunCreateMetadata
 run_id
 thread_id
 Auth
 types
 exceptions
 on
 authenticate
 RunStatus
 MultitaskStrategy
 OnConflictBehavior
 IfNotExists
 FilterType
 ThreadStatus
 MetadataInput
 HandlerResult
 Authenticator
 MinimalUser
 identity
 MinimalUserDict
 identity
 display_name
 is_authenticated
 permissions
 BaseUser
 is_authenticated
 display_name
 identity
 permissions
 __getitem__
 __contains__
 __iter__
 StudioUser
 BaseAuthContext
 permissions
 user
 AuthContext
 resource
 action
 permissions
 user
 ThreadsCreate
 thread_id
 metadata
 if_exists
 ThreadsRead
 thread_id
 run_id
 ThreadsUpdate
 thread_id
 metadata
 action
 ThreadsDelete
 thread_id
 run_id
 ThreadsSearch
 metadata
 values
 status
 limit
 offset
 thread_id
 RunsCreate
 assistant_id
 thread_id
 run_id
 status
 metadata
 prevent_insert_if_inflight
 multitask_strategy
 if_not_exists
 after_seconds
 kwargs
 action
 AssistantsCreate
 assistant_id
 graph_id
 config
 metadata
 if_exists
 name
 AssistantsRead
 assistant_id
 metadata
 AssistantsUpdate
 assistant_id
 graph_id
 config
 context
 metadata
 name
 version
 AssistantsDelete
 assistant_id
 AssistantsSearch
 graph_id
 metadata
 limit
 offset
 CronsCreate
 payload
 schedule
 cron_id
 thread_id
 user_id
 end_time
 CronsDelete
 cron_id
 CronsRead
 cron_id
 CronsUpdate
 cron_id
 payload
 schedule
 CronsSearch
 assistant_id
 thread_id
 limit
 offset
 StoreGet
 namespace
 key
 StoreSearch
 namespace
 filter
 limit
 offset
 query
 StoreListNamespaces
 namespace
 suffix
 max_depth
 limit
 offset
 StorePut
 namespace
 key
 value
 index
 StoreDelete
 namespace
 key
 on
 threads
 create
 create_run
 read
 update
 delete
 search
 assistants
 create
 read
 update
 delete
 search
 crons
 create
 read
 update
 delete
 search
 store
 put
 get
 search
 delete
 list_namespaces
 HTTPException
Python SDK Reference¶
The LangGraph client implementations connect to the LangGraph API.

This module provides both asynchronous (get_client(url="http://localhost:2024")) or LangGraphClient) and synchronous (get_sync_client(url="http://localhost:2024")) or SyncLanggraphClient) clients to interacting with the LangGraph API's core resources such as Assistants, Threads, Runs, and Cron jobs, as well as its persistent document Store.

Classes:

Name	Description
LangGraphClient	Top-level client for LangGraph API.
HttpClient	Handle async requests to the LangGraph API.
AssistantsClient	Client for managing assistants in LangGraph.
ThreadsClient	Client for managing threads in LangGraph.
RunsClient	Client for managing runs in LangGraph.
CronClient	Client for managing recurrent runs (cron jobs) in LangGraph.
StoreClient	Client for interacting with the graph's shared storage.
SyncLangGraphClient	Synchronous client for interacting with the LangGraph API.
SyncHttpClient	Handle synchronous requests to the LangGraph API.
SyncAssistantsClient	Client for managing assistants in LangGraph synchronously.
SyncThreadsClient	Synchronous client for managing threads in LangGraph.
SyncRunsClient	Synchronous client for managing runs in LangGraph.
SyncCronClient	Synchronous client for managing cron jobs in LangGraph.
SyncStoreClient	A client for synchronous operations on a key-value store.
Functions:

Name	Description
get_client	Get a LangGraphClient instance.
get_sync_client	Get a synchronous LangGraphClient instance.
 LangGraphClient ¶
Top-level client for LangGraph API.

Attributes:

Name	Type	Description
assistants		Manages versioned configuration for your graphs.
threads		Handles (potentially) multi-turn interactions, such as conversational threads.
runs		Controls individual invocations of the graph.
crons		Manages scheduled operations.
store		Interfaces with persistent, shared data storage.
 HttpClient ¶
Handle async requests to the LangGraph API.

Adds additional error messaging & content handling above the provided httpx client.

Attributes:

Name	Type	Description
client	AsyncClient	Underlying HTTPX async client.
Methods:

Name	Description
get	Send a GET request.
post	Send a POST request.
put	Send a PUT request.
patch	Send a PATCH request.
delete	Send a DELETE request.
stream	Stream results using SSE.
 get async ¶

get(
    path: str,
    *,
    params: QueryParamTypes | None = None,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Any
Send a GET request.

 post async ¶

post(
    path: str,
    *,
    json: dict | None,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Any
Send a POST request.

 put async ¶

put(
    path: str,
    *,
    json: dict,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Any
Send a PUT request.

 patch async ¶

patch(
    path: str,
    *,
    json: dict,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Any
Send a PATCH request.

 delete async ¶

delete(
    path: str,
    *,
    json: Any | None = None,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> None
Send a DELETE request.

 stream async ¶

stream(
    path: str,
    method: str,
    *,
    json: dict | None = None,
    params: QueryParamTypes | None = None,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> AsyncIterator[StreamPart]
Stream results using SSE.

 AssistantsClient ¶
Client for managing assistants in LangGraph.

This class provides methods to interact with assistants, which are versioned configurations of your graph.

Example

client = get_client(url="http://localhost:2024")
assistant = await client.assistants.get("assistant_id_123")
Methods:

Name	Description
get	Get an assistant by ID.
get_graph	Get the graph of an assistant by ID.
get_schemas	Get the schemas of an assistant by ID.
get_subgraphs	Get the schemas of an assistant by ID.
create	Create a new assistant.
update	Update an assistant.
delete	Delete an assistant.
search	Search for assistants.
get_versions	List all versions of an assistant.
set_latest	Change the version of an assistant.
 get async ¶

get(
    assistant_id: str,
    *,
    headers: dict[str, str] | None = None
) -> Assistant
Get an assistant by ID.

Parameters:

Name	Type	Description	Default
assistant_id	str	The ID of the assistant to get.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Assistant	Assistant	Assistant Object.
Example Usage

assistant = await client.assistants.get(
    assistant_id="my_assistant_id"
)
print(assistant)

----------------------------------------------------

{
    'assistant_id': 'my_assistant_id',
    'graph_id': 'agent',
    'created_at': '2024-06-25T17:10:33.109781+00:00',
    'updated_at': '2024-06-25T17:10:33.109781+00:00',
    'config': {},
    'metadata': {'created_by': 'system'},
    'version': 1,
    'name': 'my_assistant'
}
 get_graph async ¶

get_graph(
    assistant_id: str,
    *,
    xray: int | bool = False,
    headers: dict[str, str] | None = None
) -> dict[str, list[dict[str, Any]]]
Get the graph of an assistant by ID.

Parameters:

Name	Type	Description	Default
assistant_id	str	The ID of the assistant to get the graph of.	required
xray	int | bool	Include graph representation of subgraphs. If an integer value is provided, only subgraphs with a depth less than or equal to the value will be included.	False
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Graph	dict[str, list[dict[str, Any]]]	The graph information for the assistant in JSON format.
Example Usage

client = get_client(url="http://localhost:2024")
graph_info = await client.assistants.get_graph(
    assistant_id="my_assistant_id"
)
print(graph_info)

--------------------------------------------------------------------------------------------------------------------------

{
    'nodes':
        [
            {'id': '__start__', 'type': 'schema', 'data': '__start__'},
            {'id': '__end__', 'type': 'schema', 'data': '__end__'},
            {'id': 'agent','type': 'runnable','data': {'id': ['langgraph', 'utils', 'RunnableCallable'],'name': 'agent'}},
        ],
    'edges':
        [
            {'source': '__start__', 'target': 'agent'},
            {'source': 'agent','target': '__end__'}
        ]
}
 get_schemas async ¶

get_schemas(
    assistant_id: str,
    *,
    headers: dict[str, str] | None = None
) -> GraphSchema
Get the schemas of an assistant by ID.

Parameters:

Name	Type	Description	Default
assistant_id	str	The ID of the assistant to get the schema of.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
GraphSchema	GraphSchema	The graph schema for the assistant.
Example Usage

client = get_client(url="http://localhost:2024")
schema = await client.assistants.get_schemas(
    assistant_id="my_assistant_id"
)
print(schema)

----------------------------------------------------------------------------------------------------------------------------

{
    'graph_id': 'agent',
    'state_schema':
        {
            'title': 'LangGraphInput',
            '$ref': '#/definitions/AgentState',
            'definitions':
                {
                    'BaseMessage':
                        {
                            'title': 'BaseMessage',
                            'description': 'Base abstract Message class. Messages are the inputs and outputs of ChatModels.',
                            'type': 'object',
                            'properties':
                                {
                                 'content':
                                    {
                                        'title': 'Content',
                                        'anyOf': [
                                            {'type': 'string'},
                                            {'type': 'array','items': {'anyOf': [{'type': 'string'}, {'type': 'object'}]}}
                                        ]
                                    },
                                'additional_kwargs':
                                    {
                                        'title': 'Additional Kwargs',
                                        'type': 'object'
                                    },
                                'response_metadata':
                                    {
                                        'title': 'Response Metadata',
                                        'type': 'object'
                                    },
                                'type':
                                    {
                                        'title': 'Type',
                                        'type': 'string'
                                    },
                                'name':
                                    {
                                        'title': 'Name',
                                        'type': 'string'
                                    },
                                'id':
                                    {
                                        'title': 'Id',
                                        'type': 'string'
                                    }
                                },
                            'required': ['content', 'type']
                        },
                    'AgentState':
                        {
                            'title': 'AgentState',
                            'type': 'object',
                            'properties':
                                {
                                    'messages':
                                        {
                                            'title': 'Messages',
                                            'type': 'array',
                                            'items': {'$ref': '#/definitions/BaseMessage'}
                                        }
                                },
                            'required': ['messages']
                        }
                }
        },
    'context_schema':
        {
            'title': 'Context',
            'type': 'object',
            'properties':
                {
                    'model_name':
                        {
                            'title': 'Model Name',
                            'enum': ['anthropic', 'openai'],
                            'type': 'string'
                        }
                }
        }
}
 get_subgraphs async ¶

get_subgraphs(
    assistant_id: str,
    namespace: str | None = None,
    recurse: bool = False,
    *,
    headers: dict[str, str] | None = None
) -> Subgraphs
Get the schemas of an assistant by ID.

Parameters:

Name	Type	Description	Default
assistant_id	str	The ID of the assistant to get the schema of.	required
namespace	str | None	Optional namespace to filter by.	None
recurse	bool	Whether to recursively get subgraphs.	False
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Subgraphs	Subgraphs	The graph schema for the assistant.
 create async ¶

create(
    graph_id: str | None,
    config: Config | None = None,
    *,
    context: Context | None = None,
    metadata: Json = None,
    assistant_id: str | None = None,
    if_exists: OnConflictBehavior | None = None,
    name: str | None = None,
    headers: dict[str, str] | None = None,
    description: str | None = None
) -> Assistant
Create a new assistant.

Useful when graph is configurable and you want to create different assistants based on different configurations.

Parameters:

Name	Type	Description	Default
graph_id	str | None	The ID of the graph the assistant should use. The graph ID is normally set in your langgraph.json configuration.	required
config	Config | None	Configuration to use for the graph.	None
metadata	Json	Metadata to add to assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
assistant_id	str | None	Assistant ID to use, will default to a random UUID if not provided.	None
if_exists	OnConflictBehavior | None	How to handle duplicate creation. Defaults to 'raise' under the hood. Must be either 'raise' (raise error if duplicate), or 'do_nothing' (return existing assistant).	None
name	str | None	The name of the assistant. Defaults to 'Untitled' under the hood.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
description	str | None	Optional description of the assistant. The description field is available for langgraph-api server version>=0.0.45	None
Returns:

Name	Type	Description
Assistant	Assistant	The created assistant.
Example Usage

client = get_client(url="http://localhost:2024")
assistant = await client.assistants.create(
    graph_id="agent",
    context={"model_name": "openai"},
    metadata={"number":1},
    assistant_id="my-assistant-id",
    if_exists="do_nothing",
    name="my_name"
)
 update async ¶

update(
    assistant_id: str,
    *,
    graph_id: str | None = None,
    config: Config | None = None,
    context: Context | None = None,
    metadata: Json = None,
    name: str | None = None,
    headers: dict[str, str] | None = None,
    description: str | None = None
) -> Assistant
Update an assistant.

Use this to point to a different graph, update the configuration, or change the metadata of an assistant.

Parameters:

Name	Type	Description	Default
assistant_id	str	Assistant to update.	required
graph_id	str | None	The ID of the graph the assistant should use. The graph ID is normally set in your langgraph.json configuration. If None, assistant will keep pointing to same graph.	None
config	Config | None	Configuration to use for the graph.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
metadata	Json	Metadata to merge with existing assistant metadata.	None
name	str | None	The new name for the assistant.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
description	str | None	Optional description of the assistant. The description field is available for langgraph-api server version>=0.0.45	None
Returns:

Name	Type	Description
Assistant	Assistant	The updated assistant.
Example Usage

client = get_client(url="http://localhost:2024")
assistant = await client.assistants.update(
    assistant_id='e280dad7-8618-443f-87f1-8e41841c180f',
    graph_id="other-graph",
    context={"model_name": "anthropic"},
    metadata={"number":2}
)
 delete async ¶

delete(
    assistant_id: str,
    *,
    headers: dict[str, str] | None = None
) -> None
Delete an assistant.

Parameters:

Name	Type	Description	Default
assistant_id	str	The assistant ID to delete.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_client(url="http://localhost:2024")
await client.assistants.delete(
    assistant_id="my_assistant_id"
)
 search async ¶

search(
    *,
    metadata: Json = None,
    graph_id: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: AssistantSortBy | None = None,
    sort_order: SortOrder | None = None,
    headers: dict[str, str] | None = None
) -> list[Assistant]
Search for assistants.

Parameters:

Name	Type	Description	Default
metadata	Json	Metadata to filter by. Exact match filter for each KV pair.	None
graph_id	str | None	The ID of the graph to filter by. The graph ID is normally set in your langgraph.json configuration.	None
limit	int	The maximum number of results to return.	10
offset	int	The number of results to skip.	0
sort_by	AssistantSortBy | None	The field to sort by.	None
sort_order	SortOrder | None	The order to sort by.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[Assistant]	list[Assistant]: A list of assistants.
Example Usage

client = get_client(url="http://localhost:2024")
assistants = await client.assistants.search(
    metadata = {"name":"my_name"},
    graph_id="my_graph_id",
    limit=5,
    offset=5
)
 get_versions async ¶

get_versions(
    assistant_id: str,
    metadata: Json = None,
    limit: int = 10,
    offset: int = 0,
    *,
    headers: dict[str, str] | None = None
) -> list[AssistantVersion]
List all versions of an assistant.

Parameters:

Name	Type	Description	Default
assistant_id	str	The assistant ID to get versions for.	required
metadata	Json	Metadata to filter versions by. Exact match filter for each KV pair.	None
limit	int	The maximum number of versions to return.	10
offset	int	The number of versions to skip.	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[AssistantVersion]	list[AssistantVersion]: A list of assistant versions.
Example Usage

client = get_client(url="http://localhost:2024")
assistant_versions = await client.assistants.get_versions(
    assistant_id="my_assistant_id"
)
 set_latest async ¶

set_latest(
    assistant_id: str,
    version: int,
    *,
    headers: dict[str, str] | None = None
) -> Assistant
Change the version of an assistant.

Parameters:

Name	Type	Description	Default
assistant_id	str	The assistant ID to delete.	required
version	int	The version to change to.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Assistant	Assistant	Assistant Object.
Example Usage

client = get_client(url="http://localhost:2024")
new_version_assistant = await client.assistants.set_latest(
    assistant_id="my_assistant_id",
    version=3
)
 ThreadsClient ¶
Client for managing threads in LangGraph.

A thread maintains the state of a graph across multiple interactions/invocations (aka runs). It accumulates and persists the graph's state, allowing for continuity between separate invocations of the graph.

Example

client = get_client(url="http://localhost:2024"))
new_thread = await client.threads.create(metadata={"user_id": "123"})
Methods:

Name	Description
get	Get a thread by ID.
create	Create a new thread.
update	Update a thread.
delete	Delete a thread.
search	Search for threads.
copy	Copy a thread.
get_state	Get the state of a thread.
update_state	Update the state of a thread.
get_history	Get the state history of a thread.
 get async ¶

get(
    thread_id: str, *, headers: dict[str, str] | None = None
) -> Thread
Get a thread by ID.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to get.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Thread	Thread	Thread object.
Example Usage

client = get_client(url="http://localhost:2024")
thread = await client.threads.get(
    thread_id="my_thread_id"
)
print(thread)

-----------------------------------------------------

{
    'thread_id': 'my_thread_id',
    'created_at': '2024-07-18T18:35:15.540834+00:00',
    'updated_at': '2024-07-18T18:35:15.540834+00:00',
    'metadata': {'graph_id': 'agent'}
}
 create async ¶

create(
    *,
    metadata: Json = None,
    thread_id: str | None = None,
    if_exists: OnConflictBehavior | None = None,
    supersteps: (
        Sequence[dict[str, Sequence[dict[str, Any]]]] | None
    ) = None,
    graph_id: str | None = None,
    headers: dict[str, str] | None = None
) -> Thread
Create a new thread.

Parameters:

Name	Type	Description	Default
metadata	Json	Metadata to add to thread.	None
thread_id	str | None	ID of thread. If None, ID will be a randomly generated UUID.	None
if_exists	OnConflictBehavior | None	How to handle duplicate creation. Defaults to 'raise' under the hood. Must be either 'raise' (raise error if duplicate), or 'do_nothing' (return existing thread).	None
supersteps	Sequence[dict[str, Sequence[dict[str, Any]]]] | None	Apply a list of supersteps when creating a thread, each containing a sequence of updates. Each update has values or command and as_node. Used for copying a thread between deployments.	None
graph_id	str | None	Optional graph ID to associate with the thread.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Thread	Thread	The created thread.
Example Usage

client = get_client(url="http://localhost:2024")
thread = await client.threads.create(
    metadata={"number":1},
    thread_id="my-thread-id",
    if_exists="raise"
)
 update async ¶

update(
    thread_id: str,
    *,
    metadata: dict[str, Any],
    headers: dict[str, str] | None = None
) -> Thread
Update a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	ID of thread to update.	required
metadata	dict[str, Any]	Metadata to merge with existing thread metadata.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Thread	Thread	The created thread.
Example Usage

client = get_client(url="http://localhost:2024")
thread = await client.threads.update(
    thread_id="my-thread-id",
    metadata={"number":1},
)
 delete async ¶

delete(
    thread_id: str, *, headers: dict[str, str] | None = None
) -> None
Delete a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to delete.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_client(url="http://localhost2024)
await client.threads.delete(
    thread_id="my_thread_id"
)
 search async ¶

search(
    *,
    metadata: Json = None,
    values: Json = None,
    status: ThreadStatus | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: ThreadSortBy | None = None,
    sort_order: SortOrder | None = None,
    headers: dict[str, str] | None = None
) -> list[Thread]
Search for threads.

Parameters:

Name	Type	Description	Default
metadata	Json	Thread metadata to filter on.	None
values	Json	State values to filter on.	None
status	ThreadStatus | None	Thread status to filter on. Must be one of 'idle', 'busy', 'interrupted' or 'error'.	None
limit	int	Limit on number of threads to return.	10
offset	int	Offset in threads table to start search from.	0
sort_by	ThreadSortBy | None	Sort by field.	None
sort_order	SortOrder | None	Sort order.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[Thread]	list[Thread]: List of the threads matching the search parameters.
Example Usage

client = get_client(url="http://localhost:2024")
threads = await client.threads.search(
    metadata={"number":1},
    status="interrupted",
    limit=15,
    offset=5
)
 copy async ¶

copy(
    thread_id: str, *, headers: dict[str, str] | None = None
) -> None
Copy a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to copy.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_client(url="http://localhost:2024)
await client.threads.copy(
    thread_id="my_thread_id"
)
 get_state async ¶

get_state(
    thread_id: str,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    *,
    subgraphs: bool = False,
    headers: dict[str, str] | None = None
) -> ThreadState
Get the state of a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to get the state of.	required
checkpoint	Checkpoint | None	The checkpoint to get the state of.	None
checkpoint_id	str | None	(deprecated) The checkpoint ID to get the state of.	None
subgraphs	bool	Include subgraphs states.	False
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
ThreadState	ThreadState	the thread of the state.
Example Usage

client = get_client(url="http://localhost:2024)
thread_state = await client.threads.get_state(
    thread_id="my_thread_id",
    checkpoint_id="my_checkpoint_id"
)
print(thread_state)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

{
    'values': {
        'messages': [
            {
                'content': 'how are you?',
                'additional_kwargs': {},
                'response_metadata': {},
                'type': 'human',
                'name': None,
                'id': 'fe0a5778-cfe9-42ee-b807-0adaa1873c10',
                'example': False
            },
            {
                'content': "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, honest, and harmless.",
                'additional_kwargs': {},
                'response_metadata': {},
                'type': 'ai',
                'name': None,
                'id': 'run-159b782c-b679-4830-83c6-cef87798fe8b',
                'example': False,
                'tool_calls': [],
                'invalid_tool_calls': [],
                'usage_metadata': None
            }
        ]
    },
    'next': [],
    'checkpoint':
        {
            'thread_id': 'e2496803-ecd5-4e0c-a779-3226296181c2',
            'checkpoint_ns': '',
            'checkpoint_id': '1ef4a9b8-e6fb-67b1-8001-abd5184439d1'
        }
    'metadata':
        {
            'step': 1,
            'run_id': '1ef4a9b8-d7da-679a-a45a-872054341df2',
            'source': 'loop',
            'writes':
                {
                    'agent':
                        {
                            'messages': [
                                {
                                    'id': 'run-159b782c-b679-4830-83c6-cef87798fe8b',
                                    'name': None,
                                    'type': 'ai',
                                    'content': "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, honest, and harmless.",
                                    'example': False,
                                    'tool_calls': [],
                                    'usage_metadata': None,
                                    'additional_kwargs': {},
                                    'response_metadata': {},
                                    'invalid_tool_calls': []
                                }
                            ]
                        }
                },
    'user_id': None,
    'graph_id': 'agent',
    'thread_id': 'e2496803-ecd5-4e0c-a779-3226296181c2',
    'created_by': 'system',
    'assistant_id': 'fe096781-5601-53d2-b2f6-0d3403f7e9ca'},
    'created_at': '2024-07-25T15:35:44.184703+00:00',
    'parent_config':
        {
            'thread_id': 'e2496803-ecd5-4e0c-a779-3226296181c2',
            'checkpoint_ns': '',
            'checkpoint_id': '1ef4a9b8-d80d-6fa7-8000-9300467fad0f'
        }
}
 update_state async ¶

update_state(
    thread_id: str,
    values: dict | Sequence[dict] | None,
    *,
    as_node: str | None = None,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    headers: dict[str, str] | None = None
) -> ThreadUpdateStateResponse
Update the state of a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to update.	required
values	dict | Sequence[dict] | None	The values to update the state with.	required
as_node	str | None	Update the state as if this node had just executed.	None
checkpoint	Checkpoint | None	The checkpoint to update the state of.	None
checkpoint_id	str | None	(deprecated) The checkpoint ID to update the state of.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
ThreadUpdateStateResponse	ThreadUpdateStateResponse	Response after updating a thread's state.
Example Usage

client = get_client(url="http://localhost:2024)
response = await client.threads.update_state(
    thread_id="my_thread_id",
    values={"messages":[{"role": "user", "content": "hello!"}]},
    as_node="my_node",
)
print(response)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

{
    'checkpoint': {
        'thread_id': 'e2496803-ecd5-4e0c-a779-3226296181c2',
        'checkpoint_ns': '',
        'checkpoint_id': '1ef4a9b8-e6fb-67b1-8001-abd5184439d1',
        'checkpoint_map': {}
    }
}
 get_history async ¶

get_history(
    thread_id: str,
    *,
    limit: int = 10,
    before: str | Checkpoint | None = None,
    metadata: dict | None = None,
    checkpoint: Checkpoint | None = None,
    headers: dict[str, str] | None = None
) -> list[ThreadState]
Get the state history of a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to get the state history for.	required
checkpoint	Checkpoint | None	Return states for this subgraph. If empty defaults to root.	None
limit	int	The maximum number of states to return.	10
before	str | Checkpoint | None	Return states before this checkpoint.	None
metadata	dict | None	Filter states by metadata key-value pairs.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[ThreadState]	list[ThreadState]: the state history of the thread.
Example Usage

client = get_client(url="http://localhost:2024)
thread_state = await client.threads.get_history(
    thread_id="my_thread_id",
    limit=5,
)
 RunsClient ¶
Client for managing runs in LangGraph.

A run is a single assistant invocation with optional input, config, context, and metadata. This client manages runs, which can be stateful (on threads) or stateless.

Example

client = get_client(url="http://localhost:2024")
run = await client.runs.create(assistant_id="asst_123", thread_id="thread_456", input={"query": "Hello"})
Methods:

Name	Description
stream	Create a run and stream the results.
create	Create a background run.
create_batch	Create a batch of stateless background runs.
wait	Create a run, wait until it finishes and return the final state.
list	List runs.
get	Get a run.
cancel	Get a run.
join	Block until a run is done. Returns the final state of the thread.
join_stream	Stream output from a run in real-time, until the run is done.
delete	Delete a run.
 stream ¶

stream(
    thread_id: str | None,
    assistant_id: str,
    *,
    input: dict | None = None,
    command: Command | None = None,
    stream_mode: (
        StreamMode | Sequence[StreamMode]
    ) = "values",
    stream_subgraphs: bool = False,
    stream_resumable: bool = False,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    checkpoint_during: bool | None = None,
    interrupt_before: All | Sequence[str] | None = None,
    interrupt_after: All | Sequence[str] | None = None,
    feedback_keys: Sequence[str] | None = None,
    on_disconnect: DisconnectMode | None = None,
    on_completion: OnCompletionBehavior | None = None,
    webhook: str | None = None,
    multitask_strategy: MultitaskStrategy | None = None,
    if_not_exists: IfNotExists | None = None,
    after_seconds: int | None = None,
    headers: dict[str, str] | None = None,
    on_run_created: (
        Callable[[RunCreateMetadata], None] | None
    ) = None
) -> AsyncIterator[StreamPart]
Create a run and stream the results.

Parameters:

Name	Type	Description	Default
thread_id	str | None	the thread ID to assign to the thread. If None will create a stateless run.	required
assistant_id	str	The assistant ID or graph name to stream from. If using graph name, will default to first assistant created from that graph.	required
input	dict | None	The input to the graph.	None
command	Command | None	A command to execute. Cannot be combined with input.	None
stream_mode	StreamMode | Sequence[StreamMode]	The stream mode(s) to use.	'values'
stream_subgraphs	bool	Whether to stream output from subgraphs.	False
stream_resumable	bool	Whether the stream is considered resumable. If true, the stream can be resumed and replayed in its entirety even after disconnection.	False
metadata	dict | None	Metadata to assign to the run.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint	Checkpoint | None	The checkpoint to resume from.	None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | Sequence[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | Sequence[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
feedback_keys	Sequence[str] | None	Feedback keys to assign to run.	None
on_disconnect	DisconnectMode | None	The disconnect mode to use. Must be one of 'cancel' or 'continue'.	None
on_completion	OnCompletionBehavior | None	Whether to delete or keep the thread created for a stateless run. Must be one of 'delete' or 'keep'.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
multitask_strategy	MultitaskStrategy | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
if_not_exists	IfNotExists | None	How to handle missing thread. Defaults to 'reject'. Must be either 'reject' (raise error if missing), or 'create' (create new thread).	None
after_seconds	int | None	The number of seconds to wait before starting the run. Use to schedule future runs.	None
on_run_created	Callable[[RunCreateMetadata], None] | None	Callback when a run is created.	None
Returns:

Type	Description
AsyncIterator[StreamPart]	AsyncIterator[StreamPart]: Asynchronous iterator of stream results.
Example Usage

client = get_client(url="http://localhost:2024)
async for chunk in client.runs.stream(
    thread_id=None,
    assistant_id="agent",
    input={"messages": [{"role": "user", "content": "how are you?"}]},
    stream_mode=["values","debug"],
    metadata={"name":"my_run"},
    context={"model_name": "anthropic"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    feedback_keys=["my_feedback_key_1","my_feedback_key_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
):
    print(chunk)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

StreamPart(event='metadata', data={'run_id': '1ef4a9b8-d7da-679a-a45a-872054341df2'})
StreamPart(event='values', data={'messages': [{'content': 'how are you?', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': 'fe0a5778-cfe9-42ee-b807-0adaa1873c10', 'example': False}]})
StreamPart(event='values', data={'messages': [{'content': 'how are you?', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': 'fe0a5778-cfe9-42ee-b807-0adaa1873c10', 'example': False}, {'content': "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, honest, and harmless.", 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'ai', 'name': None, 'id': 'run-159b782c-b679-4830-83c6-cef87798fe8b', 'example': False, 'tool_calls': [], 'invalid_tool_calls': [], 'usage_metadata': None}]})
StreamPart(event='end', data=None)
 create async ¶

create(
    thread_id: str | None,
    assistant_id: str,
    *,
    input: dict | None = None,
    command: Command | None = None,
    stream_mode: (
        StreamMode | Sequence[StreamMode]
    ) = "values",
    stream_subgraphs: bool = False,
    stream_resumable: bool = False,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    checkpoint_during: bool | None = None,
    interrupt_before: All | Sequence[str] | None = None,
    interrupt_after: All | Sequence[str] | None = None,
    webhook: str | None = None,
    multitask_strategy: MultitaskStrategy | None = None,
    if_not_exists: IfNotExists | None = None,
    on_completion: OnCompletionBehavior | None = None,
    after_seconds: int | None = None,
    headers: dict[str, str] | None = None,
    on_run_created: (
        Callable[[RunCreateMetadata], None] | None
    ) = None
) -> Run
Create a background run.

Parameters:

Name	Type	Description	Default
thread_id	str | None	the thread ID to assign to the thread. If None will create a stateless run.	required
assistant_id	str	The assistant ID or graph name to stream from. If using graph name, will default to first assistant created from that graph.	required
input	dict | None	The input to the graph.	None
command	Command | None	A command to execute. Cannot be combined with input.	None
stream_mode	StreamMode | Sequence[StreamMode]	The stream mode(s) to use.	'values'
stream_subgraphs	bool	Whether to stream output from subgraphs.	False
stream_resumable	bool	Whether the stream is considered resumable. If true, the stream can be resumed and replayed in its entirety even after disconnection.	False
metadata	dict | None	Metadata to assign to the run.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint	Checkpoint | None	The checkpoint to resume from.	None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | Sequence[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | Sequence[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
multitask_strategy	MultitaskStrategy | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
on_completion	OnCompletionBehavior | None	Whether to delete or keep the thread created for a stateless run. Must be one of 'delete' or 'keep'.	None
if_not_exists	IfNotExists | None	How to handle missing thread. Defaults to 'reject'. Must be either 'reject' (raise error if missing), or 'create' (create new thread).	None
after_seconds	int | None	The number of seconds to wait before starting the run. Use to schedule future runs.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
on_run_created	Callable[[RunCreateMetadata], None] | None	Optional callback to call when a run is created.	None
Returns:

Name	Type	Description
Run	Run	The created background run.
Example Usage

background_run = await client.runs.create(
    thread_id="my_thread_id",
    assistant_id="my_assistant_id",
    input={"messages": [{"role": "user", "content": "hello!"}]},
    metadata={"name":"my_run"},
    context={"model_name": "openai"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
)
print(background_run)

--------------------------------------------------------------------------------

{
    'run_id': 'my_run_id',
    'thread_id': 'my_thread_id',
    'assistant_id': 'my_assistant_id',
    'created_at': '2024-07-25T15:35:42.598503+00:00',
    'updated_at': '2024-07-25T15:35:42.598503+00:00',
    'metadata': {},
    'status': 'pending',
    'kwargs':
        {
            'input':
                {
                    'messages': [
                        {
                            'role': 'user',
                            'content': 'how are you?'
                        }
                    ]
                },
            'config':
                {
                    'metadata':
                        {
                            'created_by': 'system'
                        },
                    'configurable':
                        {
                            'run_id': 'my_run_id',
                            'user_id': None,
                            'graph_id': 'agent',
                            'thread_id': 'my_thread_id',
                            'checkpoint_id': None,
                            'assistant_id': 'my_assistant_id'
                        },
                },
            'context':
                {
                    'model_name': 'openai'
                }
            'webhook': "https://my.fake.webhook.com",
            'temporary': False,
            'stream_mode': ['values'],
            'feedback_keys': None,
            'interrupt_after': ["node_to_stop_after_1","node_to_stop_after_2"],
            'interrupt_before': ["node_to_stop_before_1","node_to_stop_before_2"]
        },
    'multitask_strategy': 'interrupt'
}
 create_batch async ¶

create_batch(payloads: list[RunCreate]) -> list[Run]
Create a batch of stateless background runs.

 wait async ¶

wait(
    thread_id: str | None,
    assistant_id: str,
    *,
    input: dict | None = None,
    command: Command | None = None,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    checkpoint_during: bool | None = None,
    interrupt_before: All | Sequence[str] | None = None,
    interrupt_after: All | Sequence[str] | None = None,
    webhook: str | None = None,
    on_disconnect: DisconnectMode | None = None,
    on_completion: OnCompletionBehavior | None = None,
    multitask_strategy: MultitaskStrategy | None = None,
    if_not_exists: IfNotExists | None = None,
    after_seconds: int | None = None,
    raise_error: bool = True,
    headers: dict[str, str] | None = None,
    on_run_created: (
        Callable[[RunCreateMetadata], None] | None
    ) = None
) -> list[dict] | dict[str, Any]
Create a run, wait until it finishes and return the final state.

Parameters:

Name	Type	Description	Default
thread_id	str | None	the thread ID to create the run on. If None will create a stateless run.	required
assistant_id	str	The assistant ID or graph name to run. If using graph name, will default to first assistant created from that graph.	required
input	dict | None	The input to the graph.	None
command	Command | None	A command to execute. Cannot be combined with input.	None
metadata	dict | None	Metadata to assign to the run.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint	Checkpoint | None	The checkpoint to resume from.	None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | Sequence[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | Sequence[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
on_disconnect	DisconnectMode | None	The disconnect mode to use. Must be one of 'cancel' or 'continue'.	None
on_completion	OnCompletionBehavior | None	Whether to delete or keep the thread created for a stateless run. Must be one of 'delete' or 'keep'.	None
multitask_strategy	MultitaskStrategy | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
if_not_exists	IfNotExists | None	How to handle missing thread. Defaults to 'reject'. Must be either 'reject' (raise error if missing), or 'create' (create new thread).	None
after_seconds	int | None	The number of seconds to wait before starting the run. Use to schedule future runs.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
on_run_created	Callable[[RunCreateMetadata], None] | None	Optional callback to call when a run is created.	None
Returns:

Type	Description
list[dict] | dict[str, Any]	Union[list[dict], dict[str, Any]]: The output of the run.
Example Usage

client = get_client(url="http://localhost:2024")
final_state_of_run = await client.runs.wait(
    thread_id=None,
    assistant_id="agent",
    input={"messages": [{"role": "user", "content": "how are you?"}]},
    metadata={"name":"my_run"},
    context={"model_name": "anthropic"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
)
print(final_state_of_run)

-------------------------------------------------------------------------------------------------------------------------------------------

{
    'messages': [
        {
            'content': 'how are you?',
            'additional_kwargs': {},
            'response_metadata': {},
            'type': 'human',
            'name': None,
            'id': 'f51a862c-62fe-4866-863b-b0863e8ad78a',
            'example': False
        },
        {
            'content': "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, honest, and harmless.",
            'additional_kwargs': {},
            'response_metadata': {},
            'type': 'ai',
            'name': None,
            'id': 'run-bf1cd3c6-768f-4c16-b62d-ba6f17ad8b36',
            'example': False,
            'tool_calls': [],
            'invalid_tool_calls': [],
            'usage_metadata': None
        }
    ]
}
 list async ¶

list(
    thread_id: str,
    *,
    limit: int = 10,
    offset: int = 0,
    status: RunStatus | None = None,
    headers: dict[str, str] | None = None
) -> list[Run]
List runs.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to list runs for.	required
limit	int	The maximum number of results to return.	10
offset	int	The number of results to skip.	0
status	RunStatus | None	The status of the run to filter by.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[Run]	list[Run]: The runs for the thread.
Example Usage

client = get_client(url="http://localhost:2024")
await client.runs.list(
    thread_id="thread_id",
    limit=5,
    offset=5,
)
 get async ¶

get(
    thread_id: str,
    run_id: str,
    *,
    headers: dict[str, str] | None = None
) -> Run
Get a run.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to get.	required
run_id	str	The run ID to get.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Run	Run	Run object.
Example Usage

client = get_client(url="http://localhost:2024")
run = await client.runs.get(
    thread_id="thread_id_to_delete",
    run_id="run_id_to_delete",
)
 cancel async ¶

cancel(
    thread_id: str,
    run_id: str,
    *,
    wait: bool = False,
    action: CancelAction = "interrupt",
    headers: dict[str, str] | None = None
) -> None
Get a run.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to cancel.	required
run_id	str	The run ID to cancel.	required
wait	bool	Whether to wait until run has completed.	False
action	CancelAction	Action to take when cancelling the run. Possible values are interrupt or rollback. Default is interrupt.	'interrupt'
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_client(url="http://localhost:2024")
await client.runs.cancel(
    thread_id="thread_id_to_cancel",
    run_id="run_id_to_cancel",
    wait=True,
    action="interrupt"
)
 join async ¶

join(
    thread_id: str,
    run_id: str,
    *,
    headers: dict[str, str] | None = None
) -> dict
Block until a run is done. Returns the final state of the thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to join.	required
run_id	str	The run ID to join.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
dict	None
Example Usage

client = get_client(url="http://localhost:2024")
result =await client.runs.join(
    thread_id="thread_id_to_join",
    run_id="run_id_to_join"
)
 join_stream ¶

join_stream(
    thread_id: str,
    run_id: str,
    *,
    cancel_on_disconnect: bool = False,
    stream_mode: (
        StreamMode | Sequence[StreamMode] | None
    ) = None,
    headers: dict[str, str] | None = None,
    last_event_id: str | None = None
) -> AsyncIterator[StreamPart]
Stream output from a run in real-time, until the run is done. Output is not buffered, so any output produced before this call will not be received here.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to join.	required
run_id	str	The run ID to join.	required
cancel_on_disconnect	bool	Whether to cancel the run when the stream is disconnected.	False
stream_mode	StreamMode | Sequence[StreamMode] | None	The stream mode(s) to use. Must be a subset of the stream modes passed when creating the run. Background runs default to having the union of all stream modes.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
AsyncIterator[StreamPart]	None
Example Usage

client = get_client(url="http://localhost:2024")
async for part in client.runs.join_stream(
    thread_id="thread_id_to_join",
    run_id="run_id_to_join",
    stream_mode=["values", "debug"]
):
    print(part)
 delete async ¶

delete(
    thread_id: str,
    run_id: str,
    *,
    headers: dict[str, str] | None = None
) -> None
Delete a run.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to delete.	required
run_id	str	The run ID to delete.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_client(url="http://localhost:2024")
await client.runs.delete(
    thread_id="thread_id_to_delete",
    run_id="run_id_to_delete"
)
 CronClient ¶
Client for managing recurrent runs (cron jobs) in LangGraph.

A run is a single invocation of an assistant with optional input, config, and context. This client allows scheduling recurring runs to occur automatically.

Example Usage

client = get_client(url="http://localhost:2024"))
cron_job = await client.crons.create_for_thread(
    thread_id="thread_123",
    assistant_id="asst_456",
    schedule="0 9 * * *",
    input={"message": "Daily update"}
)
Feature Availability

The crons client functionality is not supported on all licenses. Please check the relevant license documentation for the most up-to-date details on feature availability.

Methods:

Name	Description
create_for_thread	Create a cron job for a thread.
create	Create a cron run.
delete	Delete a cron.
search	Get a list of cron jobs.
 create_for_thread async ¶

create_for_thread(
    thread_id: str,
    assistant_id: str,
    *,
    schedule: str,
    input: dict | None = None,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint_during: bool | None = None,
    interrupt_before: All | list[str] | None = None,
    interrupt_after: All | list[str] | None = None,
    webhook: str | None = None,
    multitask_strategy: str | None = None,
    headers: dict[str, str] | None = None
) -> Run
Create a cron job for a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	the thread ID to run the cron job on.	required
assistant_id	str	The assistant ID or graph name to use for the cron job. If using graph name, will default to first assistant created from that graph.	required
schedule	str	The cron schedule to execute this job on.	required
input	dict | None	The input to the graph.	None
metadata	dict | None	Metadata to assign to the cron job runs.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | list[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | list[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
multitask_strategy	str | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Run	Run	The cron run.
Example Usage

client = get_client(url="http://localhost:2024")
cron_run = await client.crons.create_for_thread(
    thread_id="my-thread-id",
    assistant_id="agent",
    schedule="27 15 * * *",
    input={"messages": [{"role": "user", "content": "hello!"}]},
    metadata={"name":"my_run"},
    context={"model_name": "openai"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
)
 create async ¶

create(
    assistant_id: str,
    *,
    schedule: str,
    input: dict | None = None,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint_during: bool | None = None,
    interrupt_before: All | list[str] | None = None,
    interrupt_after: All | list[str] | None = None,
    webhook: str | None = None,
    multitask_strategy: str | None = None,
    headers: dict[str, str] | None = None
) -> Run
Create a cron run.

Parameters:

Name	Type	Description	Default
assistant_id	str	The assistant ID or graph name to use for the cron job. If using graph name, will default to first assistant created from that graph.	required
schedule	str	The cron schedule to execute this job on.	required
input	dict | None	The input to the graph.	None
metadata	dict | None	Metadata to assign to the cron job runs.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | list[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | list[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
multitask_strategy	str | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Run	Run	The cron run.
Example Usage

client = get_client(url="http://localhost:2024")
cron_run = client.crons.create(
    assistant_id="agent",
    schedule="27 15 * * *",
    input={"messages": [{"role": "user", "content": "hello!"}]},
    metadata={"name":"my_run"},
    context={"model_name": "openai"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
)
 delete async ¶

delete(
    cron_id: str, headers: dict[str, str] | None = None
) -> None
Delete a cron.

Parameters:

Name	Type	Description	Default
cron_id	str	The cron ID to delete.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_client(url="http://localhost:2024")
await client.crons.delete(
    cron_id="cron_to_delete"
)
 search async ¶

search(
    *,
    assistant_id: str | None = None,
    thread_id: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: CronSortBy | None = None,
    sort_order: SortOrder | None = None,
    headers: dict[str, str] | None = None
) -> list[Cron]
Get a list of cron jobs.

Parameters:

Name	Type	Description	Default
assistant_id	str | None	The assistant ID or graph name to search for.	None
thread_id	str | None	the thread ID to search for.	None
limit	int	The maximum number of results to return.	10
offset	int	The number of results to skip.	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[Cron]	list[Cron]: The list of cron jobs returned by the search,
Example Usage

client = get_client(url="http://localhost:2024")
cron_jobs = await client.crons.search(
    assistant_id="my_assistant_id",
    thread_id="my_thread_id",
    limit=5,
    offset=5,
)
print(cron_jobs)

----------------------------------------------------------

[
    {
        'cron_id': '1ef3cefa-4c09-6926-96d0-3dc97fd5e39b',
        'assistant_id': 'my_assistant_id',
        'thread_id': 'my_thread_id',
        'user_id': None,
        'payload':
            {
                'input': {'start_time': ''},
                'schedule': '4 * * * *',
                'assistant_id': 'my_assistant_id'
            },
        'schedule': '4 * * * *',
        'next_run_date': '2024-07-25T17:04:00+00:00',
        'end_time': None,
        'created_at': '2024-07-08T06:02:23.073257+00:00',
        'updated_at': '2024-07-08T06:02:23.073257+00:00'
    }
]
 StoreClient ¶
Client for interacting with the graph's shared storage.

The Store provides a key-value storage system for persisting data across graph executions, allowing for stateful operations and data sharing across threads.

Example

client = get_client(url="http://localhost:2024")
await client.store.put_item(["users", "user123"], "mem-123451342", {"name": "Alice", "score": 100})
Methods:

Name	Description
put_item	Store or update an item.
get_item	Retrieve a single item.
delete_item	Delete an item.
search_items	Search for items within a namespace prefix.
list_namespaces	List namespaces with optional match conditions.
 put_item async ¶

put_item(
    namespace: Sequence[str],
    /,
    key: str,
    value: dict[str, Any],
    index: Literal[False] | list[str] | None = None,
    ttl: int | None = None,
    headers: dict[str, str] | None = None,
) -> None
Store or update an item.

Parameters:

Name	Type	Description	Default
namespace	Sequence[str]	A list of strings representing the namespace path.	required
key	str	The unique identifier for the item within the namespace.	required
value	dict[str, Any]	A dictionary containing the item's data.	required
index	Literal[False] | list[str] | None	Controls search indexing - None (use defaults), False (disable), or list of field paths to index.	None
ttl	int | None	Optional time-to-live in minutes for the item, or None for no expiration.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_client(url="http://localhost:2024")
await client.store.put_item(
    ["documents", "user123"],
    key="item456",
    value={"title": "My Document", "content": "Hello World"}
)
 get_item async ¶

get_item(
    namespace: Sequence[str],
    /,
    key: str,
    *,
    refresh_ttl: bool | None = None,
    headers: dict[str, str] | None = None,
) -> Item
Retrieve a single item.

Parameters:

Name	Type	Description	Default
key	str	The unique identifier for the item.	required
namespace	Sequence[str]	Optional list of strings representing the namespace path.	required
refresh_ttl	bool | None	Whether to refresh the TTL on this read operation. If None, uses the store's default behavior.	None
Returns:

Name	Type	Description
Item	Item	The retrieved item.
headers	Item	Optional custom headers to include with the request.
Example Usage

client = get_client(url="http://localhost:2024")
item = await client.store.get_item(
    ["documents", "user123"],
    key="item456",
)
print(item)

----------------------------------------------------------------

{
    'namespace': ['documents', 'user123'],
    'key': 'item456',
    'value': {'title': 'My Document', 'content': 'Hello World'},
    'created_at': '2024-07-30T12:00:00Z',
    'updated_at': '2024-07-30T12:00:00Z'
}
 delete_item async ¶

delete_item(
    namespace: Sequence[str],
    /,
    key: str,
    headers: dict[str, str] | None = None,
) -> None
Delete an item.

Parameters:

Name	Type	Description	Default
key	str	The unique identifier for the item.	required
namespace	Sequence[str]	Optional list of strings representing the namespace path.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_client(url="http://localhost:2024")
await client.store.delete_item(
    ["documents", "user123"],
    key="item456",
)
 search_items async ¶

search_items(
    namespace_prefix: Sequence[str],
    /,
    filter: dict[str, Any] | None = None,
    limit: int = 10,
    offset: int = 0,
    query: str | None = None,
    refresh_ttl: bool | None = None,
    headers: dict[str, str] | None = None,
) -> SearchItemsResponse
Search for items within a namespace prefix.

Parameters:

Name	Type	Description	Default
namespace_prefix	Sequence[str]	List of strings representing the namespace prefix.	required
filter	dict[str, Any] | None	Optional dictionary of key-value pairs to filter results.	None
limit	int	Maximum number of items to return (default is 10).	10
offset	int	Number of items to skip before returning results (default is 0).	0
query	str | None	Optional query for natural language search.	None
refresh_ttl	bool | None	Whether to refresh the TTL on items returned by this search. If None, uses the store's default behavior.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
SearchItemsResponse	list[Item]: A list of items matching the search criteria.
Example Usage

client = get_client(url="http://localhost:2024")
items = await client.store.search_items(
    ["documents"],
    filter={"author": "John Doe"},
    limit=5,
    offset=0
)
print(items)

----------------------------------------------------------------

{
    "items": [
        {
            "namespace": ["documents", "user123"],
            "key": "item789",
            "value": {
                "title": "Another Document",
                "author": "John Doe"
            },
            "created_at": "2024-07-30T12:00:00Z",
            "updated_at": "2024-07-30T12:00:00Z"
        },
        # ... additional items ...
    ]
}
 list_namespaces async ¶

list_namespaces(
    prefix: list[str] | None = None,
    suffix: list[str] | None = None,
    max_depth: int | None = None,
    limit: int = 100,
    offset: int = 0,
    headers: dict[str, str] | None = None,
) -> ListNamespaceResponse
List namespaces with optional match conditions.

Parameters:

Name	Type	Description	Default
prefix	list[str] | None	Optional list of strings representing the prefix to filter namespaces.	None
suffix	list[str] | None	Optional list of strings representing the suffix to filter namespaces.	None
max_depth	int | None	Optional integer specifying the maximum depth of namespaces to return.	None
limit	int	Maximum number of namespaces to return (default is 100).	100
offset	int	Number of namespaces to skip before returning results (default is 0).	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
ListNamespaceResponse	list[list[str]]: A list of namespaces matching the criteria.
Example Usage

client = get_client(url="http://localhost:2024")
namespaces = await client.store.list_namespaces(
    prefix=["documents"],
    max_depth=3,
    limit=10,
    offset=0
)
print(namespaces)

----------------------------------------------------------------

[
    ["documents", "user123", "reports"],
    ["documents", "user456", "invoices"],
    ...
]
 SyncLangGraphClient ¶
Synchronous client for interacting with the LangGraph API.

This class provides synchronous access to LangGraph API endpoints for managing assistants, threads, runs, cron jobs, and data storage.

Example

client = get_sync_client(url="http://localhost:2024")
assistant = client.assistants.get("asst_123")
 SyncHttpClient ¶
Handle synchronous requests to the LangGraph API.

Provides error messaging and content handling enhancements above the underlying httpx client, mirroring the interface of HttpClient but for sync usage.

Attributes:

Name	Type	Description
client	Client	Underlying HTTPX sync client.
Methods:

Name	Description
get	Send a GET request.
post	Send a POST request.
put	Send a PUT request.
patch	Send a PATCH request.
delete	Send a DELETE request.
stream	Stream the results of a request using SSE.
 get ¶

get(
    path: str,
    *,
    params: QueryParamTypes | None = None,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Any
Send a GET request.

 post ¶

post(
    path: str,
    *,
    json: dict | None,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Any
Send a POST request.

 put ¶

put(
    path: str,
    *,
    json: dict,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Any
Send a PUT request.

 patch ¶

patch(
    path: str,
    *,
    json: dict,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Any
Send a PATCH request.

 delete ¶

delete(
    path: str,
    *,
    json: Any | None = None,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> None
Send a DELETE request.

 stream ¶

stream(
    path: str,
    method: str,
    *,
    json: dict | None = None,
    params: QueryParamTypes | None = None,
    headers: dict[str, str] | None = None,
    on_response: Callable[[Response], None] | None = None
) -> Iterator[StreamPart]
Stream the results of a request using SSE.

 SyncAssistantsClient ¶
Client for managing assistants in LangGraph synchronously.

This class provides methods to interact with assistants, which are versioned configurations of your graph.

Examples

client = get_sync_client(url="http://localhost:2024")
assistant = client.assistants.get("assistant_id_123")
Methods:

Name	Description
get	Get an assistant by ID.
get_graph	Get the graph of an assistant by ID.
get_schemas	Get the schemas of an assistant by ID.
get_subgraphs	Get the schemas of an assistant by ID.
create	Create a new assistant.
update	Update an assistant.
delete	Delete an assistant.
search	Search for assistants.
get_versions	List all versions of an assistant.
set_latest	Change the version of an assistant.
 get ¶

get(
    assistant_id: str,
    *,
    headers: dict[str, str] | None = None
) -> Assistant
Get an assistant by ID.

Parameters:

Name	Type	Description	Default
assistant_id	str	The ID of the assistant to get OR the name of the graph (to use the default assistant).	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Assistant	Assistant	Assistant Object.
Example Usage

assistant = client.assistants.get(
    assistant_id="my_assistant_id"
)
print(assistant)

----------------------------------------------------

{
    'assistant_id': 'my_assistant_id',
    'graph_id': 'agent',
    'created_at': '2024-06-25T17:10:33.109781+00:00',
    'updated_at': '2024-06-25T17:10:33.109781+00:00',
    'config': {},
    'context': {},
    'metadata': {'created_by': 'system'}
}
 get_graph ¶

get_graph(
    assistant_id: str,
    *,
    xray: int | bool = False,
    headers: dict[str, str] | None = None
) -> dict[str, list[dict[str, Any]]]
Get the graph of an assistant by ID.

Parameters:

Name	Type	Description	Default
assistant_id	str	The ID of the assistant to get the graph of.	required
xray	int | bool	Include graph representation of subgraphs. If an integer value is provided, only subgraphs with a depth less than or equal to the value will be included.	False
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Graph	dict[str, list[dict[str, Any]]]	The graph information for the assistant in JSON format.
Example Usage

client = get_sync_client(url="http://localhost:2024")
graph_info = client.assistants.get_graph(
    assistant_id="my_assistant_id"
)
print(graph_info)

--------------------------------------------------------------------------------------------------------------------------

{
    'nodes':
        [
            {'id': '__start__', 'type': 'schema', 'data': '__start__'},
            {'id': '__end__', 'type': 'schema', 'data': '__end__'},
            {'id': 'agent','type': 'runnable','data': {'id': ['langgraph', 'utils', 'RunnableCallable'],'name': 'agent'}},
        ],
    'edges':
        [
            {'source': '__start__', 'target': 'agent'},
            {'source': 'agent','target': '__end__'}
        ]
}
 get_schemas ¶

get_schemas(
    assistant_id: str,
    *,
    headers: dict[str, str] | None = None
) -> GraphSchema
Get the schemas of an assistant by ID.

Parameters:

Name	Type	Description	Default
assistant_id	str	The ID of the assistant to get the schema of.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
GraphSchema	GraphSchema	The graph schema for the assistant.
Example Usage

client = get_sync_client(url="http://localhost:2024")
schema = client.assistants.get_schemas(
    assistant_id="my_assistant_id"
)
print(schema)

----------------------------------------------------------------------------------------------------------------------------

{
    'graph_id': 'agent',
    'state_schema':
        {
            'title': 'LangGraphInput',
            '$ref': '#/definitions/AgentState',
            'definitions':
                {
                    'BaseMessage':
                        {
                            'title': 'BaseMessage',
                            'description': 'Base abstract Message class. Messages are the inputs and outputs of ChatModels.',
                            'type': 'object',
                            'properties':
                                {
                                 'content':
                                    {
                                        'title': 'Content',
                                        'anyOf': [
                                            {'type': 'string'},
                                            {'type': 'array','items': {'anyOf': [{'type': 'string'}, {'type': 'object'}]}}
                                        ]
                                    },
                                'additional_kwargs':
                                    {
                                        'title': 'Additional Kwargs',
                                        'type': 'object'
                                    },
                                'response_metadata':
                                    {
                                        'title': 'Response Metadata',
                                        'type': 'object'
                                    },
                                'type':
                                    {
                                        'title': 'Type',
                                        'type': 'string'
                                    },
                                'name':
                                    {
                                        'title': 'Name',
                                        'type': 'string'
                                    },
                                'id':
                                    {
                                        'title': 'Id',
                                        'type': 'string'
                                    }
                                },
                            'required': ['content', 'type']
                        },
                    'AgentState':
                        {
                            'title': 'AgentState',
                            'type': 'object',
                            'properties':
                                {
                                    'messages':
                                        {
                                            'title': 'Messages',
                                            'type': 'array',
                                            'items': {'$ref': '#/definitions/BaseMessage'}
                                        }
                                },
                            'required': ['messages']
                        }
                }
        },
    'config_schema':
        {
            'title': 'Configurable',
            'type': 'object',
            'properties':
                {
                    'model_name':
                        {
                            'title': 'Model Name',
                            'enum': ['anthropic', 'openai'],
                            'type': 'string'
                        }
                }
        },
    'context_schema':
        {
            'title': 'Context',
            'type': 'object',
            'properties':
                {
                    'model_name':
                        {
                            'title': 'Model Name',
                            'enum': ['anthropic', 'openai'],
                            'type': 'string'
                        }
                }
        }
}
 get_subgraphs ¶

get_subgraphs(
    assistant_id: str,
    namespace: str | None = None,
    recurse: bool = False,
    *,
    headers: dict[str, str] | None = None
) -> Subgraphs
Get the schemas of an assistant by ID.

Parameters:

Name	Type	Description	Default
assistant_id	str	The ID of the assistant to get the schema of.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Subgraphs	Subgraphs	The graph schema for the assistant.
 create ¶

create(
    graph_id: str | None,
    config: Config | None = None,
    *,
    context: Context | None = None,
    metadata: Json = None,
    assistant_id: str | None = None,
    if_exists: OnConflictBehavior | None = None,
    name: str | None = None,
    headers: dict[str, str] | None = None,
    description: str | None = None
) -> Assistant
Create a new assistant.

Useful when graph is configurable and you want to create different assistants based on different configurations.

Parameters:

Name	Type	Description	Default
graph_id	str | None	The ID of the graph the assistant should use. The graph ID is normally set in your langgraph.json configuration.	required
config	Config | None	Configuration to use for the graph.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
metadata	Json	Metadata to add to assistant.	None
assistant_id	str | None	Assistant ID to use, will default to a random UUID if not provided.	None
if_exists	OnConflictBehavior | None	How to handle duplicate creation. Defaults to 'raise' under the hood. Must be either 'raise' (raise error if duplicate), or 'do_nothing' (return existing assistant).	None
name	str | None	The name of the assistant. Defaults to 'Untitled' under the hood.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
description	str | None	Optional description of the assistant. The description field is available for langgraph-api server version>=0.0.45	None
Returns:

Name	Type	Description
Assistant	Assistant	The created assistant.
Example Usage

client = get_sync_client(url="http://localhost:2024")
assistant = client.assistants.create(
    graph_id="agent",
    context={"model_name": "openai"},
    metadata={"number":1},
    assistant_id="my-assistant-id",
    if_exists="do_nothing",
    name="my_name"
)
 update ¶

update(
    assistant_id: str,
    *,
    graph_id: str | None = None,
    config: Config | None = None,
    context: Context | None = None,
    metadata: Json = None,
    name: str | None = None,
    headers: dict[str, str] | None = None,
    description: str | None = None
) -> Assistant
Update an assistant.

Use this to point to a different graph, update the configuration, or change the metadata of an assistant.

Parameters:

Name	Type	Description	Default
assistant_id	str	Assistant to update.	required
graph_id	str | None	The ID of the graph the assistant should use. The graph ID is normally set in your langgraph.json configuration. If None, assistant will keep pointing to same graph.	None
config	Config | None	Configuration to use for the graph.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
metadata	Json	Metadata to merge with existing assistant metadata.	None
name	str | None	The new name for the assistant.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
description	str | None	Optional description of the assistant. The description field is available for langgraph-api server version>=0.0.45	None
Returns:

Name	Type	Description
Assistant	Assistant	The updated assistant.
Example Usage

client = get_sync_client(url="http://localhost:2024")
assistant = client.assistants.update(
    assistant_id='e280dad7-8618-443f-87f1-8e41841c180f',
    graph_id="other-graph",
    context={"model_name": "anthropic"},
    metadata={"number":2}
)
 delete ¶

delete(
    assistant_id: str,
    *,
    headers: dict[str, str] | None = None
) -> None
Delete an assistant.

Parameters:

Name	Type	Description	Default
assistant_id	str	The assistant ID to delete.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_sync_client(url="http://localhost:2024")
client.assistants.delete(
    assistant_id="my_assistant_id"
)
 search ¶

search(
    *,
    metadata: Json = None,
    graph_id: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: AssistantSortBy | None = None,
    sort_order: SortOrder | None = None,
    headers: dict[str, str] | None = None
) -> list[Assistant]
Search for assistants.

Parameters:

Name	Type	Description	Default
metadata	Json	Metadata to filter by. Exact match filter for each KV pair.	None
graph_id	str | None	The ID of the graph to filter by. The graph ID is normally set in your langgraph.json configuration.	None
limit	int	The maximum number of results to return.	10
offset	int	The number of results to skip.	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[Assistant]	list[Assistant]: A list of assistants.
Example Usage

client = get_sync_client(url="http://localhost:2024")
assistants = client.assistants.search(
    metadata = {"name":"my_name"},
    graph_id="my_graph_id",
    limit=5,
    offset=5
)
 get_versions ¶

get_versions(
    assistant_id: str,
    metadata: Json = None,
    limit: int = 10,
    offset: int = 0,
    *,
    headers: dict[str, str] | None = None
) -> list[AssistantVersion]
List all versions of an assistant.

Parameters:

Name	Type	Description	Default
assistant_id	str	The assistant ID to get versions for.	required
metadata	Json	Metadata to filter versions by. Exact match filter for each KV pair.	None
limit	int	The maximum number of versions to return.	10
offset	int	The number of versions to skip.	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[AssistantVersion]	list[Assistant]: A list of assistants.
Example Usage

client = get_sync_client(url="http://localhost:2024")
assistant_versions = client.assistants.get_versions(
    assistant_id="my_assistant_id"
)
 set_latest ¶

set_latest(
    assistant_id: str,
    version: int,
    *,
    headers: dict[str, str] | None = None
) -> Assistant
Change the version of an assistant.

Parameters:

Name	Type	Description	Default
assistant_id	str	The assistant ID to delete.	required
version	int	The version to change to.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Assistant	Assistant	Assistant Object.
Example Usage

client = get_sync_client(url="http://localhost:2024")
new_version_assistant = client.assistants.set_latest(
    assistant_id="my_assistant_id",
    version=3
)
 SyncThreadsClient ¶
Synchronous client for managing threads in LangGraph.

This class provides methods to create, retrieve, and manage threads, which represent conversations or stateful interactions.

Example

client = get_sync_client(url="http://localhost:2024")
thread = client.threads.create(metadata={"user_id": "123"})
Methods:

Name	Description
get	Get a thread by ID.
create	Create a new thread.
update	Update a thread.
delete	Delete a thread.
search	Search for threads.
copy	Copy a thread.
get_state	Get the state of a thread.
update_state	Update the state of a thread.
get_history	Get the state history of a thread.
 get ¶

get(
    thread_id: str, *, headers: dict[str, str] | None = None
) -> Thread
Get a thread by ID.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to get.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Thread	Thread	Thread object.
Example Usage

client = get_sync_client(url="http://localhost:2024")
thread = client.threads.get(
    thread_id="my_thread_id"
)
print(thread)

-----------------------------------------------------

{
    'thread_id': 'my_thread_id',
    'created_at': '2024-07-18T18:35:15.540834+00:00',
    'updated_at': '2024-07-18T18:35:15.540834+00:00',
    'metadata': {'graph_id': 'agent'}
}
 create ¶

create(
    *,
    metadata: Json = None,
    thread_id: str | None = None,
    if_exists: OnConflictBehavior | None = None,
    supersteps: (
        Sequence[dict[str, Sequence[dict[str, Any]]]] | None
    ) = None,
    graph_id: str | None = None,
    headers: dict[str, str] | None = None
) -> Thread
Create a new thread.

Parameters:

Name	Type	Description	Default
metadata	Json	Metadata to add to thread.	None
thread_id	str | None	ID of thread. If None, ID will be a randomly generated UUID.	None
if_exists	OnConflictBehavior | None	How to handle duplicate creation. Defaults to 'raise' under the hood. Must be either 'raise' (raise error if duplicate), or 'do_nothing' (return existing thread).	None
supersteps	Sequence[dict[str, Sequence[dict[str, Any]]]] | None	Apply a list of supersteps when creating a thread, each containing a sequence of updates. Each update has values or command and as_node. Used for copying a thread between deployments.	None
graph_id	str | None	Optional graph ID to associate with the thread.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Thread	Thread	The created thread.
Example Usage

client = get_sync_client(url="http://localhost:2024")
thread = client.threads.create(
    metadata={"number":1},
    thread_id="my-thread-id",
    if_exists="raise"
)
)
 update ¶

update(
    thread_id: str,
    *,
    metadata: dict[str, Any],
    headers: dict[str, str] | None = None
) -> Thread
Update a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	ID of thread to update.	required
metadata	dict[str, Any]	Metadata to merge with existing thread metadata.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Thread	Thread	The created thread.
Example Usage

client = get_sync_client(url="http://localhost:2024")
thread = client.threads.update(
    thread_id="my-thread-id",
    metadata={"number":1},
)
 delete ¶

delete(
    thread_id: str, *, headers: dict[str, str] | None = None
) -> None
Delete a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to delete.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client.threads.delete(
    thread_id="my_thread_id"
)
 search ¶

search(
    *,
    metadata: Json = None,
    values: Json = None,
    status: ThreadStatus | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: ThreadSortBy | None = None,
    sort_order: SortOrder | None = None,
    headers: dict[str, str] | None = None
) -> list[Thread]
Search for threads.

Parameters:

Name	Type	Description	Default
metadata	Json	Thread metadata to filter on.	None
values	Json	State values to filter on.	None
status	ThreadStatus | None	Thread status to filter on. Must be one of 'idle', 'busy', 'interrupted' or 'error'.	None
limit	int	Limit on number of threads to return.	10
offset	int	Offset in threads table to start search from.	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[Thread]	list[Thread]: List of the threads matching the search parameters.
Example Usage

client = get_sync_client(url="http://localhost:2024")
threads = client.threads.search(
    metadata={"number":1},
    status="interrupted",
    limit=15,
    offset=5
)
 copy ¶

copy(
    thread_id: str, *, headers: dict[str, str] | None = None
) -> None
Copy a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to copy.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_sync_client(url="http://localhost:2024")
client.threads.copy(
    thread_id="my_thread_id"
)
 get_state ¶

get_state(
    thread_id: str,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    *,
    subgraphs: bool = False,
    headers: dict[str, str] | None = None
) -> ThreadState
Get the state of a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to get the state of.	required
checkpoint	Checkpoint | None	The checkpoint to get the state of.	None
subgraphs	bool	Include subgraphs states.	False
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
ThreadState	ThreadState	the thread of the state.
Example Usage

client = get_sync_client(url="http://localhost:2024")
thread_state = client.threads.get_state(
    thread_id="my_thread_id",
    checkpoint_id="my_checkpoint_id"
)
print(thread_state)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

{
    'values': {
        'messages': [
            {
                'content': 'how are you?',
                'additional_kwargs': {},
                'response_metadata': {},
                'type': 'human',
                'name': None,
                'id': 'fe0a5778-cfe9-42ee-b807-0adaa1873c10',
                'example': False
            },
            {
                'content': "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, honest, and harmless.",
                'additional_kwargs': {},
                'response_metadata': {},
                'type': 'ai',
                'name': None,
                'id': 'run-159b782c-b679-4830-83c6-cef87798fe8b',
                'example': False,
                'tool_calls': [],
                'invalid_tool_calls': [],
                'usage_metadata': None
            }
        ]
    },
    'next': [],
    'checkpoint':
        {
            'thread_id': 'e2496803-ecd5-4e0c-a779-3226296181c2',
            'checkpoint_ns': '',
            'checkpoint_id': '1ef4a9b8-e6fb-67b1-8001-abd5184439d1'
        }
    'metadata':
        {
            'step': 1,
            'run_id': '1ef4a9b8-d7da-679a-a45a-872054341df2',
            'source': 'loop',
            'writes':
                {
                    'agent':
                        {
                            'messages': [
                                {
                                    'id': 'run-159b782c-b679-4830-83c6-cef87798fe8b',
                                    'name': None,
                                    'type': 'ai',
                                    'content': "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, honest, and harmless.",
                                    'example': False,
                                    'tool_calls': [],
                                    'usage_metadata': None,
                                    'additional_kwargs': {},
                                    'response_metadata': {},
                                    'invalid_tool_calls': []
                                }
                            ]
                        }
                },
    'user_id': None,
    'graph_id': 'agent',
    'thread_id': 'e2496803-ecd5-4e0c-a779-3226296181c2',
    'created_by': 'system',
    'assistant_id': 'fe096781-5601-53d2-b2f6-0d3403f7e9ca'},
    'created_at': '2024-07-25T15:35:44.184703+00:00',
    'parent_config':
        {
            'thread_id': 'e2496803-ecd5-4e0c-a779-3226296181c2',
            'checkpoint_ns': '',
            'checkpoint_id': '1ef4a9b8-d80d-6fa7-8000-9300467fad0f'
        }
}
 update_state ¶

update_state(
    thread_id: str,
    values: dict | Sequence[dict] | None,
    *,
    as_node: str | None = None,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    headers: dict[str, str] | None = None
) -> ThreadUpdateStateResponse
Update the state of a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to update.	required
values	dict | Sequence[dict] | None	The values to update the state with.	required
as_node	str | None	Update the state as if this node had just executed.	None
checkpoint	Checkpoint | None	The checkpoint to update the state of.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
ThreadUpdateStateResponse	ThreadUpdateStateResponse	Response after updating a thread's state.
Example Usage

response = await client.threads.update_state(
    thread_id="my_thread_id",
    values={"messages":[{"role": "user", "content": "hello!"}]},
    as_node="my_node",
)
print(response)

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

{
    'checkpoint': {
        'thread_id': 'e2496803-ecd5-4e0c-a779-3226296181c2',
        'checkpoint_ns': '',
        'checkpoint_id': '1ef4a9b8-e6fb-67b1-8001-abd5184439d1',
        'checkpoint_map': {}
    }
}
 get_history ¶

get_history(
    thread_id: str,
    *,
    limit: int = 10,
    before: str | Checkpoint | None = None,
    metadata: dict | None = None,
    checkpoint: Checkpoint | None = None,
    headers: dict[str, str] | None = None
) -> list[ThreadState]
Get the state history of a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The ID of the thread to get the state history for.	required
checkpoint	Checkpoint | None	Return states for this subgraph. If empty defaults to root.	None
limit	int	The maximum number of states to return.	10
before	str | Checkpoint | None	Return states before this checkpoint.	None
metadata	dict | None	Filter states by metadata key-value pairs.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[ThreadState]	list[ThreadState]: the state history of the thread.
Example Usage

thread_state = client.threads.get_history(
    thread_id="my_thread_id",
    limit=5,
    before="my_timestamp",
    metadata={"name":"my_name"}
)
 SyncRunsClient ¶
Synchronous client for managing runs in LangGraph.

This class provides methods to create, retrieve, and manage runs, which represent individual executions of graphs.

Example

client = get_sync_client(url="http://localhost:2024")
run = client.runs.create(thread_id="thread_123", assistant_id="asst_456")
Methods:

Name	Description
stream	Create a run and stream the results.
create	Create a background run.
create_batch	Create a batch of stateless background runs.
wait	Create a run, wait until it finishes and return the final state.
list	List runs.
get	Get a run.
cancel	Get a run.
join	Block until a run is done. Returns the final state of the thread.
join_stream	Stream output from a run in real-time, until the run is done.
delete	Delete a run.
 stream ¶

stream(
    thread_id: str | None,
    assistant_id: str,
    *,
    input: dict | None = None,
    command: Command | None = None,
    stream_mode: (
        StreamMode | Sequence[StreamMode]
    ) = "values",
    stream_subgraphs: bool = False,
    stream_resumable: bool = False,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    checkpoint_during: bool | None = None,
    interrupt_before: All | Sequence[str] | None = None,
    interrupt_after: All | Sequence[str] | None = None,
    feedback_keys: Sequence[str] | None = None,
    on_disconnect: DisconnectMode | None = None,
    on_completion: OnCompletionBehavior | None = None,
    webhook: str | None = None,
    multitask_strategy: MultitaskStrategy | None = None,
    if_not_exists: IfNotExists | None = None,
    after_seconds: int | None = None,
    headers: dict[str, str] | None = None,
    on_run_created: (
        Callable[[RunCreateMetadata], None] | None
    ) = None
) -> Iterator[StreamPart]
Create a run and stream the results.

Parameters:

Name	Type	Description	Default
thread_id	str | None	the thread ID to assign to the thread. If None will create a stateless run.	required
assistant_id	str	The assistant ID or graph name to stream from. If using graph name, will default to first assistant created from that graph.	required
input	dict | None	The input to the graph.	None
command	Command | None	The command to execute.	None
stream_mode	StreamMode | Sequence[StreamMode]	The stream mode(s) to use.	'values'
stream_subgraphs	bool	Whether to stream output from subgraphs.	False
stream_resumable	bool	Whether the stream is considered resumable. If true, the stream can be resumed and replayed in its entirety even after disconnection.	False
metadata	dict | None	Metadata to assign to the run.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint	Checkpoint | None	The checkpoint to resume from.	None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | Sequence[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | Sequence[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
feedback_keys	Sequence[str] | None	Feedback keys to assign to run.	None
on_disconnect	DisconnectMode | None	The disconnect mode to use. Must be one of 'cancel' or 'continue'.	None
on_completion	OnCompletionBehavior | None	Whether to delete or keep the thread created for a stateless run. Must be one of 'delete' or 'keep'.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
multitask_strategy	MultitaskStrategy | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
if_not_exists	IfNotExists | None	How to handle missing thread. Defaults to 'reject'. Must be either 'reject' (raise error if missing), or 'create' (create new thread).	None
after_seconds	int | None	The number of seconds to wait before starting the run. Use to schedule future runs.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
on_run_created	Callable[[RunCreateMetadata], None] | None	Optional callback to call when a run is created.	None
Returns:

Type	Description
Iterator[StreamPart]	Iterator[StreamPart]: Iterator of stream results.
Example Usage

client = get_sync_client(url="http://localhost:2024")
async for chunk in client.runs.stream(
    thread_id=None,
    assistant_id="agent",
    input={"messages": [{"role": "user", "content": "how are you?"}]},
    stream_mode=["values","debug"],
    metadata={"name":"my_run"},
    context={"model_name": "anthropic"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    feedback_keys=["my_feedback_key_1","my_feedback_key_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
):
    print(chunk)

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

StreamPart(event='metadata', data={'run_id': '1ef4a9b8-d7da-679a-a45a-872054341df2'})
StreamPart(event='values', data={'messages': [{'content': 'how are you?', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': 'fe0a5778-cfe9-42ee-b807-0adaa1873c10', 'example': False}]})
StreamPart(event='values', data={'messages': [{'content': 'how are you?', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': 'fe0a5778-cfe9-42ee-b807-0adaa1873c10', 'example': False}, {'content': "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, honest, and harmless.", 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'ai', 'name': None, 'id': 'run-159b782c-b679-4830-83c6-cef87798fe8b', 'example': False, 'tool_calls': [], 'invalid_tool_calls': [], 'usage_metadata': None}]})
StreamPart(event='end', data=None)
 create ¶

create(
    thread_id: str | None,
    assistant_id: str,
    *,
    input: dict | None = None,
    command: Command | None = None,
    stream_mode: (
        StreamMode | Sequence[StreamMode]
    ) = "values",
    stream_subgraphs: bool = False,
    stream_resumable: bool = False,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    checkpoint_during: bool | None = None,
    interrupt_before: All | Sequence[str] | None = None,
    interrupt_after: All | Sequence[str] | None = None,
    webhook: str | None = None,
    multitask_strategy: MultitaskStrategy | None = None,
    on_completion: OnCompletionBehavior | None = None,
    if_not_exists: IfNotExists | None = None,
    after_seconds: int | None = None,
    headers: dict[str, str] | None = None,
    on_run_created: (
        Callable[[RunCreateMetadata], None] | None
    ) = None
) -> Run
Create a background run.

Parameters:

Name	Type	Description	Default
thread_id	str | None	the thread ID to assign to the thread. If None will create a stateless run.	required
assistant_id	str	The assistant ID or graph name to stream from. If using graph name, will default to first assistant created from that graph.	required
input	dict | None	The input to the graph.	None
command	Command | None	The command to execute.	None
stream_mode	StreamMode | Sequence[StreamMode]	The stream mode(s) to use.	'values'
stream_subgraphs	bool	Whether to stream output from subgraphs.	False
stream_resumable	bool	Whether the stream is considered resumable. If true, the stream can be resumed and replayed in its entirety even after disconnection.	False
metadata	dict | None	Metadata to assign to the run.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint	Checkpoint | None	The checkpoint to resume from.	None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | Sequence[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | Sequence[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
multitask_strategy	MultitaskStrategy | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
on_completion	OnCompletionBehavior | None	Whether to delete or keep the thread created for a stateless run. Must be one of 'delete' or 'keep'.	None
if_not_exists	IfNotExists | None	How to handle missing thread. Defaults to 'reject'. Must be either 'reject' (raise error if missing), or 'create' (create new thread).	None
after_seconds	int | None	The number of seconds to wait before starting the run. Use to schedule future runs.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
on_run_created	Callable[[RunCreateMetadata], None] | None	Optional callback to call when a run is created.	None
Returns:

Name	Type	Description
Run	Run	The created background run.
Example Usage

client = get_sync_client(url="http://localhost:2024")
background_run = client.runs.create(
    thread_id="my_thread_id",
    assistant_id="my_assistant_id",
    input={"messages": [{"role": "user", "content": "hello!"}]},
    metadata={"name":"my_run"},
    context={"model_name": "openai"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
)
print(background_run)

--------------------------------------------------------------------------------

{
    'run_id': 'my_run_id',
    'thread_id': 'my_thread_id',
    'assistant_id': 'my_assistant_id',
    'created_at': '2024-07-25T15:35:42.598503+00:00',
    'updated_at': '2024-07-25T15:35:42.598503+00:00',
    'metadata': {},
    'status': 'pending',
    'kwargs':
        {
            'input':
                {
                    'messages': [
                        {
                            'role': 'user',
                            'content': 'how are you?'
                        }
                    ]
                },
            'config':
                {
                    'metadata':
                        {
                            'created_by': 'system'
                        },
                    'configurable':
                        {
                            'run_id': 'my_run_id',
                            'user_id': None,
                            'graph_id': 'agent',
                            'thread_id': 'my_thread_id',
                            'checkpoint_id': None,
                            'assistant_id': 'my_assistant_id'
                        }
                },
            'context':
                {
                    'model_name': 'openai'
                },
            'webhook': "https://my.fake.webhook.com",
            'temporary': False,
            'stream_mode': ['values'],
            'feedback_keys': None,
            'interrupt_after': ["node_to_stop_after_1","node_to_stop_after_2"],
            'interrupt_before': ["node_to_stop_before_1","node_to_stop_before_2"]
        },
    'multitask_strategy': 'interrupt'
}
 create_batch ¶

create_batch(
    payloads: list[RunCreate],
    *,
    headers: dict[str, str] | None = None
) -> list[Run]
Create a batch of stateless background runs.

 wait ¶

wait(
    thread_id: str | None,
    assistant_id: str,
    *,
    input: dict | None = None,
    command: Command | None = None,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint_during: bool | None = None,
    checkpoint: Checkpoint | None = None,
    checkpoint_id: str | None = None,
    interrupt_before: All | Sequence[str] | None = None,
    interrupt_after: All | Sequence[str] | None = None,
    webhook: str | None = None,
    on_disconnect: DisconnectMode | None = None,
    on_completion: OnCompletionBehavior | None = None,
    multitask_strategy: MultitaskStrategy | None = None,
    if_not_exists: IfNotExists | None = None,
    after_seconds: int | None = None,
    headers: dict[str, str] | None = None,
    on_run_created: (
        Callable[[RunCreateMetadata], None] | None
    ) = None
) -> list[dict] | dict[str, Any]
Create a run, wait until it finishes and return the final state.

Parameters:

Name	Type	Description	Default
thread_id	str | None	the thread ID to create the run on. If None will create a stateless run.	required
assistant_id	str	The assistant ID or graph name to run. If using graph name, will default to first assistant created from that graph.	required
input	dict | None	The input to the graph.	None
command	Command | None	The command to execute.	None
metadata	dict | None	Metadata to assign to the run.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint	Checkpoint | None	The checkpoint to resume from.	None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | Sequence[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | Sequence[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
on_disconnect	DisconnectMode | None	The disconnect mode to use. Must be one of 'cancel' or 'continue'.	None
on_completion	OnCompletionBehavior | None	Whether to delete or keep the thread created for a stateless run. Must be one of 'delete' or 'keep'.	None
multitask_strategy	MultitaskStrategy | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
if_not_exists	IfNotExists | None	How to handle missing thread. Defaults to 'reject'. Must be either 'reject' (raise error if missing), or 'create' (create new thread).	None
after_seconds	int | None	The number of seconds to wait before starting the run. Use to schedule future runs.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
on_run_created	Callable[[RunCreateMetadata], None] | None	Optional callback to call when a run is created.	None
Returns:

Type	Description
list[dict] | dict[str, Any]	Union[list[dict], dict[str, Any]]: The output of the run.
Example Usage

final_state_of_run = client.runs.wait(
    thread_id=None,
    assistant_id="agent",
    input={"messages": [{"role": "user", "content": "how are you?"}]},
    metadata={"name":"my_run"},
    context={"model_name": "anthropic"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
)
print(final_state_of_run)

-------------------------------------------------------------------------------------------------------------------------------------------

{
    'messages': [
        {
            'content': 'how are you?',
            'additional_kwargs': {},
            'response_metadata': {},
            'type': 'human',
            'name': None,
            'id': 'f51a862c-62fe-4866-863b-b0863e8ad78a',
            'example': False
        },
        {
            'content': "I'm doing well, thanks for asking! I'm an AI assistant created by Anthropic to be helpful, honest, and harmless.",
            'additional_kwargs': {},
            'response_metadata': {},
            'type': 'ai',
            'name': None,
            'id': 'run-bf1cd3c6-768f-4c16-b62d-ba6f17ad8b36',
            'example': False,
            'tool_calls': [],
            'invalid_tool_calls': [],
            'usage_metadata': None
        }
    ]
}
 list ¶

list(
    thread_id: str,
    *,
    limit: int = 10,
    offset: int = 0,
    headers: dict[str, str] | None = None
) -> list[Run]
List runs.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to list runs for.	required
limit	int	The maximum number of results to return.	10
offset	int	The number of results to skip.	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[Run]	list[Run]: The runs for the thread.
Example Usage

client = get_sync_client(url="http://localhost:2024")
client.runs.list(
    thread_id="thread_id",
    limit=5,
    offset=5,
)
 get ¶

get(
    thread_id: str,
    run_id: str,
    *,
    headers: dict[str, str] | None = None
) -> Run
Get a run.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to get.	required
run_id	str	The run ID to get.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Run	Run	Run object.
Example Usage

run = client.runs.get(
    thread_id="thread_id_to_delete",
    run_id="run_id_to_delete",
)
 cancel ¶

cancel(
    thread_id: str,
    run_id: str,
    *,
    wait: bool = False,
    action: CancelAction = "interrupt",
    headers: dict[str, str] | None = None
) -> None
Get a run.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to cancel.	required
run_id	str	The run ID to cancel.	required
wait	bool	Whether to wait until run has completed.	False
action	CancelAction	Action to take when cancelling the run. Possible values are interrupt or rollback. Default is interrupt.	'interrupt'
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_sync_client(url="http://localhost:2024")
client.runs.cancel(
    thread_id="thread_id_to_cancel",
    run_id="run_id_to_cancel",
    wait=True,
    action="interrupt"
)
 join ¶

join(
    thread_id: str,
    run_id: str,
    *,
    headers: dict[str, str] | None = None
) -> dict
Block until a run is done. Returns the final state of the thread.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to join.	required
run_id	str	The run ID to join.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
dict	None
Example Usage

client = get_sync_client(url="http://localhost:2024")
client.runs.join(
    thread_id="thread_id_to_join",
    run_id="run_id_to_join"
)
 join_stream ¶

join_stream(
    thread_id: str,
    run_id: str,
    *,
    stream_mode: (
        StreamMode | Sequence[StreamMode] | None
    ) = None,
    cancel_on_disconnect: bool = False,
    headers: dict[str, str] | None = None,
    last_event_id: str | None = None
) -> Iterator[StreamPart]
Stream output from a run in real-time, until the run is done. Output is not buffered, so any output produced before this call will not be received here.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to join.	required
run_id	str	The run ID to join.	required
stream_mode	StreamMode | Sequence[StreamMode] | None	The stream mode(s) to use. Must be a subset of the stream modes passed when creating the run. Background runs default to having the union of all stream modes.	None
cancel_on_disconnect	bool	Whether to cancel the run when the stream is disconnected.	False
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
Iterator[StreamPart]	None
Example Usage

client = get_sync_client(url="http://localhost:2024")
client.runs.join_stream(
    thread_id="thread_id_to_join",
    run_id="run_id_to_join",
    stream_mode=["values", "debug"]
)
 delete ¶

delete(
    thread_id: str,
    run_id: str,
    *,
    headers: dict[str, str] | None = None
) -> None
Delete a run.

Parameters:

Name	Type	Description	Default
thread_id	str	The thread ID to delete.	required
run_id	str	The run ID to delete.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_sync_client(url="http://localhost:2024")
client.runs.delete(
    thread_id="thread_id_to_delete",
    run_id="run_id_to_delete"
)
 SyncCronClient ¶
Synchronous client for managing cron jobs in LangGraph.

This class provides methods to create and manage scheduled tasks (cron jobs) for automated graph executions.

Example

client = get_sync_client(url="http://localhost:8123")
cron_job = client.crons.create_for_thread(thread_id="thread_123", assistant_id="asst_456", schedule="0 * * * *")
Feature Availability

The crons client functionality is not supported on all licenses. Please check the relevant license documentation for the most up-to-date details on feature availability.

Methods:

Name	Description
create_for_thread	Create a cron job for a thread.
create	Create a cron run.
delete	Delete a cron.
search	Get a list of cron jobs.
 create_for_thread ¶

create_for_thread(
    thread_id: str,
    assistant_id: str,
    *,
    schedule: str,
    input: dict | None = None,
    metadata: dict | None = None,
    checkpoint_during: bool | None = None,
    config: Config | None = None,
    context: Context | None = None,
    interrupt_before: All | list[str] | None = None,
    interrupt_after: All | list[str] | None = None,
    webhook: str | None = None,
    multitask_strategy: str | None = None,
    headers: dict[str, str] | None = None
) -> Run
Create a cron job for a thread.

Parameters:

Name	Type	Description	Default
thread_id	str	the thread ID to run the cron job on.	required
assistant_id	str	The assistant ID or graph name to use for the cron job. If using graph name, will default to first assistant created from that graph.	required
schedule	str	The cron schedule to execute this job on.	required
input	dict | None	The input to the graph.	None
metadata	dict | None	Metadata to assign to the cron job runs.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | list[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | list[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
multitask_strategy	str | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Run	Run	The cron run.
Example Usage

client = get_sync_client(url="http://localhost:8123")
cron_run = client.crons.create_for_thread(
    thread_id="my-thread-id",
    assistant_id="agent",
    schedule="27 15 * * *",
    input={"messages": [{"role": "user", "content": "hello!"}]},
    metadata={"name":"my_run"},
    context={"model_name": "openai"},
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
)
 create ¶

create(
    assistant_id: str,
    *,
    schedule: str,
    input: dict | None = None,
    metadata: dict | None = None,
    config: Config | None = None,
    context: Context | None = None,
    checkpoint_during: bool | None = None,
    interrupt_before: All | list[str] | None = None,
    interrupt_after: All | list[str] | None = None,
    webhook: str | None = None,
    multitask_strategy: str | None = None,
    headers: dict[str, str] | None = None
) -> Run
Create a cron run.

Parameters:

Name	Type	Description	Default
assistant_id	str	The assistant ID or graph name to use for the cron job. If using graph name, will default to first assistant created from that graph.	required
schedule	str	The cron schedule to execute this job on.	required
input	dict | None	The input to the graph.	None
metadata	dict | None	Metadata to assign to the cron job runs.	None
config	Config | None	The configuration for the assistant.	None
context	Context | None	Static context to add to the assistant.
Supported with langgraph>=0.6.0

None
checkpoint_during	bool | None	Whether to checkpoint during the run (or only at the end/interruption).	None
interrupt_before	All | list[str] | None	Nodes to interrupt immediately before they get executed.	None
interrupt_after	All | list[str] | None	Nodes to Nodes to interrupt immediately after they get executed.	None
webhook	str | None	Webhook to call after LangGraph API call is done.	None
multitask_strategy	str | None	Multitask strategy to use. Must be one of 'reject', 'interrupt', 'rollback', or 'enqueue'.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Run	Run	The cron run.
Example Usage

client = get_sync_client(url="http://localhost:8123")
cron_run = client.crons.create(
    assistant_id="agent",
    schedule="27 15 * * *",
    input={"messages": [{"role": "user", "content": "hello!"}]},
    metadata={"name":"my_run"},
    context={"model_name": "openai"},
    checkpoint_during=True,
    interrupt_before=["node_to_stop_before_1","node_to_stop_before_2"],
    interrupt_after=["node_to_stop_after_1","node_to_stop_after_2"],
    webhook="https://my.fake.webhook.com",
    multitask_strategy="interrupt"
)
 delete ¶

delete(
    cron_id: str, *, headers: dict[str, str] | None = None
) -> None
Delete a cron.

Parameters:

Name	Type	Description	Default
cron_id	str	The cron ID to delete.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_sync_client(url="http://localhost:8123")
client.crons.delete(
    cron_id="cron_to_delete"
)
 search ¶

search(
    *,
    assistant_id: str | None = None,
    thread_id: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: CronSortBy | None = None,
    sort_order: SortOrder | None = None,
    headers: dict[str, str] | None = None
) -> list[Cron]
Get a list of cron jobs.

Parameters:

Name	Type	Description	Default
assistant_id	str | None	The assistant ID or graph name to search for.	None
thread_id	str | None	the thread ID to search for.	None
limit	int	The maximum number of results to return.	10
offset	int	The number of results to skip.	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
list[Cron]	list[Cron]: The list of cron jobs returned by the search,
Example Usage

client = get_sync_client(url="http://localhost:8123")
cron_jobs = client.crons.search(
    assistant_id="my_assistant_id",
    thread_id="my_thread_id",
    limit=5,
    offset=5,
)
print(cron_jobs)

----------------------------------------------------------

[
    {
        'cron_id': '1ef3cefa-4c09-6926-96d0-3dc97fd5e39b',
        'assistant_id': 'my_assistant_id',
        'thread_id': 'my_thread_id',
        'user_id': None,
        'payload':
            {
                'input': {'start_time': ''},
                'schedule': '4 * * * *',
                'assistant_id': 'my_assistant_id'
            },
        'schedule': '4 * * * *',
        'next_run_date': '2024-07-25T17:04:00+00:00',
        'end_time': None,
        'created_at': '2024-07-08T06:02:23.073257+00:00',
        'updated_at': '2024-07-08T06:02:23.073257+00:00'
    }
]
 SyncStoreClient ¶
A client for synchronous operations on a key-value store.

Provides methods to interact with a remote key-value store, allowing storage and retrieval of items within namespaced hierarchies.

Example

client = get_sync_client(url="http://localhost:2024"))
client.store.put_item(["users", "profiles"], "user123", {"name": "Alice", "age": 30})
Methods:

Name	Description
put_item	Store or update an item.
get_item	Retrieve a single item.
delete_item	Delete an item.
search_items	Search for items within a namespace prefix.
list_namespaces	List namespaces with optional match conditions.
 put_item ¶

put_item(
    namespace: Sequence[str],
    /,
    key: str,
    value: dict[str, Any],
    index: Literal[False] | list[str] | None = None,
    ttl: int | None = None,
    headers: dict[str, str] | None = None,
) -> None
Store or update an item.

Parameters:

Name	Type	Description	Default
namespace	Sequence[str]	A list of strings representing the namespace path.	required
key	str	The unique identifier for the item within the namespace.	required
value	dict[str, Any]	A dictionary containing the item's data.	required
index	Literal[False] | list[str] | None	Controls search indexing - None (use defaults), False (disable), or list of field paths to index.	None
ttl	int | None	Optional time-to-live in minutes for the item, or None for no expiration.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_sync_client(url="http://localhost:8123")
client.store.put_item(
    ["documents", "user123"],
    key="item456",
    value={"title": "My Document", "content": "Hello World"}
)
 get_item ¶

get_item(
    namespace: Sequence[str],
    /,
    key: str,
    *,
    refresh_ttl: bool | None = None,
    headers: dict[str, str] | None = None,
) -> Item
Retrieve a single item.

Parameters:

Name	Type	Description	Default
key	str	The unique identifier for the item.	required
namespace	Sequence[str]	Optional list of strings representing the namespace path.	required
refresh_ttl	bool | None	Whether to refresh the TTL on this read operation. If None, uses the store's default behavior.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Name	Type	Description
Item	Item	The retrieved item.
Example Usage

client = get_sync_client(url="http://localhost:8123")
item = client.store.get_item(
    ["documents", "user123"],
    key="item456",
)
print(item)

----------------------------------------------------------------

{
    'namespace': ['documents', 'user123'],
    'key': 'item456',
    'value': {'title': 'My Document', 'content': 'Hello World'},
    'created_at': '2024-07-30T12:00:00Z',
    'updated_at': '2024-07-30T12:00:00Z'
}
 delete_item ¶

delete_item(
    namespace: Sequence[str],
    /,
    key: str,
    headers: dict[str, str] | None = None,
) -> None
Delete an item.

Parameters:

Name	Type	Description	Default
key	str	The unique identifier for the item.	required
namespace	Sequence[str]	Optional list of strings representing the namespace path.	required
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
None	None
Example Usage

client = get_sync_client(url="http://localhost:8123")
client.store.delete_item(
    ["documents", "user123"],
    key="item456",
)
 search_items ¶

search_items(
    namespace_prefix: Sequence[str],
    /,
    filter: dict[str, Any] | None = None,
    limit: int = 10,
    offset: int = 0,
    query: str | None = None,
    refresh_ttl: bool | None = None,
    headers: dict[str, str] | None = None,
) -> SearchItemsResponse
Search for items within a namespace prefix.

Parameters:

Name	Type	Description	Default
namespace_prefix	Sequence[str]	List of strings representing the namespace prefix.	required
filter	dict[str, Any] | None	Optional dictionary of key-value pairs to filter results.	None
limit	int	Maximum number of items to return (default is 10).	10
offset	int	Number of items to skip before returning results (default is 0).	0
query	str | None	Optional query for natural language search.	None
refresh_ttl	bool | None	Whether to refresh the TTL on items returned by this search. If None, uses the store's default behavior.	None
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
SearchItemsResponse	list[Item]: A list of items matching the search criteria.
Example Usage

client = get_sync_client(url="http://localhost:8123")
items = client.store.search_items(
    ["documents"],
    filter={"author": "John Doe"},
    limit=5,
    offset=0
)
print(items)

----------------------------------------------------------------

{
    "items": [
        {
            "namespace": ["documents", "user123"],
            "key": "item789",
            "value": {
                "title": "Another Document",
                "author": "John Doe"
            },
            "created_at": "2024-07-30T12:00:00Z",
            "updated_at": "2024-07-30T12:00:00Z"
        },
        # ... additional items ...
    ]
}
 list_namespaces ¶

list_namespaces(
    prefix: list[str] | None = None,
    suffix: list[str] | None = None,
    max_depth: int | None = None,
    limit: int = 100,
    offset: int = 0,
    headers: dict[str, str] | None = None,
) -> ListNamespaceResponse
List namespaces with optional match conditions.

Parameters:

Name	Type	Description	Default
prefix	list[str] | None	Optional list of strings representing the prefix to filter namespaces.	None
suffix	list[str] | None	Optional list of strings representing the suffix to filter namespaces.	None
max_depth	int | None	Optional integer specifying the maximum depth of namespaces to return.	None
limit	int	Maximum number of namespaces to return (default is 100).	100
offset	int	Number of namespaces to skip before returning results (default is 0).	0
headers	dict[str, str] | None	Optional custom headers to include with the request.	None
Returns:

Type	Description
ListNamespaceResponse	list[list[str]]: A list of namespaces matching the criteria.
Example Usage

client = get_sync_client(url="http://localhost:8123")
namespaces = client.store.list_namespaces(
    prefix=["documents"],
    max_depth=3,
    limit=10,
    offset=0
)
print(namespaces)

----------------------------------------------------------------

[
    ["documents", "user123", "reports"],
    ["documents", "user456", "invoices"],
    ...
]
 get_client ¶

get_client(
    *,
    url: str | None = None,
    api_key: str | None = None,
    headers: dict[str, str] | None = None,
    timeout: TimeoutTypes | None = None
) -> LangGraphClient
Get a LangGraphClient instance.

Parameters:

Name	Type	Description	Default
url	str | None	The URL of the LangGraph API.	None
api_key	str | None	The API key. If not provided, it will be read from the environment. Precedence: 1. explicit argument 2. LANGGRAPH_API_KEY 3. LANGSMITH_API_KEY 4. LANGCHAIN_API_KEY	None
headers	dict[str, str] | None	Optional custom headers	None
timeout	TimeoutTypes | None	Optional timeout configuration for the HTTP client. Accepts an httpx.Timeout instance, a float (seconds), or a tuple of timeouts. Tuple format is (connect, read, write, pool) If not provided, defaults to connect=5s, read=300s, write=300s, and pool=5s.	None
Returns:

Name	Type	Description
LangGraphClient	LangGraphClient	The top-level client for accessing AssistantsClient,
LangGraphClient	ThreadsClient, RunsClient, and CronClient.
Example

from langgraph_sdk import get_client

# get top-level LangGraphClient
client = get_client(url="http://localhost:8123")

# example usage: client.<model>.<method_name>()
assistants = await client.assistants.get(assistant_id="some_uuid")
 get_sync_client ¶

get_sync_client(
    *,
    url: str | None = None,
    api_key: str | None = None,
    headers: dict[str, str] | None = None,
    timeout: TimeoutTypes | None = None
) -> SyncLangGraphClient
Get a synchronous LangGraphClient instance.

Parameters:

Name	Type	Description	Default
url	str | None	The URL of the LangGraph API.	None
api_key	str | None	The API key. If not provided, it will be read from the environment. Precedence: 1. explicit argument 2. LANGGRAPH_API_KEY 3. LANGSMITH_API_KEY 4. LANGCHAIN_API_KEY	None
headers	dict[str, str] | None	Optional custom headers	None
timeout	TimeoutTypes | None	Optional timeout configuration for the HTTP client. Accepts an httpx.Timeout instance, a float (seconds), or a tuple of timeouts. Tuple format is (connect, read, write, pool) If not provided, defaults to connect=5s, read=300s, write=300s, and pool=5s.	None
Returns: SyncLangGraphClient: The top-level synchronous client for accessing AssistantsClient, ThreadsClient, RunsClient, and CronClient.

Example

from langgraph_sdk import get_sync_client

# get top-level synchronous LangGraphClient
client = get_sync_client(url="http://localhost:8123")

# example usage: client.<model>.<method_name>()
assistant = client.assistants.get(assistant_id="some_uuid")
Data models for interacting with the LangGraph API.

Classes:

Name	Description
Config	Configuration options for a call.
Checkpoint	Represents a checkpoint in the execution process.
GraphSchema	Defines the structure and properties of a graph.
AssistantBase	Base model for an assistant.
AssistantVersion	Represents a specific version of an assistant.
Assistant	Represents an assistant with additional properties.
Interrupt	Represents an interruption in the execution flow.
Thread	Represents a conversation thread.
ThreadTask	Represents a task within a thread.
ThreadState	Represents the state of a thread.
ThreadUpdateStateResponse	Represents the response from updating a thread's state.
Run	Represents a single execution run.
Cron	Represents a scheduled task.
RunCreate	Defines the parameters for initiating a background run.
Item	Represents a single document or data entry in the graph's Store.
ListNamespaceResponse	Response structure for listing namespaces.
SearchItem	Item with an optional relevance score from search operations.
SearchItemsResponse	Response structure for searching items.
StreamPart	Represents a part of a stream response.
Send	Represents a message to be sent to a specific node in the graph.
Command	Represents one or more commands to control graph execution flow and state.
RunCreateMetadata	Metadata for a run creation request.
Attributes:

Name	Type	Description
Json		Represents a JSON-like structure, which can be None or a dictionary with string keys and any values.
RunStatus		Represents the status of a run:
ThreadStatus		Represents the status of a thread:
StreamMode		Defines the mode of streaming:
DisconnectMode		Specifies behavior on disconnection:
MultitaskStrategy		Defines how to handle multiple tasks:
OnConflictBehavior		Specifies behavior on conflict:
OnCompletionBehavior		Defines action after completion:
All		Represents a wildcard or 'all' selector.
IfNotExists		Specifies behavior if the thread doesn't exist:
CancelAction		Action to take when cancelling the run.
AssistantSortBy		The field to sort by.
ThreadSortBy		The field to sort by.
CronSortBy		The field to sort by.
SortOrder		The order to sort by.
 Json module-attribute ¶

Json = Optional[dict[str, Any]]
Represents a JSON-like structure, which can be None or a dictionary with string keys and any values.

 RunStatus module-attribute ¶

RunStatus = Literal[
    "pending",
    "running",
    "error",
    "success",
    "timeout",
    "interrupted",
]
Represents the status of a run: - "pending": The run is waiting to start. - "running": The run is currently executing. - "error": The run encountered an error and stopped. - "success": The run completed successfully. - "timeout": The run exceeded its time limit. - "interrupted": The run was manually stopped or interrupted.

 ThreadStatus module-attribute ¶

ThreadStatus = Literal[
    "idle", "busy", "interrupted", "error"
]
Represents the status of a thread: - "idle": The thread is not currently processing any task. - "busy": The thread is actively processing a task. - "interrupted": The thread's execution was interrupted. - "error": An exception occurred during task processing.

 StreamMode module-attribute ¶

StreamMode = Literal[
    "values",
    "messages",
    "updates",
    "events",
    "tasks",
    "checkpoints",
    "debug",
    "custom",
    "messages-tuple",
]
Defines the mode of streaming: - "values": Stream only the values. - "messages": Stream complete messages. - "updates": Stream updates to the state. - "events": Stream events occurring during execution. - "checkpoints": Stream checkpoints as they are created. - "tasks": Stream task start and finish events. - "debug": Stream detailed debug information. - "custom": Stream custom events.

 DisconnectMode module-attribute ¶

DisconnectMode = Literal['cancel', 'continue']
Specifies behavior on disconnection: - "cancel": Cancel the operation on disconnection. - "continue": Continue the operation even if disconnected.

 MultitaskStrategy module-attribute ¶

MultitaskStrategy = Literal[
    "reject", "interrupt", "rollback", "enqueue"
]
Defines how to handle multiple tasks: - "reject": Reject new tasks when busy. - "interrupt": Interrupt current task for new ones. - "rollback": Roll back current task and start new one. - "enqueue": Queue new tasks for later execution.

 OnConflictBehavior module-attribute ¶

OnConflictBehavior = Literal['raise', 'do_nothing']
Specifies behavior on conflict: - "raise": Raise an exception when a conflict occurs. - "do_nothing": Ignore conflicts and proceed.

 OnCompletionBehavior module-attribute ¶

OnCompletionBehavior = Literal['delete', 'keep']
Defines action after completion: - "delete": Delete resources after completion. - "keep": Retain resources after completion.

 All module-attribute ¶

All = Literal['*']
Represents a wildcard or 'all' selector.

 IfNotExists module-attribute ¶

IfNotExists = Literal['create', 'reject']
Specifies behavior if the thread doesn't exist: - "create": Create a new thread if it doesn't exist. - "reject": Reject the operation if the thread doesn't exist.

 CancelAction module-attribute ¶

CancelAction = Literal['interrupt', 'rollback']
Action to take when cancelling the run. - "interrupt": Simply cancel the run. - "rollback": Cancel the run. Then delete the run and associated checkpoints.

 AssistantSortBy module-attribute ¶

AssistantSortBy = Literal[
    "assistant_id",
    "graph_id",
    "name",
    "created_at",
    "updated_at",
]
The field to sort by.

 ThreadSortBy module-attribute ¶

ThreadSortBy = Literal[
    "thread_id", "status", "created_at", "updated_at"
]
The field to sort by.

 CronSortBy module-attribute ¶

CronSortBy = Literal[
    "cron_id",
    "assistant_id",
    "thread_id",
    "created_at",
    "updated_at",
    "next_run_date",
]
The field to sort by.

 SortOrder module-attribute ¶

SortOrder = Literal['asc', 'desc']
The order to sort by.

 Config ¶
Bases: TypedDict

Configuration options for a call.

Attributes:

Name	Type	Description
tags	list[str]	Tags for this call and any sub-calls (eg. a Chain calling an LLM).
recursion_limit	int	Maximum number of times a call can recurse. If not provided, defaults to 25.
configurable	dict[str, Any]	Runtime values for attributes previously made configurable on this Runnable,
 tags instance-attribute ¶

tags: list[str]
Tags for this call and any sub-calls (eg. a Chain calling an LLM). You can use these to filter calls.

 recursion_limit instance-attribute ¶

recursion_limit: int
Maximum number of times a call can recurse. If not provided, defaults to 25.

 configurable instance-attribute ¶

configurable: dict[str, Any]
Runtime values for attributes previously made configurable on this Runnable, or sub-Runnables, through .configurable_fields() or .configurable_alternatives(). Check .output_schema() for a description of the attributes that have been made configurable.

 Checkpoint ¶
Bases: TypedDict

Represents a checkpoint in the execution process.

Attributes:

Name	Type	Description
thread_id	str	Unique identifier for the thread associated with this checkpoint.
checkpoint_ns	str	Namespace for the checkpoint; used internally to manage subgraph state.
checkpoint_id	str | None	Optional unique identifier for the checkpoint itself.
checkpoint_map	dict[str, Any] | None	Optional dictionary containing checkpoint-specific data.
 thread_id instance-attribute ¶

thread_id: str
Unique identifier for the thread associated with this checkpoint.

 checkpoint_ns instance-attribute ¶

checkpoint_ns: str
Namespace for the checkpoint; used internally to manage subgraph state.

 checkpoint_id instance-attribute ¶

checkpoint_id: str | None
Optional unique identifier for the checkpoint itself.

 checkpoint_map instance-attribute ¶

checkpoint_map: dict[str, Any] | None
Optional dictionary containing checkpoint-specific data.

 GraphSchema ¶
Bases: TypedDict

Defines the structure and properties of a graph.

Attributes:

Name	Type	Description
graph_id	str	The ID of the graph.
input_schema	dict | None	The schema for the graph input.
output_schema	dict | None	The schema for the graph output.
state_schema	dict | None	The schema for the graph state.
config_schema	dict | None	The schema for the graph config.
context_schema	dict | None	The schema for the graph context.
 graph_id instance-attribute ¶

graph_id: str
The ID of the graph.

 input_schema instance-attribute ¶

input_schema: dict | None
The schema for the graph input. Missing if unable to generate JSON schema from graph.

 output_schema instance-attribute ¶

output_schema: dict | None
The schema for the graph output. Missing if unable to generate JSON schema from graph.

 state_schema instance-attribute ¶

state_schema: dict | None
The schema for the graph state. Missing if unable to generate JSON schema from graph.

 config_schema instance-attribute ¶

config_schema: dict | None
The schema for the graph config. Missing if unable to generate JSON schema from graph.

 context_schema instance-attribute ¶

context_schema: dict | None
The schema for the graph context. Missing if unable to generate JSON schema from graph.

 AssistantBase ¶
Bases: TypedDict

Base model for an assistant.

Attributes:

Name	Type	Description
assistant_id	str	The ID of the assistant.
graph_id	str	The ID of the graph.
config	Config	The assistant config.
context	Context	The static context of the assistant.
created_at	datetime	The time the assistant was created.
metadata	Json	The assistant metadata.
version	int	The version of the assistant
name	str	The name of the assistant
description	str | None	The description of the assistant
 assistant_id instance-attribute ¶

assistant_id: str
The ID of the assistant.

 graph_id instance-attribute ¶

graph_id: str
The ID of the graph.

 config instance-attribute ¶

config: Config
The assistant config.

 context instance-attribute ¶

context: Context
The static context of the assistant.

 created_at instance-attribute ¶

created_at: datetime
The time the assistant was created.

 metadata instance-attribute ¶

metadata: Json
The assistant metadata.

 version instance-attribute ¶

version: int
The version of the assistant

 name instance-attribute ¶

name: str
The name of the assistant

 description instance-attribute ¶

description: str | None
The description of the assistant

 AssistantVersion ¶
Bases: AssistantBase

Represents a specific version of an assistant.

Attributes:

Name	Type	Description
assistant_id	str	The ID of the assistant.
graph_id	str	The ID of the graph.
config	Config	The assistant config.
context	Context	The static context of the assistant.
created_at	datetime	The time the assistant was created.
metadata	Json	The assistant metadata.
version	int	The version of the assistant
name	str	The name of the assistant
description	str | None	The description of the assistant
 assistant_id instance-attribute ¶

assistant_id: str
The ID of the assistant.

 graph_id instance-attribute ¶

graph_id: str
The ID of the graph.

 config instance-attribute ¶

config: Config
The assistant config.

 context instance-attribute ¶

context: Context
The static context of the assistant.

 created_at instance-attribute ¶

created_at: datetime
The time the assistant was created.

 metadata instance-attribute ¶

metadata: Json
The assistant metadata.

 version instance-attribute ¶

version: int
The version of the assistant

 name instance-attribute ¶

name: str
The name of the assistant

 description instance-attribute ¶

description: str | None
The description of the assistant

 Assistant ¶
Bases: AssistantBase

Represents an assistant with additional properties.

Attributes:

Name	Type	Description
updated_at	datetime	The last time the assistant was updated.
assistant_id	str	The ID of the assistant.
graph_id	str	The ID of the graph.
config	Config	The assistant config.
context	Context	The static context of the assistant.
created_at	datetime	The time the assistant was created.
metadata	Json	The assistant metadata.
version	int	The version of the assistant
name	str	The name of the assistant
description	str | None	The description of the assistant
 updated_at instance-attribute ¶

updated_at: datetime
The last time the assistant was updated.

 assistant_id instance-attribute ¶

assistant_id: str
The ID of the assistant.

 graph_id instance-attribute ¶

graph_id: str
The ID of the graph.

 config instance-attribute ¶

config: Config
The assistant config.

 context instance-attribute ¶

context: Context
The static context of the assistant.

 created_at instance-attribute ¶

created_at: datetime
The time the assistant was created.

 metadata instance-attribute ¶

metadata: Json
The assistant metadata.

 version instance-attribute ¶

version: int
The version of the assistant

 name instance-attribute ¶

name: str
The name of the assistant

 description instance-attribute ¶

description: str | None
The description of the assistant

 Interrupt ¶
Bases: TypedDict

Represents an interruption in the execution flow.

Attributes:

Name	Type	Description
value	Any	The value associated with the interrupt.
id	str	The ID of the interrupt. Can be used to resume the interrupt.
 value instance-attribute ¶

value: Any
The value associated with the interrupt.

 id instance-attribute ¶

id: str
The ID of the interrupt. Can be used to resume the interrupt.

 Thread ¶
Bases: TypedDict

Represents a conversation thread.

Attributes:

Name	Type	Description
thread_id	str	The ID of the thread.
created_at	datetime	The time the thread was created.
updated_at	datetime	The last time the thread was updated.
metadata	Json	The thread metadata.
status	ThreadStatus	The status of the thread, one of 'idle', 'busy', 'interrupted'.
values	Json	The current state of the thread.
interrupts	dict[str, list[Interrupt]]	Mapping of task ids to interrupts that were raised in that task.
 thread_id instance-attribute ¶

thread_id: str
The ID of the thread.

 created_at instance-attribute ¶

created_at: datetime
The time the thread was created.

 updated_at instance-attribute ¶

updated_at: datetime
The last time the thread was updated.

 metadata instance-attribute ¶

metadata: Json
The thread metadata.

 status instance-attribute ¶

status: ThreadStatus
The status of the thread, one of 'idle', 'busy', 'interrupted'.

 values instance-attribute ¶

values: Json
The current state of the thread.

 interrupts instance-attribute ¶

interrupts: dict[str, list[Interrupt]]
Mapping of task ids to interrupts that were raised in that task.

 ThreadTask ¶
Bases: TypedDict

Represents a task within a thread.

 ThreadState ¶
Bases: TypedDict

Represents the state of a thread.

Attributes:

Name	Type	Description
values	list[dict] | dict[str, Any]	The state values.
next	Sequence[str]	The next nodes to execute. If empty, the thread is done until new input is
checkpoint	Checkpoint	The ID of the checkpoint.
metadata	Json	Metadata for this state
created_at	str | None	Timestamp of state creation
parent_checkpoint	Checkpoint | None	The ID of the parent checkpoint. If missing, this is the root checkpoint.
tasks	Sequence[ThreadTask]	Tasks to execute in this step. If already attempted, may contain an error.
interrupts	list[Interrupt]	Interrupts which were thrown in this thread.
 values instance-attribute ¶

values: list[dict] | dict[str, Any]
The state values.

 next instance-attribute ¶

next: Sequence[str]
The next nodes to execute. If empty, the thread is done until new input is received.

 checkpoint instance-attribute ¶

checkpoint: Checkpoint
The ID of the checkpoint.

 metadata instance-attribute ¶

metadata: Json
Metadata for this state

 created_at instance-attribute ¶

created_at: str | None
Timestamp of state creation

 parent_checkpoint instance-attribute ¶

parent_checkpoint: Checkpoint | None
The ID of the parent checkpoint. If missing, this is the root checkpoint.

 tasks instance-attribute ¶

tasks: Sequence[ThreadTask]
Tasks to execute in this step. If already attempted, may contain an error.

 interrupts instance-attribute ¶

interrupts: list[Interrupt]
Interrupts which were thrown in this thread.

 ThreadUpdateStateResponse ¶
Bases: TypedDict

Represents the response from updating a thread's state.

Attributes:

Name	Type	Description
checkpoint	Checkpoint	Checkpoint of the latest state.
 checkpoint instance-attribute ¶

checkpoint: Checkpoint
Checkpoint of the latest state.

 Run ¶
Bases: TypedDict

Represents a single execution run.

Attributes:

Name	Type	Description
run_id	str	The ID of the run.
thread_id	str	The ID of the thread.
assistant_id	str	The assistant that was used for this run.
created_at	datetime	The time the run was created.
updated_at	datetime	The last time the run was updated.
status	RunStatus	The status of the run. One of 'pending', 'running', "error", 'success', "timeout", "interrupted".
metadata	Json	The run metadata.
multitask_strategy	MultitaskStrategy	Strategy to handle concurrent runs on the same thread.
 run_id instance-attribute ¶

run_id: str
The ID of the run.

 thread_id instance-attribute ¶

thread_id: str
The ID of the thread.

 assistant_id instance-attribute ¶

assistant_id: str
The assistant that was used for this run.

 created_at instance-attribute ¶

created_at: datetime
The time the run was created.

 updated_at instance-attribute ¶

updated_at: datetime
The last time the run was updated.

 status instance-attribute ¶

status: RunStatus
The status of the run. One of 'pending', 'running', "error", 'success', "timeout", "interrupted".

 metadata instance-attribute ¶

metadata: Json
The run metadata.

 multitask_strategy instance-attribute ¶

multitask_strategy: MultitaskStrategy
Strategy to handle concurrent runs on the same thread.

 Cron ¶
Bases: TypedDict

Represents a scheduled task.

Attributes:

Name	Type	Description
cron_id	str	The ID of the cron.
assistant_id	str	The ID of the assistant.
thread_id	str | None	The ID of the thread.
end_time	datetime | None	The end date to stop running the cron.
schedule	str	The schedule to run, cron format.
created_at	datetime	The time the cron was created.
updated_at	datetime	The last time the cron was updated.
payload	dict	The run payload to use for creating new run.
user_id	str | None	The user ID of the cron.
next_run_date	datetime | None	The next run date of the cron.
metadata	dict	The metadata of the cron.
 cron_id instance-attribute ¶

cron_id: str
The ID of the cron.

 assistant_id instance-attribute ¶

assistant_id: str
The ID of the assistant.

 thread_id instance-attribute ¶

thread_id: str | None
The ID of the thread.

 end_time instance-attribute ¶

end_time: datetime | None
The end date to stop running the cron.

 schedule instance-attribute ¶

schedule: str
The schedule to run, cron format.

 created_at instance-attribute ¶

created_at: datetime
The time the cron was created.

 updated_at instance-attribute ¶

updated_at: datetime
The last time the cron was updated.

 payload instance-attribute ¶

payload: dict
The run payload to use for creating new run.

 user_id instance-attribute ¶

user_id: str | None
The user ID of the cron.

 next_run_date instance-attribute ¶

next_run_date: datetime | None
The next run date of the cron.

 metadata instance-attribute ¶

metadata: dict
The metadata of the cron.

 RunCreate ¶
Bases: TypedDict

Defines the parameters for initiating a background run.

Attributes:

Name	Type	Description
thread_id	str | None	The identifier of the thread to run. If not provided, the run is stateless.
assistant_id	str	The identifier of the assistant to use for this run.
input	dict | None	Initial input data for the run.
metadata	dict | None	Additional metadata to associate with the run.
config	Config | None	Configuration options for the run.
context	Context | None	The static context of the run.
checkpoint_id	str | None	The identifier of a checkpoint to resume from.
interrupt_before	list[str] | None	List of node names to interrupt execution before.
interrupt_after	list[str] | None	List of node names to interrupt execution after.
webhook	str | None	URL to send webhook notifications about the run's progress.
multitask_strategy	MultitaskStrategy | None	Strategy for handling concurrent runs on the same thread.
 thread_id instance-attribute ¶

thread_id: str | None
The identifier of the thread to run. If not provided, the run is stateless.

 assistant_id instance-attribute ¶

assistant_id: str
The identifier of the assistant to use for this run.

 input instance-attribute ¶

input: dict | None
Initial input data for the run.

 metadata instance-attribute ¶

metadata: dict | None
Additional metadata to associate with the run.

 config instance-attribute ¶

config: Config | None
Configuration options for the run.

 context instance-attribute ¶

context: Context | None
The static context of the run.

 checkpoint_id instance-attribute ¶

checkpoint_id: str | None
The identifier of a checkpoint to resume from.

 interrupt_before instance-attribute ¶

interrupt_before: list[str] | None
List of node names to interrupt execution before.

 interrupt_after instance-attribute ¶

interrupt_after: list[str] | None
List of node names to interrupt execution after.

 webhook instance-attribute ¶

webhook: str | None
URL to send webhook notifications about the run's progress.

 multitask_strategy instance-attribute ¶

multitask_strategy: MultitaskStrategy | None
Strategy for handling concurrent runs on the same thread.

 Item ¶
Bases: TypedDict

Represents a single document or data entry in the graph's Store.

Items are used to store cross-thread memories.

Attributes:

Name	Type	Description
namespace	list[str]	The namespace of the item. A namespace is analogous to a document's directory.
key	str	The unique identifier of the item within its namespace.
value	dict[str, Any]	The value stored in the item. This is the document itself.
created_at	datetime	The timestamp when the item was created.
updated_at	datetime	The timestamp when the item was last updated.
 namespace instance-attribute ¶

namespace: list[str]
The namespace of the item. A namespace is analogous to a document's directory.

 key instance-attribute ¶

key: str
The unique identifier of the item within its namespace.

In general, keys needn't be globally unique.

 value instance-attribute ¶

value: dict[str, Any]
The value stored in the item. This is the document itself.

 created_at instance-attribute ¶

created_at: datetime
The timestamp when the item was created.

 updated_at instance-attribute ¶

updated_at: datetime
The timestamp when the item was last updated.

 ListNamespaceResponse ¶
Bases: TypedDict

Response structure for listing namespaces.

Attributes:

Name	Type	Description
namespaces	list[list[str]]	A list of namespace paths, where each path is a list of strings.
 namespaces instance-attribute ¶

namespaces: list[list[str]]
A list of namespace paths, where each path is a list of strings.

 SearchItem ¶
Bases: Item

Item with an optional relevance score from search operations.

Attributes:

Name	Type	Description
score	Optional[float]	Relevance/similarity score. Included when searching a compatible store with a natural language query.
 namespace instance-attribute ¶

namespace: list[str]
The namespace of the item. A namespace is analogous to a document's directory.

 key instance-attribute ¶

key: str
The unique identifier of the item within its namespace.

In general, keys needn't be globally unique.

 value instance-attribute ¶

value: dict[str, Any]
The value stored in the item. This is the document itself.

 created_at instance-attribute ¶

created_at: datetime
The timestamp when the item was created.

 updated_at instance-attribute ¶

updated_at: datetime
The timestamp when the item was last updated.

 SearchItemsResponse ¶
Bases: TypedDict

Response structure for searching items.

Attributes:

Name	Type	Description
items	list[SearchItem]	A list of items matching the search criteria.
 items instance-attribute ¶

items: list[SearchItem]
A list of items matching the search criteria.

 StreamPart ¶
Bases: NamedTuple

Represents a part of a stream response.

Attributes:

Name	Type	Description
event	str	The type of event for this stream part.
data	dict	The data payload associated with the event.
 event instance-attribute ¶

event: str
The type of event for this stream part.

 data instance-attribute ¶

data: dict
The data payload associated with the event.

 Send ¶
Bases: TypedDict

Represents a message to be sent to a specific node in the graph.

This type is used to explicitly send messages to nodes in the graph, typically used within Command objects to control graph execution flow.

Attributes:

Name	Type	Description
node	str	The name of the target node to send the message to.
input	dict[str, Any] | None	Optional dictionary containing the input data to be passed to the node.
 node instance-attribute ¶

node: str
The name of the target node to send the message to.

 input instance-attribute ¶

input: dict[str, Any] | None
Optional dictionary containing the input data to be passed to the node.

If None, the node will be called with no input.

 Command ¶
Bases: TypedDict

Represents one or more commands to control graph execution flow and state.

This type defines the control commands that can be returned by nodes to influence graph execution. It lets you navigate to other nodes, update graph state, and resume from interruptions.

Attributes:

Name	Type	Description
goto	Send | str | Sequence[Send | str]	Specifies where execution should continue. Can be:
update	dict[str, Any] | Sequence[tuple[str, Any]]	Updates to apply to the graph's state. Can be:
resume	Any	Value to resume execution with after an interruption.
 goto instance-attribute ¶

goto: Send | str | Sequence[Send | str]
Specifies where execution should continue. Can be:

A string node name to navigate to
A Send object to execute a node with specific input
A sequence of node names or Send objects to execute in order
 update instance-attribute ¶

update: dict[str, Any] | Sequence[tuple[str, Any]]
Updates to apply to the graph's state. Can be:

A dictionary of state updates to merge
A sequence of (key, value) tuples for ordered updates
 resume instance-attribute ¶

resume: Any
Value to resume execution with after an interruption. Used in conjunction with interrupt() to implement control flow.

 RunCreateMetadata ¶
Bases: TypedDict

Metadata for a run creation request.

Attributes:

Name	Type	Description
run_id	str	The ID of the run.
thread_id	str | None	The ID of the thread.
 run_id instance-attribute ¶

run_id: str
The ID of the run.

 thread_id instance-attribute ¶

thread_id: str | None
The ID of the thread.

Modules:

Name	Description
exceptions	Exceptions used in the auth system.
types	Authentication and authorization types for LangGraph.
Classes:

Name	Description
Auth	Add custom authentication and authorization management to your LangGraph application.
 Auth ¶
Add custom authentication and authorization management to your LangGraph application.

The Auth class provides a unified system for handling authentication and authorization in LangGraph applications. It supports custom user authentication protocols and fine-grained authorization rules for different resources and actions.

To use, create a separate python file and add the path to the file to your LangGraph API configuration file (langgraph.json). Within that file, create an instance of the Auth class and register authentication and authorization handlers as needed.

Example langgraph.json file:


{
  "dependencies": ["."],
  "graphs": {
    "agent": "./my_agent/agent.py:graph"
  },
  "env": ".env",
  "auth": {
    "path": "./auth.py:my_auth"
  }
Then the LangGraph server will load your auth file and run it server-side whenever a request comes in.

Basic Usage

from langgraph_sdk import Auth

my_auth = Auth()

async def verify_token(token: str) -> str:
    # Verify token and return user_id
    # This would typically be a call to your auth server
    return "user_id"

@auth.authenticate
async def authenticate(authorization: str) -> str:
    # Verify token and return user_id
    result = await verify_token(authorization)
    if result != "user_id":
        raise Auth.exceptions.HTTPException(
            status_code=401, detail="Unauthorized"
        )
    return result

# Global fallback handler
@auth.on
async def authorize_default(params: Auth.on.value):
    return False # Reject all requests (default behavior)

@auth.on.threads.create
async def authorize_thread_create(params: Auth.on.threads.create.value):
    # Allow the allowed user to create a thread
    assert params.get("metadata", {}).get("owner") == "allowed_user"

@auth.on.store
async def authorize_store(ctx: Auth.types.AuthContext, value: Auth.types.on):
    assert ctx.user.identity in value["namespace"], "Not authorized"
Request Processing Flow
Authentication (your @auth.authenticate handler) is performed first on every request
For authorization, the most specific matching handler is called:
If a handler exists for the exact resource and action, it is used (e.g., @auth.on.threads.create)
Otherwise, if a handler exists for the resource with any action, it is used (e.g., @auth.on.threads)
Finally, if no specific handlers match, the global handler is used (e.g., @auth.on)
If no global handler is set, the request is accepted
This allows you to set default behavior with a global handler while overriding specific routes as needed.

Methods:

Name	Description
authenticate	Register an authentication handler function.
Attributes:

Name	Type	Description
types		Reference to auth type definitions.
exceptions		Reference to auth exception definitions.
on		Entry point for authorization handlers that control access to specific resources.
 types class-attribute instance-attribute ¶

types = types
Reference to auth type definitions.

Provides access to all type definitions used in the auth system, like ThreadsCreate, AssistantsRead, etc.

 exceptions class-attribute instance-attribute ¶

exceptions = exceptions
Reference to auth exception definitions.

Provides access to all exception definitions used in the auth system, like HTTPException, etc.

 on instance-attribute ¶

on = _On(self)
Entry point for authorization handlers that control access to specific resources.

The on class provides a flexible way to define authorization rules for different resources and actions in your application. It supports three main usage patterns:

Global handlers that run for all resources and actions
Resource-specific handlers that run for all actions on a resource
Resource and action specific handlers for fine-grained control
Each handler must be an async function that accepts two parameters
ctx (AuthContext): Contains request context and authenticated user info
value: The data being authorized (type varies by endpoint)
The handler should return one of:


- None or True: Accept the request
- False: Reject with 403 error
- FilterType: Apply filtering rules to the response
Examples
Global handler for all requests:


@auth.on
async def reject_unhandled_requests(ctx: AuthContext, value: Any) -> None:
    print(f"Request to {ctx.path} by {ctx.user.identity}")
    return False
Resource-specific handler. This would take precedence over the global handler for all actions on the threads resource:


@auth.on.threads
async def check_thread_access(ctx: AuthContext, value: Any) -> bool:
    # Allow access only to threads created by the user
    return value.get("created_by") == ctx.user.identity
Resource and action specific handler:


@auth.on.threads.delete
async def prevent_thread_deletion(ctx: AuthContext, value: Any) -> bool:
    # Only admins can delete threads
    return "admin" in ctx.user.permissions
Multiple resources or actions:


@auth.on(resources=["threads", "runs"], actions=["create", "update"])
async def rate_limit_writes(ctx: AuthContext, value: Any) -> bool:
    # Implement rate limiting for write operations
    return await check_rate_limit(ctx.user.identity)
Auth for the store resource is a bit different since its structure is developer defined. You typically want to enforce user creds in the namespace. Y


@auth.on.store
async def check_store_access(ctx: AuthContext, value: Auth.types.on) -> bool:
    # Assuming you structure your store like (store.aput((user_id, application_context), key, value))
    assert value["namespace"][0] == ctx.user.identity
 authenticate ¶

authenticate(fn: AH) -> AH
Register an authentication handler function.

The authentication handler is responsible for verifying credentials and returning user scopes. It can accept any of the following parameters by name:


- request (Request): The raw ASGI request object
- body (dict): The parsed request body
- path (str): The request path, e.g., "/threads/abcd-1234-abcd-1234/runs/abcd-1234-abcd-1234/stream"
- method (str): The HTTP method, e.g., "GET"
- path_params (dict[str, str]): URL path parameters, e.g., {"thread_id": "abcd-1234-abcd-1234", "run_id": "abcd-1234-abcd-1234"}
- query_params (dict[str, str]): URL query parameters, e.g., {"stream": "true"}
- headers (dict[bytes, bytes]): Request headers
- authorization (str | None): The Authorization header value (e.g., "Bearer <token>")
Parameters:

Name	Type	Description	Default
fn	AH	The authentication handler function to register. Must return a representation of the user. This could be a: - string (the user id) - dict containing {"identity": str, "permissions": list[str]} - or an object with identity and permissions properties Permissions can be optionally used by your handlers downstream.	required
Returns:

Type	Description
AH	The registered handler function.
Raises:

Type	Description
ValueError	If an authentication handler is already registered.
Examples
Basic token authentication:


@auth.authenticate
async def authenticate(authorization: str) -> str:
    user_id = verify_token(authorization)
    return user_id
Accept the full request context:


@auth.authenticate
async def authenticate(
    method: str,
    path: str,
    headers: dict[str, bytes]
) -> str:
    user = await verify_request(method, path, headers)
    return user
Return user name and permissions:


@auth.authenticate
async def authenticate(
    method: str,
    path: str,
    headers: dict[str, bytes]
) -> Auth.types.MinimalUserDict:
    permissions, user = await verify_request(method, path, headers)
    # Permissions could be things like ["runs:read", "runs:write", "threads:read", "threads:write"]
    return {
        "identity": user["id"],
        "permissions": permissions,
        "display_name": user["name"],
    }
Authentication and authorization types for LangGraph.

This module defines the core types used for authentication, authorization, and request handling in LangGraph. It includes user protocols, authentication contexts, and typed dictionaries for various API operations.

Note
All typing.TypedDict classes use total=False to make all fields typing.Optional by default.

Classes:

Name	Description
ThreadsCreate	Parameters for creating a new thread.
ThreadsRead	Parameters for reading thread state or run information.
ThreadsUpdate	Parameters for updating a thread or run.
ThreadsDelete	Parameters for deleting a thread.
ThreadsSearch	Parameters for searching threads.
RunsCreate	Payload for creating a run.
AssistantsCreate	Payload for creating an assistant.
AssistantsRead	Payload for reading an assistant.
AssistantsUpdate	Payload for updating an assistant.
AssistantsDelete	Payload for deleting an assistant.
AssistantsSearch	Payload for searching assistants.
StoreGet	Operation to retrieve a specific item by its namespace and key.
StoreSearch	Operation to search for items within a specified namespace hierarchy.
StoreListNamespaces	Operation to list and filter namespaces in the store.
StorePut	Operation to store, update, or delete an item in the store.
StoreDelete	Operation to delete an item from the store.
on	Namespace for type definitions of different API operations.
Attributes:

Name	Type	Description
MetadataInput		Type for arbitrary metadata attached to entities.
 RunStatus module-attribute ¶

RunStatus = Literal[
    "pending", "error", "success", "timeout", "interrupted"
]
Status of a run execution.

Values
pending: Run is queued or in progress
error: Run failed with an error
success: Run completed successfully
timeout: Run exceeded time limit
interrupted: Run was manually interrupted
 MultitaskStrategy module-attribute ¶

MultitaskStrategy = Literal[
    "reject", "rollback", "interrupt", "enqueue"
]
Strategy for handling multiple concurrent tasks.

Values
reject: Reject new tasks while one is in progress
rollback: Cancel current task and start new one
interrupt: Interrupt current task and start new one
enqueue: Queue new tasks to run after current one
 OnConflictBehavior module-attribute ¶

OnConflictBehavior = Literal['raise', 'do_nothing']
Behavior when encountering conflicts.

Values
raise: Raise an exception on conflict
do_nothing: Silently ignore conflicts
 IfNotExists module-attribute ¶

IfNotExists = Literal['create', 'reject']
Behavior when an entity doesn't exist.

Values
create: Create the entity
reject: Reject the operation
 FilterType module-attribute ¶

FilterType = Union[
    dict[
        str,
        Union[str, dict[Literal["$eq", "$contains"], str]],
    ],
    dict[str, str],
]
Response type for authorization handlers.

Supports exact matches and operators
Exact match shorthand: {"field": "value"}
Exact match: {"field": {"$eq": "value"}}
Contains: {"field": {"$contains": "value"}}
Examples
Simple exact match filter for the resource owner:


filter = {"owner": "user-abcd123"}
Explicit version of the exact match filter:


filter = {"owner": {"$eq": "user-abcd123"}}
Containment:


filter = {"participants": {"$contains": "user-abcd123"}}
Combining filters (treated as a logical AND):


filter = {"owner": "user-abcd123", "participants": {"$contains": "user-efgh456"}}
 ThreadStatus module-attribute ¶

ThreadStatus = Literal[
    "idle", "busy", "interrupted", "error"
]
Status of a thread.

Values
idle: Thread is available for work
busy: Thread is currently processing
interrupted: Thread was interrupted
error: Thread encountered an error
 MetadataInput module-attribute ¶

MetadataInput = dict[str, Any]
Type for arbitrary metadata attached to entities.

Allows storing custom key-value pairs with any entity. Keys must be strings, values can be any JSON-serializable type.

Examples

metadata = {
    "created_by": "user123",
    "priority": 1,
    "tags": ["important", "urgent"]
}
 HandlerResult module-attribute ¶

HandlerResult = Union[None, bool, FilterType]
The result of a handler can be: * None | True: accept the request. * False: reject the request with a 403 error * FilterType: filter to apply

 Authenticator module-attribute ¶

Authenticator = Callable[
    ...,
    Awaitable[
        Union[
            MinimalUser,
            str,
            BaseUser,
            MinimalUserDict,
            Mapping[str, Any],
        ],
    ],
]
Type for authentication functions.

An authenticator can return either: 1. A string (user_id) 2. A dict containing {"identity": str, "permissions": list[str]} 3. An object with identity and permissions properties

Permissions can be used downstream by your authorization logic to determine access permissions to different resources.

The authenticate decorator will automatically inject any of the following parameters by name if they are included in your function signature:

Parameters:

Name	Type	Description	Default
request	Request	The raw ASGI request object	required
body	dict	The parsed request body	required
path	str	The request path	required
method	str	The HTTP method (GET, POST, etc.)	required
path_params	dict[str, str] | None	URL path parameters	required
query_params	dict[str, str] | None	URL query parameters	required
headers	dict[str, bytes] | None	Request headers	required
authorization	str | None	The Authorization header value (e.g. "Bearer ")	required
Examples
Basic authentication with token:


from langgraph_sdk import Auth

auth = Auth()

@auth.authenticate
async def authenticate1(authorization: str) -> Auth.types.MinimalUserDict:
    return await get_user(authorization)
Authentication with multiple parameters:


@auth.authenticate
async def authenticate2(
    method: str,
    path: str,
    headers: dict[str, bytes]
) -> Auth.types.MinimalUserDict:
    # Custom auth logic using method, path and headers
    user = verify_request(method, path, headers)
    return user
Accepting the raw ASGI request:


MY_SECRET = "my-secret-key"
@auth.authenticate
async def get_current_user(request: Request) -> Auth.types.MinimalUserDict:
    try:
        token = (request.headers.get("authorization") or "").split(" ", 1)[1]
        payload = jwt.decode(token, MY_SECRET, algorithms=["HS256"])
    except (IndexError, InvalidTokenError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.myauth-provider.com/auth/v1/user",
            headers={"Authorization": f"Bearer {MY_SECRET}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="User not found")

        user_data = response.json()
        return {
            "identity": user_data["id"],
            "display_name": user_data.get("name"),
            "permissions": user_data.get("permissions", []),
            "is_authenticated": True,
        }
 MinimalUser ¶
Bases: Protocol

User objects must at least expose the identity property.

Attributes:

Name	Type	Description
identity	str	The unique identifier for the user.
 identity property ¶

identity: str
The unique identifier for the user.

This could be a username, email, or any other unique identifier used to distinguish between different users in the system.

 MinimalUserDict ¶
Bases: TypedDict

The dictionary representation of a user.

Attributes:

Name	Type	Description
identity	Required[str]	The required unique identifier for the user.
display_name	str	The typing.Optional display name for the user.
is_authenticated	bool	Whether the user is authenticated. Defaults to True.
permissions	Sequence[str]	A list of permissions associated with the user.
 identity instance-attribute ¶

identity: Required[str]
The required unique identifier for the user.

 display_name instance-attribute ¶

display_name: str
The typing.Optional display name for the user.

 is_authenticated instance-attribute ¶

is_authenticated: bool
Whether the user is authenticated. Defaults to True.

 permissions instance-attribute ¶

permissions: Sequence[str]
A list of permissions associated with the user.

You can use these in your @auth.on authorization logic to determine access permissions to different resources.

 BaseUser ¶
Bases: Protocol

The base ASGI user protocol

Methods:

Name	Description
__getitem__	Get a key from your minimal user dict.
__contains__	Check if a property exists.
__iter__	Iterate over the keys of the user.
Attributes:

Name	Type	Description
is_authenticated	bool	Whether the user is authenticated.
display_name	str	The display name of the user.
identity	str	The unique identifier for the user.
permissions	Sequence[str]	The permissions associated with the user.
 is_authenticated property ¶

is_authenticated: bool
Whether the user is authenticated.

 display_name property ¶

display_name: str
The display name of the user.

 identity property ¶

identity: str
The unique identifier for the user.

 permissions property ¶

permissions: Sequence[str]
The permissions associated with the user.

 __getitem__ ¶

__getitem__(key)
Get a key from your minimal user dict.

 __contains__ ¶

__contains__(key)
Check if a property exists.

 __iter__ ¶

__iter__()
Iterate over the keys of the user.

 StudioUser ¶
A user object that's populated from authenticated requests from the LangGraph studio.

Note: Studio auth can be disabled in your langgraph.json config.


{
  "auth": {
    "disable_studio_auth": true
  }
}
You can use isinstance checks in your authorization handlers (@auth.on) to control access specifically for developers accessing the instance from the LangGraph Studio UI.

Examples

@auth.on
async def allow_developers(ctx: Auth.types.AuthContext, value: Any) -> None:
    if isinstance(ctx.user, Auth.types.StudioUser):
        return None
    ...
    return False
 BaseAuthContext ¶
Base class for authentication context.

Provides the fundamental authentication information needed for authorization decisions.

Attributes:

Name	Type	Description
permissions	Sequence[str]	The permissions granted to the authenticated user.
user	BaseUser	The authenticated user.
 permissions instance-attribute ¶

permissions: Sequence[str]
The permissions granted to the authenticated user.

 user instance-attribute ¶

user: BaseUser
The authenticated user.

 AuthContext ¶
Bases: BaseAuthContext

Complete authentication context with resource and action information.

Extends BaseAuthContext with specific resource and action being accessed, allowing for fine-grained access control decisions.

Attributes:

Name	Type	Description
resource	Literal['runs', 'threads', 'crons', 'assistants', 'store']	The resource being accessed.
action	Literal['create', 'read', 'update', 'delete', 'search', 'create_run', 'put', 'get', 'list_namespaces']	The action being performed on the resource.
permissions	Sequence[str]	The permissions granted to the authenticated user.
user	BaseUser	The authenticated user.
 resource instance-attribute ¶

resource: Literal[
    "runs", "threads", "crons", "assistants", "store"
]
The resource being accessed.

 action instance-attribute ¶

action: Literal[
    "create",
    "read",
    "update",
    "delete",
    "search",
    "create_run",
    "put",
    "get",
    "list_namespaces",
]
The action being performed on the resource.

Most resources support the following actions: - create: Create a new resource - read: Read information about a resource - update: Update an existing resource - delete: Delete a resource - search: Search for resources

The store supports the following actions: - put: Add or update a document in the store - get: Get a document from the store - list_namespaces: List the namespaces in the store

 permissions instance-attribute ¶

permissions: Sequence[str]
The permissions granted to the authenticated user.

 user instance-attribute ¶

user: BaseUser
The authenticated user.

 ThreadsCreate ¶
Bases: TypedDict

Parameters for creating a new thread.

Examples

create_params = {
    "thread_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    "metadata": {"owner": "user123"},
    "if_exists": "do_nothing"
}
Attributes:

Name	Type	Description
thread_id	UUID	Unique identifier for the thread.
metadata	MetadataInput	typing.Optional metadata to attach to the thread.
if_exists	OnConflictBehavior	Behavior when a thread with the same ID already exists.
 thread_id instance-attribute ¶

thread_id: UUID
Unique identifier for the thread.

 metadata instance-attribute ¶

metadata: MetadataInput
typing.Optional metadata to attach to the thread.

 if_exists instance-attribute ¶

if_exists: OnConflictBehavior
Behavior when a thread with the same ID already exists.

 ThreadsRead ¶
Bases: TypedDict

Parameters for reading thread state or run information.

This type is used in three contexts: 1. Reading thread, thread version, or thread state information: Only thread_id is provided 2. Reading run information: Both thread_id and run_id are provided

Attributes:

Name	Type	Description
thread_id	UUID	Unique identifier for the thread.
run_id	UUID | None	Run ID to filter by. Only used when reading run information within a thread.
 thread_id instance-attribute ¶

thread_id: UUID
Unique identifier for the thread.

 run_id instance-attribute ¶

run_id: UUID | None
Run ID to filter by. Only used when reading run information within a thread.

 ThreadsUpdate ¶
Bases: TypedDict

Parameters for updating a thread or run.

Called for updates to a thread, thread version, or run cancellation.

Attributes:

Name	Type	Description
thread_id	UUID	Unique identifier for the thread.
metadata	MetadataInput	typing.Optional metadata to update.
action	Literal['interrupt', 'rollback'] | None	typing.Optional action to perform on the thread.
 thread_id instance-attribute ¶

thread_id: UUID
Unique identifier for the thread.

 metadata instance-attribute ¶

metadata: MetadataInput
typing.Optional metadata to update.

 action instance-attribute ¶

action: Literal['interrupt', 'rollback'] | None
typing.Optional action to perform on the thread.

 ThreadsDelete ¶
Bases: TypedDict

Parameters for deleting a thread.

Called for deletes to a thread, thread version, or run

Attributes:

Name	Type	Description
thread_id	UUID	Unique identifier for the thread.
run_id	UUID | None	typing.Optional run ID to filter by.
 thread_id instance-attribute ¶

thread_id: UUID
Unique identifier for the thread.

 run_id instance-attribute ¶

run_id: UUID | None
typing.Optional run ID to filter by.

 ThreadsSearch ¶
Bases: TypedDict

Parameters for searching threads.

Called for searches to threads or runs.

Attributes:

Name	Type	Description
metadata	MetadataInput	typing.Optional metadata to filter by.
values	MetadataInput	typing.Optional values to filter by.
status	ThreadStatus | None	typing.Optional status to filter by.
limit	int	Maximum number of results to return.
offset	int	Offset for pagination.
thread_id	UUID | None	typing.Optional thread ID to filter by.
 metadata instance-attribute ¶

metadata: MetadataInput
typing.Optional metadata to filter by.

 values instance-attribute ¶

values: MetadataInput
typing.Optional values to filter by.

 status instance-attribute ¶

status: ThreadStatus | None
typing.Optional status to filter by.

 limit instance-attribute ¶

limit: int
Maximum number of results to return.

 offset instance-attribute ¶

offset: int
Offset for pagination.

 thread_id instance-attribute ¶

thread_id: UUID | None
typing.Optional thread ID to filter by.

 RunsCreate ¶
Bases: TypedDict

Payload for creating a run.

Examples

create_params = {
    "assistant_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    "thread_id": UUID("123e4567-e89b-12d3-a456-426614174001"),
    "run_id": UUID("123e4567-e89b-12d3-a456-426614174002"),
    "status": "pending",
    "metadata": {"owner": "user123"},
    "prevent_insert_if_inflight": True,
    "multitask_strategy": "reject",
    "if_not_exists": "create",
    "after_seconds": 10,
    "kwargs": {"key": "value"},
    "action": "interrupt"
}
Attributes:

Name	Type	Description
assistant_id	UUID | None	typing.Optional assistant ID to use for this run.
thread_id	UUID | None	typing.Optional thread ID to use for this run.
run_id	UUID | None	typing.Optional run ID to use for this run.
status	RunStatus | None	typing.Optional status for this run.
metadata	MetadataInput	typing.Optional metadata for the run.
prevent_insert_if_inflight	bool	Prevent inserting a new run if one is already in flight.
multitask_strategy	MultitaskStrategy	Multitask strategy for this run.
if_not_exists	IfNotExists	IfNotExists for this run.
after_seconds	int	Number of seconds to wait before creating the run.
kwargs	dict[str, Any]	Keyword arguments to pass to the run.
action	Literal['interrupt', 'rollback'] | None	Action to take if updating an existing run.
 assistant_id instance-attribute ¶

assistant_id: UUID | None
typing.Optional assistant ID to use for this run.

 thread_id instance-attribute ¶

thread_id: UUID | None
typing.Optional thread ID to use for this run.

 run_id instance-attribute ¶

run_id: UUID | None
typing.Optional run ID to use for this run.

 status instance-attribute ¶

status: RunStatus | None
typing.Optional status for this run.

 metadata instance-attribute ¶

metadata: MetadataInput
typing.Optional metadata for the run.

 prevent_insert_if_inflight instance-attribute ¶

prevent_insert_if_inflight: bool
Prevent inserting a new run if one is already in flight.

 multitask_strategy instance-attribute ¶

multitask_strategy: MultitaskStrategy
Multitask strategy for this run.

 if_not_exists instance-attribute ¶

if_not_exists: IfNotExists
IfNotExists for this run.

 after_seconds instance-attribute ¶

after_seconds: int
Number of seconds to wait before creating the run.

 kwargs instance-attribute ¶

kwargs: dict[str, Any]
Keyword arguments to pass to the run.

 action instance-attribute ¶

action: Literal['interrupt', 'rollback'] | None
Action to take if updating an existing run.

 AssistantsCreate ¶
Bases: TypedDict

Payload for creating an assistant.

Examples

create_params = {
    "assistant_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    "graph_id": "graph123",
    "config": {"tags": ["tag1", "tag2"]},
    "context": {"key": "value"},
    "metadata": {"owner": "user123"},
    "if_exists": "do_nothing",
    "name": "Assistant 1"
}
Attributes:

Name	Type	Description
assistant_id	UUID	Unique identifier for the assistant.
graph_id	str	Graph ID to use for this assistant.
config	dict[str, Any]	typing.Optional configuration for the assistant.
metadata	MetadataInput	typing.Optional metadata to attach to the assistant.
if_exists	OnConflictBehavior	Behavior when an assistant with the same ID already exists.
name	str	Name of the assistant.
 assistant_id instance-attribute ¶

assistant_id: UUID
Unique identifier for the assistant.

 graph_id instance-attribute ¶

graph_id: str
Graph ID to use for this assistant.

 config instance-attribute ¶

config: dict[str, Any]
typing.Optional configuration for the assistant.

 metadata instance-attribute ¶

metadata: MetadataInput
typing.Optional metadata to attach to the assistant.

 if_exists instance-attribute ¶

if_exists: OnConflictBehavior
Behavior when an assistant with the same ID already exists.

 name instance-attribute ¶

name: str
Name of the assistant.

 AssistantsRead ¶
Bases: TypedDict

Payload for reading an assistant.

Examples

read_params = {
    "assistant_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    "metadata": {"owner": "user123"}
}
Attributes:

Name	Type	Description
assistant_id	UUID	Unique identifier for the assistant.
metadata	MetadataInput	typing.Optional metadata to filter by.
 assistant_id instance-attribute ¶

assistant_id: UUID
Unique identifier for the assistant.

 metadata instance-attribute ¶

metadata: MetadataInput
typing.Optional metadata to filter by.

 AssistantsUpdate ¶
Bases: TypedDict

Payload for updating an assistant.

Examples

update_params = {
    "assistant_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    "graph_id": "graph123",
    "config": {"tags": ["tag1", "tag2"]},
    "context": {"key": "value"},
    "metadata": {"owner": "user123"},
    "name": "Assistant 1",
    "version": 1
}
Attributes:

Name	Type	Description
assistant_id	UUID	Unique identifier for the assistant.
graph_id	str | None	typing.Optional graph ID to update.
config	dict[str, Any]	typing.Optional configuration to update.
context	dict[str, Any]	The static context of the assistant.
metadata	MetadataInput	typing.Optional metadata to update.
name	str | None	typing.Optional name to update.
version	int | None	typing.Optional version to update.
 assistant_id instance-attribute ¶

assistant_id: UUID
Unique identifier for the assistant.

 graph_id instance-attribute ¶

graph_id: str | None
typing.Optional graph ID to update.

 config instance-attribute ¶

config: dict[str, Any]
typing.Optional configuration to update.

 context instance-attribute ¶

context: dict[str, Any]
The static context of the assistant.

 metadata instance-attribute ¶

metadata: MetadataInput
typing.Optional metadata to update.

 name instance-attribute ¶

name: str | None
typing.Optional name to update.

 version instance-attribute ¶

version: int | None
typing.Optional version to update.

 AssistantsDelete ¶
Bases: TypedDict

Payload for deleting an assistant.

Examples

delete_params = {
    "assistant_id": UUID("123e4567-e89b-12d3-a456-426614174000")
}
Attributes:

Name	Type	Description
assistant_id	UUID	Unique identifier for the assistant.
 assistant_id instance-attribute ¶

assistant_id: UUID
Unique identifier for the assistant.

 AssistantsSearch ¶
Bases: TypedDict

Payload for searching assistants.

Examples

search_params = {
    "graph_id": "graph123",
    "metadata": {"owner": "user123"},
    "limit": 10,
    "offset": 0
}
Attributes:

Name	Type	Description
graph_id	str | None	typing.Optional graph ID to filter by.
metadata	MetadataInput	typing.Optional metadata to filter by.
limit	int	Maximum number of results to return.
offset	int	Offset for pagination.
 graph_id instance-attribute ¶

graph_id: str | None
typing.Optional graph ID to filter by.

 metadata instance-attribute ¶

metadata: MetadataInput
typing.Optional metadata to filter by.

 limit instance-attribute ¶

limit: int
Maximum number of results to return.

 offset instance-attribute ¶

offset: int
Offset for pagination.

 CronsCreate ¶
Bases: TypedDict

Payload for creating a cron job.

Examples

create_params = {
    "payload": {"key": "value"},
    "schedule": "0 0 * * *",
    "cron_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    "thread_id": UUID("123e4567-e89b-12d3-a456-426614174001"),
    "user_id": "user123",
    "end_time": datetime(2024, 3, 16, 10, 0, 0)
}
Attributes:

Name	Type	Description
payload	dict[str, Any]	Payload for the cron job.
schedule	str	Schedule for the cron job.
cron_id	UUID | None	typing.Optional unique identifier for the cron job.
thread_id	UUID | None	typing.Optional thread ID to use for this cron job.
user_id	str | None	typing.Optional user ID to use for this cron job.
end_time	datetime | None	typing.Optional end time for the cron job.
 payload instance-attribute ¶

payload: dict[str, Any]
Payload for the cron job.

 schedule instance-attribute ¶

schedule: str
Schedule for the cron job.

 cron_id instance-attribute ¶

cron_id: UUID | None
typing.Optional unique identifier for the cron job.

 thread_id instance-attribute ¶

thread_id: UUID | None
typing.Optional thread ID to use for this cron job.

 user_id instance-attribute ¶

user_id: str | None
typing.Optional user ID to use for this cron job.

 end_time instance-attribute ¶

end_time: datetime | None
typing.Optional end time for the cron job.

 CronsDelete ¶
Bases: TypedDict

Payload for deleting a cron job.

Examples

delete_params = {
    "cron_id": UUID("123e4567-e89b-12d3-a456-426614174000")
}
Attributes:

Name	Type	Description
cron_id	UUID	Unique identifier for the cron job.
 cron_id instance-attribute ¶

cron_id: UUID
Unique identifier for the cron job.

 CronsRead ¶
Bases: TypedDict

Payload for reading a cron job.

Examples

read_params = {
    "cron_id": UUID("123e4567-e89b-12d3-a456-426614174000")
}
Attributes:

Name	Type	Description
cron_id	UUID	Unique identifier for the cron job.
 cron_id instance-attribute ¶

cron_id: UUID
Unique identifier for the cron job.

 CronsUpdate ¶
Bases: TypedDict

Payload for updating a cron job.

Examples

update_params = {
    "cron_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    "payload": {"key": "value"},
    "schedule": "0 0 * * *"
}
Attributes:

Name	Type	Description
cron_id	UUID	Unique identifier for the cron job.
payload	dict[str, Any] | None	typing.Optional payload to update.
schedule	str | None	typing.Optional schedule to update.
 cron_id instance-attribute ¶

cron_id: UUID
Unique identifier for the cron job.

 payload instance-attribute ¶

payload: dict[str, Any] | None
typing.Optional payload to update.

 schedule instance-attribute ¶

schedule: str | None
typing.Optional schedule to update.

 CronsSearch ¶
Bases: TypedDict

Payload for searching cron jobs.

Examples

search_params = {
    "assistant_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    "thread_id": UUID("123e4567-e89b-12d3-a456-426614174001"),
    "limit": 10,
    "offset": 0
}
Attributes:

Name	Type	Description
assistant_id	UUID | None	typing.Optional assistant ID to filter by.
thread_id	UUID | None	typing.Optional thread ID to filter by.
limit	int	Maximum number of results to return.
offset	int	Offset for pagination.
 assistant_id instance-attribute ¶

assistant_id: UUID | None
typing.Optional assistant ID to filter by.

 thread_id instance-attribute ¶

thread_id: UUID | None
typing.Optional thread ID to filter by.

 limit instance-attribute ¶

limit: int
Maximum number of results to return.

 offset instance-attribute ¶

offset: int
Offset for pagination.

 StoreGet ¶
Bases: TypedDict

Operation to retrieve a specific item by its namespace and key.

Attributes:

Name	Type	Description
namespace	tuple[str, ...]	Hierarchical path that uniquely identifies the item's location.
key	str	Unique identifier for the item within its specific namespace.
 namespace instance-attribute ¶

namespace: tuple[str, ...]
Hierarchical path that uniquely identifies the item's location.

 key instance-attribute ¶

key: str
Unique identifier for the item within its specific namespace.

 StoreSearch ¶
Bases: TypedDict

Operation to search for items within a specified namespace hierarchy.

Attributes:

Name	Type	Description
namespace	tuple[str, ...]	Prefix filter for defining the search scope.
filter	dict[str, Any] | None	Key-value pairs for filtering results based on exact matches or comparison operators.
limit	int	Maximum number of items to return in the search results.
offset	int	Number of matching items to skip for pagination.
query	str | None	Naturalj language search query for semantic search capabilities.
 namespace instance-attribute ¶

namespace: tuple[str, ...]
Prefix filter for defining the search scope.

 filter instance-attribute ¶

filter: dict[str, Any] | None
Key-value pairs for filtering results based on exact matches or comparison operators.

 limit instance-attribute ¶

limit: int
Maximum number of items to return in the search results.

 offset instance-attribute ¶

offset: int
Number of matching items to skip for pagination.

 query instance-attribute ¶

query: str | None
Naturalj language search query for semantic search capabilities.

 StoreListNamespaces ¶
Bases: TypedDict

Operation to list and filter namespaces in the store.

Attributes:

Name	Type	Description
namespace	tuple[str, ...] | None	Prefix filter namespaces.
suffix	tuple[str, ...] | None	Optional conditions for filtering namespaces.
max_depth	int | None	Maximum depth of namespace hierarchy to return.
limit	int	Maximum number of namespaces to return.
offset	int	Number of namespaces to skip for pagination.
 namespace instance-attribute ¶

namespace: tuple[str, ...] | None
Prefix filter namespaces.

 suffix instance-attribute ¶

suffix: tuple[str, ...] | None
Optional conditions for filtering namespaces.

 max_depth instance-attribute ¶

max_depth: int | None
Maximum depth of namespace hierarchy to return.

Note
Namespaces deeper than this level will be truncated.

 limit instance-attribute ¶

limit: int
Maximum number of namespaces to return.

 offset instance-attribute ¶

offset: int
Number of namespaces to skip for pagination.

 StorePut ¶
Bases: TypedDict

Operation to store, update, or delete an item in the store.

Attributes:

Name	Type	Description
namespace	tuple[str, ...]	Hierarchical path that identifies the location of the item.
key	str	Unique identifier for the item within its namespace.
value	dict[str, Any] | None	The data to store, or None to mark the item for deletion.
index	Literal[False] | list[str] | None	Optional index configuration for full-text search.
 namespace instance-attribute ¶

namespace: tuple[str, ...]
Hierarchical path that identifies the location of the item.

 key instance-attribute ¶

key: str
Unique identifier for the item within its namespace.

 value instance-attribute ¶

value: dict[str, Any] | None
The data to store, or None to mark the item for deletion.

 index instance-attribute ¶

index: Literal[False] | list[str] | None
Optional index configuration for full-text search.

 StoreDelete ¶
Bases: TypedDict

Operation to delete an item from the store.

Attributes:

Name	Type	Description
namespace	tuple[str, ...]	Hierarchical path that uniquely identifies the item's location.
key	str	Unique identifier for the item within its specific namespace.
 namespace instance-attribute ¶

namespace: tuple[str, ...]
Hierarchical path that uniquely identifies the item's location.

 key instance-attribute ¶

key: str
Unique identifier for the item within its specific namespace.

 on ¶
Namespace for type definitions of different API operations.

This class organizes type definitions for create, read, update, delete, and search operations across different resources (threads, assistants, crons).

Usage

from langgraph_sdk import Auth

auth = Auth()

@auth.on
def handle_all(params: Auth.on.value):
    raise Exception("Not authorized")

@auth.on.threads.create
def handle_thread_create(params: Auth.on.threads.create.value):
    # Handle thread creation
    pass

@auth.on.assistants.search
def handle_assistant_search(params: Auth.on.assistants.search.value):
    # Handle assistant search
    pass
Classes:

Name	Description
threads	Types for thread-related operations.
assistants	Types for assistant-related operations.
crons	Types for cron-related operations.
store	Types for store-related operations.
 threads ¶
Types for thread-related operations.

Classes:

Name	Description
create	Type for thread creation parameters.
create_run	Type for creating or streaming a run.
read	Type for thread read parameters.
update	Type for thread update parameters.
delete	Type for thread deletion parameters.
search	Type for thread search parameters.
 create ¶
Type for thread creation parameters.

 create_run ¶
Type for creating or streaming a run.

 read ¶
Type for thread read parameters.

 update ¶
Type for thread update parameters.

 delete ¶
Type for thread deletion parameters.

 search ¶
Type for thread search parameters.

 assistants ¶
Types for assistant-related operations.

Classes:

Name	Description
create	Type for assistant creation parameters.
read	Type for assistant read parameters.
update	Type for assistant update parameters.
delete	Type for assistant deletion parameters.
search	Type for assistant search parameters.
 create ¶
Type for assistant creation parameters.

 read ¶
Type for assistant read parameters.

 update ¶
Type for assistant update parameters.

 delete ¶
Type for assistant deletion parameters.

 search ¶
Type for assistant search parameters.

 crons ¶
Types for cron-related operations.

Classes:

Name	Description
create	Type for cron creation parameters.
read	Type for cron read parameters.
update	Type for cron update parameters.
delete	Type for cron deletion parameters.
search	Type for cron search parameters.
 create ¶
Type for cron creation parameters.

 read ¶
Type for cron read parameters.

 update ¶
Type for cron update parameters.

 delete ¶
Type for cron deletion parameters.

 search ¶
Type for cron search parameters.

 store ¶
Types for store-related operations.

Classes:

Name	Description
put	Type for store put parameters.
get	Type for store get parameters.
search	Type for store search parameters.
delete	Type for store delete parameters.
list_namespaces	Type for store list namespaces parameters.
 put ¶
Type for store put parameters.

 get ¶
Type for store get parameters.

 search ¶
Type for store search parameters.

 delete ¶
Type for store delete parameters.

 list_namespaces ¶
Type for store list namespaces parameters.

Exceptions used in the auth system.

Classes:

Name	Description
HTTPException	HTTP exception that you can raise to return a specific HTTP error response.
 HTTPException ¶
Bases: Exception

HTTP exception that you can raise to return a specific HTTP error response.

Since this is defined in the auth module, we default to a 401 status code.

Parameters:

Name	Type	Description	Default
status_code	int	HTTP status code for the error. Defaults to 401 "Unauthorized".	401
detail	str | None	Detailed error message. If None, uses a default message based on the status code.	None
headers	Mapping[str, str] | None	Additional HTTP headers to include in the error response.	None
Example
Default:


raise HTTPException()
# HTTPException(status_code=401, detail='Unauthorized')
Add headers:


raise HTTPException(headers={"X-Custom-Header": "Custom Value"})
# HTTPException(status_code=401, detail='Unauthorized', headers={"WWW-Authenticate": "Bearer"})
Custom error:


raise HTTPException(status_code=404, detail="Not found")
 Back to top
Previous
MCP Adapters
Next
RemoteGraph
Copyright © 2025 LangChain, Inc | Consent Preferences
Made with Material for MkDocs
