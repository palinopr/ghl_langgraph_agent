# Use cron jobs

There are many situations in which it is useful to run an assistant on a schedule.

For example, say that you're building an assistant that runs daily and sends an email summary
of the day's news. You could use a cron job to run the assistant every day at 8:00 PM.

LangGraph Platform supports cron jobs, which run on a user-defined schedule. The user specifies a schedule, an assistant, and some input. After that, on the specified schedule, the server will:

* Create a new thread with the specified assistant
* Send the specified input to that thread

Note that this sends the same input to the thread every time.

The LangGraph Platform API provides several endpoints for creating and managing cron jobs. See the [API reference](https://langchain-ai.github.io/langgraph/cloud/reference/api/api_ref/) for more details.

Sometimes you don't want to run your graph based on user interaction, but rather you would like to schedule your graph to run on a schedule - for example if you wish for your graph to compose and send out a weekly email of to-dos for your team. LangGraph Platform allows you to do this without having to write your own script by using the `Crons` client. To schedule a graph job, you need to pass a [cron expression](https://crontab.cronhub.io/) to inform the client when you want to run the graph. `Cron` jobs are run in the background and do not interfere with normal invocations of the graph.

## Setup

First, let's set up our SDK client, assistant, and thread:

<Tabs>
  <Tab title="Python">
    ```python
    from langgraph_sdk import get_client

    client = get_client(url=<DEPLOYMENT_URL>)
    # Using the graph deployed with the name "agent"
    assistant_id = "agent"
    # create thread
    thread = await client.threads.create()
    print(thread)
    ```
  </Tab>

  <Tab title="Javascript">
    ```js
    import { Client } from "@langchain/langgraph-sdk";

    const client = new Client({ apiUrl: <DEPLOYMENT_URL> });
    // Using the graph deployed with the name "agent"
    const assistantId = "agent";
    // create thread
    const thread = await client.threads.create();
    console.log(thread);
    ```
  </Tab>

  <Tab title="CURL">
    ```bash
    curl --request POST \
        --url <DEPLOYMENT_URL>/assistants/search \
        --header 'Content-Type: application/json' \
        --data '{
            "limit": 10,
            "offset": 0
        }' | jq -c 'map(select(.config == null or .config == {})) | .[0].graph_id' && \
    curl --request POST \
        --url <DEPLOYMENT_URL>/threads \
        --header 'Content-Type: application/json' \
        --data '{}'
    ```
  </Tab>
</Tabs>

Output:

```
{
'thread_id': '9dde5490-2b67-47c8-aa14-4bfec88af217',
'created_at': '2024-08-30T23:07:38.242730+00:00',
'updated_at': '2024-08-30T23:07:38.242730+00:00',
'metadata': {},
'status': 'idle',
'config': {},
'values': None
}
```

## Cron job on a thread

To create a cron job associated with a specific thread, you can write:

<Tabs>
  <Tab title="Python">
    ```python
    # This schedules a job to run at 15:27 (3:27PM) every day
    cron_job = await client.crons.create_for_thread(
        thread["thread_id"],
        assistant_id,
        schedule="27 15 * * *",
        input={"messages": [{"role": "user", "content": "What time is it?"}]},
    )
    ```
  </Tab>

  <Tab title="Javascript">
    ```js
    // This schedules a job to run at 15:27 (3:27PM) every day
    const cronJob = await client.crons.create_for_thread(
      thread["thread_id"],
      assistantId,
      {
        schedule: "27 15 * * *",
        input: { messages: [{ role: "user", content: "What time is it?" }] }
      }
    );
    ```
  </Tab>

  <Tab title="CURL">
    ```bash
    curl --request POST \
        --url <DEPLOYMENT_URL>/threads/<THREAD_ID>/runs/crons \
        --header 'Content-Type: application/json' \
        --data '{
            "assistant_id": <ASSISTANT_ID>,
        }'
    ```
  </Tab>
</Tabs>

Note that it is **very** important to delete `Cron` jobs that are no longer useful. Otherwise you could rack up unwanted API charges to the LLM! You can delete a `Cron` job using the following code:

<Tabs>
  <Tab title="Python">
    ```python
    await client.crons.delete(cron_job["cron_id"])
    ```
  </Tab>

  <Tab title="Javascript">
    ```js
    await client.crons.delete(cronJob["cron_id"]);
    ```
  </Tab>

  <Tab title="CURL">
    ```bash
    curl --request DELETE \
        --url <DEPLOYMENT_URL>/runs/crons/<CRON_ID>
    ```
  </Tab>
</Tabs>

## Cron job stateless

You can also create stateless cron jobs by using the following code:

<Tabs>
  <Tab title="Python">
    ```python
    # This schedules a job to run at 15:27 (3:27PM) every day
    cron_job_stateless = await client.crons.create(
        assistant_id,
        schedule="27 15 * * *",
        input={"messages": [{"role": "user", "content": "What time is it?"}]},
    )
    ```
  </Tab>

  <Tab title="Javascript">
    ```js
    // This schedules a job to run at 15:27 (3:27PM) every day
    const cronJobStateless = await client.crons.create(
      assistantId,
      {
        schedule: "27 15 * * *",
        input: { messages: [{ role: "user", content: "What time is it?" }] }
      }
    );
    ```
  </Tab>

  <Tab title="CURL">
    ```bash
    curl --request POST \
        --url <DEPLOYMENT_URL>/runs/crons \
        --header 'Content-Type: application/json' \
        --data '{
            "assistant_id": <ASSISTANT_ID>,
        }'
    ```
  </Tab>
</Tabs>

Again, remember to delete your job once you are done with it!

<Tabs>
  <Tab title="Python">
    ```python
    await client.crons.delete(cron_job_stateless["cron_id"])
    ```
  </Tab>

  <Tab title="Javascript">
    ```js
    await client.crons.delete(cronJobStateless["cron_id"]);
    ```
  </Tab>

  <Tab title="CURL">
    ```bash
    curl --request DELETE \
        --url <DEPLOYMENT_URL>/runs/crons/<CRON_ID>
    ```
  </Tab>
</Tabs>