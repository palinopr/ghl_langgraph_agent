# Add custom authentication

This guide shows how to add custom authentication to your LangGraph Platform application. This guide applies to both LangGraph Platform and self-hosted deployments. It does not apply to isolated usage of the LangGraph open source library in your own custom server.

## Add custom authentication to your deployment

To leverage custom authentication and access user-level metadata in your deployments, set up custom authentication to automatically populate the `config["configurable"]["langgraph_auth_user"]` object through a custom authentication handler. You can then access this object in your graph with the `langgraph_auth_user` key to [allow an agent to perform authenticated actions on behalf of the user](#enable-agent-authentication).

1. Implement authentication:

<Note>
  Without a custom `@auth.authenticate` handler, LangGraph sees only the API-key owner (usually the developer), so requests aren't scoped to individual end-users. To propagate custom tokens, you must implement your own handler.
</Note>

```python
from langgraph_sdk import Auth
import requests

auth = Auth()

def is_valid_key(api_key: str) -> bool:
    is_valid = # your API key validation logic
    return is_valid

@auth.authenticate # (1)!
async def authenticate(headers: dict) -> Auth.types.MinimalUserDict:
    api_key = headers.get("x-api-key")
    if not api_key or not is_valid_key(api_key):
        raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid API key")

    # Fetch user-specific tokens from your secret store
    user_tokens = await fetch_user_tokens(api_key)

    return { # (2)!
        "identity": api_key,  #  fetch user ID from LangSmith
        "github_token" : user_tokens.github_token
        "jira_token" : user_tokens.jira_token
        # ... custom fields/secrets here
    }
```

1. This handler receives the request (headers, etc.), validates the user, and returns a dictionary with at least an identity field.
2. You can add any custom fields you want (e.g., OAuth tokens, roles, org IDs, etc.).
3. In your `langgraph.json`, add the path to your auth file:

```json hl_lines="7-9"
{
  "dependencies": ["."],
  "graphs": {
    "agent": "./agent.py:graph"
  },
  "env": ".env",
  "auth": {
    "path": "./auth.py:my_auth"
  }
}
```

3. Once you've set up authentication in your server, requests must include the required authorization information based on your chosen scheme. Assuming you are using JWT token authentication, you could access your deployments using any of the following methods:

<Tabs>
  <Tab title="Python Client">
    ```python
    from langgraph_sdk import get_client

    my_token = "your-token" # In practice, you would generate a signed token with your auth provider
    client = get_client(
        url="http://localhost:2024",
        headers={"Authorization": f"Bearer {my_token}"}
    )
    threads = await client.threads.search()
    ```
  </Tab>

  <Tab title="Python RemoteGraph">
    ```python
    from langgraph.pregel.remote import RemoteGraph

    my_token = "your-token" # In practice, you would generate a signed token with your auth provider
    remote-graph = RemoteGraph(
        "agent",
        url="http://localhost:2024",
        headers={"Authorization": f"Bearer {my_token}"}
    )
    threads = await remote-graph.ainvoke(...)
    ```
  </Tab>

  <Tab title="JavaScript Client">
    ```javascript
    import { Client } from "@langchain/langgraph-sdk";

    const my_token = "your-token"; // In practice, you would generate a signed token with your auth provider
    const client = new Client({
    apiUrl: "http://localhost:2024",
    defaultHeaders: { Authorization: `Bearer ${my_token}` },
    });
    const threads = await client.threads.search();
    ```
  </Tab>

  <Tab title="JavaScript RemoteGraph">
    ```javascript
    import { RemoteGraph } from "@langchain/langgraph/remote";

    const my_token = "your-token"; // In practice, you would generate a signed token with your auth provider
    const remoteGraph = new RemoteGraph({
    graphId: "agent",
    url: "http://localhost:2024",
    headers: { Authorization: `Bearer ${my_token}` },
    });
    const threads = await remoteGraph.invoke(...);
    ```
  </Tab>

  <Tab title="CURL">
    ```bash
    curl -H "Authorization: Bearer ${your-token}" http://localhost:2024/threads
    ```
  </Tab>
</Tabs>

## Enable agent authentication

After [authentication](#add-custom-authentication-to-your-deployment), the platform creates a special configuration object (`config`) that is passed to LangGraph Platform deployment. This object contains information about the current user, including any custom fields you return from your `@auth.authenticate` handler.

To allow an agent to perform authenticated actions on behalf of the user, access this object in your graph with the `langgraph_auth_user` key:

```python
def my_node(state, config):
    user_config = config["configurable"].get("langgraph_auth_user")
    # token was resolved during the @auth.authenticate function
    token = user_config.get("github_token","")
    ...
```

<Note>
  Fetch user credentials from a secure secret store. Storing secrets in graph state is not recommended.
</Note>

### Authorizing a Studio user

By default, if you add custom authorization on your resources, this will also apply to interactions made from the Studio. If you want, you can handle logged-in Studio users differently by checking [is\_studio\_user()](https://langchain-ai.github.io/langgraph/cloud/reference/sdk/python_sdk_ref/#langgraph_sdk.auth.types.StudioUser).

<Note>
  `is_studio_user` was added in version 0.1.73 of the langgraph-sdk. If you're on an older version, you can still check whether `isinstance(ctx.user, StudioUser)`.
</Note>

```python
from langgraph_sdk.auth import is_studio_user, Auth
auth = Auth()

# ... Setup authenticate, etc.

@auth.on
async def add_owner(
    ctx: Auth.types.AuthContext,
    value: dict  # The payload being sent to this access method
) -> dict:  # Returns a filter dict that restricts access to resources
    if is_studio_user(ctx.user):
        return {}

    filters = {"owner": ctx.user.identity}
    metadata = value.setdefault("metadata", {})
    metadata.update(filters)
    return filters
```

Only use this if you want to permit developer access to a graph deployed on the managed LangGraph Platform SaaS.

## Learn more

* [Authentication & Access Control](/langgraph-platform/auth)
* [LangGraph Platform](/langgraph-platform/index)
* [Setting up custom authentication tutorial](/langgraph-platform/set-up-custom-auth)