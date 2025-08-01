# LangGraph Server changelog

[LangGraph Server](/langgraph-platform/langgraph-server) is an API platform for creating and managing agent-based applications. It provides built-in persistence, a task queue, and supports deploying, configuring, and running assistants (agentic workflows) at scale. This changelog documents all notable updates, features, and fixes to LangGraph Server releases.

<a id="2025-07-31" />

## v0.2.116

* Reduced the default number of history checkpoints from 10 to 1 to optimize performance.

<a id="2025-07-31" />

## v0.2.115

* Optimized cache re-use to enhance application performance and efficiency.

<a id="2025-07-30" />

## v0.2.113

* Improved thread search pagination by updating response headers with `X-Pagination-Total` and `X-Pagination-Next` for better navigation.

<a id="2025-07-30" />

## v0.2.112

* Ensured sync logging methods are awaited and added a linter to prevent future occurrences.
* Fixed an issue where JavaScript tasks were not being populated correctly for JS graphs.

<a id="2025-07-29" />

## v0.2.111

* Fixed JS graph streaming failure by starting the heartbeat as soon as the connection opens.

<a id="2025-07-29" />

## v0.2.110

* Added interrupts as default values for join operations while preserving stream behavior.

<a id="2025-07-28" />

## v0.2.109

* Fixed an issue where config schema was missing when `config_type` was not set, ensuring more reliable configurations.

<a id="2025-07-28" />

## v0.2.108

* Prepared for Langgraph v0.6 compatibility with new context API support and bug fixes.

<a id="2025-07-27" />

## v0.2.107

* Implemented caching for authentication processes to enhance performance and efficiency.
* Optimized database performance by merging count and select queries.

<a id="2025-07-27" />

## v0.2.106

* Made log streams resumable, enhancing reliability and improving user experience when reconnecting.

<a id="2025-07-27" />

## v0.2.105

* Added a heapdump endpoint to save memory heap information to a file.

<a id="2025-07-25" />

## v0.2.103

* Used the correct metadata endpoint to resolve issues with data retrieval.

<a id="2025-07-24" />

## v0.2.102

* Captured interrupt events in the wait method to preserve previous behavior from langgraph 0.5.0.
* Added support for SDK structlog in the JavaScript environment for enhanced logging capabilities.

<a id="2025-07-24" />

## v0.2.101

* Corrected the metadata endpoint for self-hosted deployments.

<a id="2025-07-22" />

## v0.2.99

* Improved license check by adding an in-memory cache and handling Redis connection errors more effectively.
* Reloaded assistants to preserve manually created ones while discarding those removed from the configuration file.
* Reverted changes to ensure the UI namespace for gen UI is a valid JavaScript property name.
* Ensured that the UI namespace for generated UI is a valid JavaScript property name, improving API compliance.
* Enhanced error handling to return a 422 status code for unprocessable entity requests.

<a id="2025-07-19" />

## v0.2.98

* Added context to langgraph nodes to improve log filtering and trace visibility.

<a id="2025-07-19" />

## v0.2.97

* Improved interoperability with the ckpt ingestion worker on the main loop to prevent task scheduling issues.
* Delayed queue worker startup until after migrations are completed to prevent premature execution.
* Enhanced thread state error handling by adding specific metadata and improved response codes for better clarity when state updates fail during creation.
* Exposed the interrupt ID when retrieving the thread state to improve API transparency.

<a id="2025-07-17" />

## v0.2.96

* Added a fallback mechanism for configurable header patterns to handle exclude/include settings more effectively.

<a id="2025-07-17" />

## v0.2.95

* Avoided setting the future if it is already done to prevent redundant operations.
* Resolved compatibility errors in CI by switching from `typing.TypedDict` to `typing_extensions.TypedDict` for Python versions below 3.12.

<a id="2025-07-16" />

## v0.2.94

* Improved performance by omitting pending sends for langgraph versions 0.5 and above.
* Improved server startup logs to provide clearer warnings when the DD_API_KEY environment variable is set.

<a id="2025-07-16" />

## v0.2.93

* Removed the GIN index for run metadata to improve performance.

<a id="2025-07-16" />

## v0.2.92

* Enabled copying functionality for blobs and checkpoints, improving data management flexibility.

<a id="2025-07-16" />

## v0.2.91

* Reduced writes to the `checkpoint_blobs` table by inlining small values (null, numeric, str, etc.). This means we don't need to store extra values for channels that haven't been updated.

<a id="2025-07-16" />

## v0.2.90

* Improve checkpoint writes via node-local background queueing.

<a id="2025-07-15" />

## v0.2.89

* Decoupled checkpoint writing from thread/run state by removing foreign keys and updated logger to prevent timeout-related failures.

<a id="2025-07-14" />

## v0.2.88

* Removed the foreign key constraint for `thread` in the `run` table to simplify database schema.

<a id="2025-07-14" />

## v0.2.87

* Added more detailed logs for Redis worker signaling to improve debugging.

<a id="2025-07-11" />

## v0.2.86

* Honored tool descriptions in the `/mcp` endpoint to align with expected functionality.

<a id="2025-07-10" />

## v0.2.85

* Added support for the `on_disconnect` field to `runs/wait` and included disconnect logs for better debugging.

<a id="2025-07-09" />

## v0.2.84

* Removed unnecessary status updates to streamline thread handling and updated version to 0.2.84.

<a id="2025-07-09" />

## v0.2.83

* Reduced the default time-to-live for resumable streams to 2 minutes.
* Enhanced data submission logic to send data to both Beacon and LangSmith instance based on license configuration.
* Enabled submission of self-hosted data to a Langsmith instance when the endpoint is configured.

<a id="2025-07-03" />

## v0.2.82

* Addressed a race condition in background runs by implementing a lock using join, ensuring reliable execution across CTEs.

<a id="2025-07-03" />

## v0.2.81

* Optimized run streams by reducing initial wait time to improve responsiveness for older or non-existent runs.

<a id="2025-07-03" />

## v0.2.80

* Corrected parameter passing in the `logger.ainfo()` API call to resolve a TypeError.

<a id="2025-07-02" />

## v0.2.79

* Fixed a JsonDecodeError in checkpointing with remote graph by correcting JSON serialization to handle trailing slashes properly.
* Introduced a configuration flag to disable webhooks globally across all routes.

<a id="2025-07-02" />

## v0.2.78

* Added timeout retries to webhook calls to improve reliability.
* Added HTTP request metrics, including a request count and latency histogram, for enhanced monitoring capabilities.

<a id="2025-07-02" />

## v0.2.77

* Added HTTP metrics to improve performance monitoring.
* Changed the Redis cache delimiter to reduce conflicts with subgraph message names and updated caching behavior.

<a id="2025-07-01" />

## v0.2.76

* Updated Redis cache delimiter to prevent conflicts with subgraph messages.

<a id="2025-06-30" />

## v0.2.74

* Scheduled webhooks in an isolated loop to ensure thread-safe operations and prevent errors with PYTHONASYNCIODEBUG=1.

<a id="2025-06-27" />

## v0.2.73

* Fixed an infinite frame loop issue and removed the dict_parser due to structlog's unexpected behavior.
* Throw a 409 error on deadlock occurrence during run cancellations to handle lock conflicts gracefully.

<a id="2025-06-27" />

## v0.2.72

* Ensured compatibility with future langgraph versions.
* Implemented a 409 response status to handle deadlock issues during cancellation.

<a id="2025-06-26" />

## v0.2.71

* Improved logging for better clarity and detail regarding log types.

<a id="2025-06-26" />

## v0.2.70

* Improved error handling to better distinguish and log TimeoutErrors caused by users from internal run timeouts.

<a id="2025-06-26" />

## v0.2.69

* Added sorting and pagination to the crons API and updated schema definitions for improved accuracy.

<a id="2025-06-26" />

## v0.2.66

* Fixed a 404 error when creating multiple runs with the same thread_id using `on_not_exist="create"`.

<a id="2025-06-25" />

## v0.2.65

* Ensured that only fields from `assistant_versions` are returned when necessary.
* Ensured consistent data types for in-memory and PostgreSQL users, improving internal authentication handling.

<a id="2025-06-24" />

## v0.2.64

* Added descriptions to version entries for better clarity.

<a id="2025-06-23" />

## v0.2.62

* Improved user handling for custom authentication in the JS Studio.
* Added Prometheus-format run statistics to the metrics endpoint for better monitoring.
* Added run statistics in Prometheus format to the metrics endpoint.

<a id="2025-06-20" />

## v0.2.61

* Set a maximum idle time for Redis connections to prevent unnecessary open connections.

<a id="2025-06-20" />

## v0.2.60

* Enhanced error logging to include traceback details for dictionary operations.
* Added a `/metrics` endpoint to expose queue worker metrics for monitoring.

<a id="2025-06-18" />

## v0.2.57

* Removed CancelledError from retriable exceptions to allow local interrupts while maintaining retriability for workers.
* Introduced middleware to gracefully shut down the server after completing in-flight requests upon receiving a SIGINT.
* Reduced metadata stored in checkpoint to only include necessary information.
* Improved error handling in join runs to return error details when present.

<a id="2025-06-17" />

## v0.2.56

* Improved application stability by adding a handler for SIGTERM signals.

<a id="2025-06-17" />

## v0.2.55

* Improved the handling of cancellations in the queue entrypoint.
* Improved cancellation handling in the queue entry point.

<a id="2025-06-16" />

## v0.2.54

* Enhanced error message for LuaLock timeout during license validation.
* Fixed the $contains filter in custom auth by requiring an explicit ::text cast and updated tests accordingly.
* Ensured project and tenant IDs are formatted as UUIDs for consistency.

<a id="2025-06-13" />

## v0.2.53

* Resolved a timing issue to ensure the queue starts only after the graph is registered.
* Improved performance by setting thread and run status in a single query and enhanced error handling during checkpoint writes.
* Reduced the default background grace period to 3 minutes.

<a id="2025-06-12" />

## v0.2.52

* Now logging expected graphs when one is omitted to improve traceability.
* Implemented a time-to-live (TTL) feature for resumable streams.
* Improved query efficiency and consistency by adding a unique index and optimizing row locking.

<a id="2025-06-12" />

## v0.2.51

* Handled `CancelledError` by marking tasks as ready to retry, improving error management in worker processes.
* Added LG API version and request ID to metadata and logs for better tracking.
* Added LG API version and request ID to metadata and logs to improve traceability.
* Improved database performance by creating indexes concurrently.
* Ensured postgres write is committed only after the Redis running marker is set to prevent race conditions.
* Enhanced query efficiency and reliability by adding a unique index on thread_id/running, optimizing row locks, and ensuring deterministic run selection.
* Resolved a race condition by ensuring Postgres updates only occur after the Redis running marker is set.

<a id="2025-06-07" />

## v0.2.46

* Introduced a new connection for each operation while preserving transaction characteristics in Threads state `update()` and `bulk()` commands.

<a id="2025-06-05" />

## v0.2.45

* Enhanced streaming feature by incorporating tracing contexts.
* Removed an unnecessary query from the Crons.search function.
* Resolved connection reuse issue when scheduling next run for multiple cron jobs.
* Removed an unnecessary query in the Crons.search function to improve efficiency.
* Resolved an issue with scheduling the next cron run by improving connection reuse.

<a id="2025-06-04" />

## v0.2.44

* Enhanced the worker logic to exit the pipeline before continuing when the Redis message limit is reached.
* Introduced a ceiling for Redis message size with an option to skip messages larger than 128 MB for improved performance.
* Ensured the pipeline always closes properly to prevent resource leaks.

<a id="2025-06-04" />

## v0.2.43

* Improved performance by omitting logs in metadata calls and ensuring output schema compliance in value streaming.
* Ensured the connection is properly closed after use.
* Aligned output format to strictly adhere to the specified schema.
* Stopped sending internal logs in metadata requests to improve privacy.

<a id="2025-06-04" />

## v0.2.42

* Added timestamps to track the start and end of a request's run.
* Added tracer information to the configuration settings.
* Added support for streaming with tracing contexts.

<a id="2025-06-03" />

## v0.2.41

* Added locking mechanism to prevent errors in pipelined executions.