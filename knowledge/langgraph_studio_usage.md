# Use LangGraph Studio

<Info>
  **Prerequisites**

  * [LangGraph Studio Overview](/langgraph-platform/langgraph-studio)
</Info>

LangGraph Studio supports connecting to two types of graphs:

* Graphs deployed on [LangGraph Platform](/langgraph-platform/deployment-quickstart).
* Graphs running locally via the [LangGraph Server](/langgraph-platform/local-server).

LangGraph Studio is accessed from the LangSmith UI, within the LangGraph Platform Deployments tab.

For applications that are [deployed](/langgraph-platform/deployment-quickstart) on LangGraph Platform, you can access Studio as part of that deployment. To do so, navigate to the deployment in LangGraph Platform within the LangSmith UI and click the "LangGraph Studio" button.

This will load the Studio UI connected to your live deployment, allowing you to create, read, and update the [threads](https://langchain-ai.github.io/langgraph/concepts/persistence/#threads), [assistants](/langgraph-platform/assistants), and [memory](https://langchain-ai.github.io/langgraph/concepts/memory/) in that deployment.

## Local development server

To test your locally running application using LangGraph Studio, ensure your application is set up following [this guide](https://langchain-ai.github.io/langgraph/cloud/deployment/setup/).

<Info>
  **LangSmith Tracing**
  For local development, if you do not wish to have data traced to LangSmith, set `LANGSMITH_TRACING=false` in your application's `.env` file. With tracing disabled, no data will leave your local server.
</Info>

Next, install the [LangGraph CLI](/langgraph-platform/langgraph-cli):

```
pip install -U "langgraph-cli[inmem]"
```

and run:

```
langgraph dev
```

<Warning>
  **Browser Compatibility**
  Safari blocks `localhost` connections to Studio. To work around this, run the above command with `--tunnel` to access Studio via a secure tunnel.
</Warning>

This will start the LangGraph Server locally, running in-memory. The server will run in watch mode, listening for and automatically restarting on code changes. Read this [reference](/langgraph-platform/cli#dev) to learn about all the options for starting the API server.

If successful, you will see the following logs:

> Ready!
>
> * API: [http://localhost:2024](http://localhost:2024/)
>
> * Docs: [http://localhost:2024/docs](http://localhost:2024/docs)
>
> * LangGraph Studio Web UI: [https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024](https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024)

Once running, you will automatically be directed to LangGraph Studio.

For an already running server, access Studio by either:

1. Directly navigate to the following URL: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`.
2. Within LangSmith, navigate to the LangGraph Platform Deployments tab, click the "LangGraph Studio" button, enter `http://127.0.0.1:2024` and click "Connect".

If running your server at a different host or port, simply update the `baseUrl` to match.

### (Optional) Attach a debugger

For step-by-step debugging with breakpoints and variable inspection:

```bash
# Install debugpy package
pip install debugpy

# Start server with debugging enabled
langgraph dev --debug-port 5678
```

Then attach your preferred debugger:

<Tabs>
  <Tab title="VS Code">
    Add this configuration to `launch.json`:

    ```json
    {
        "name": "Attach to LangGraph",
        "type": "debugpy",
        "request": "attach",
        "connect": {
          "host": "0.0.0.0",
          "port": 5678
        }
    }
    ```
  </Tab>

  <Tab title="PyCharm">
    1. Go to Run → Edit Configurations
    2. Click + and select "Python Debug Server"
    3. Set IDE host name: `localhost`
    4. Set port: `5678` (or the port number you chose in the previous step)
    5. Click "OK" and start debugging
  </Tab>
</Tabs>

## Troubleshooting

For issues getting started, please see this [troubleshooting guide](/langgraph-platform/troubleshooting-studio).

## Next steps

See the following guides for more information on how to use Studio:

* [Run application](/langgraph-platform/invoke-studio)
* [Manage assistants](/langgraph-platform/manage-assistants-studio)
* [Manage threads](/langgraph-platform/threads-studio)
* [Iterate on prompts](/langgraph-platform/iterate-graph-studio)
* [Debug LangSmith traces](/langgraph-platform/clone-traces-studio)
* [Add node to dataset](/langgraph-platform/datasets-studio)