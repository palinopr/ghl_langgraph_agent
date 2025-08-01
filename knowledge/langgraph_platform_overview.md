# LangGraph Platform

Develop, deploy, scale, and manage agents with **LangGraph Platform**—the platform for hosting long-running, agentic workflows.

<Tip>
  **Get started with LangGraph Platform**<br />
  Check out the quickstart guides for instructions on how to use LangGraph Platform to run a LangGraph application [locally](local-server) or deploy to [cloud](deployment-quickstart).
</Tip>

## Why use LangGraph Platform?

<div align="center">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/pfAQxBS5z88?si=XGS6Chydn6lhSO1S" title="What is LangGraph Platform?" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen />
</div>

LangGraph Platform makes it easy to get your agent running in production —  whether it's built with LangGraph or another framework — so you can focus on your app logic, not infrastructure. Deploy with one click to get a live endpoint, and use our robust APIs and built-in task queues to handle production scale.

* **[Streaming Support](streaming)**: As agents grow more sophisticated, they often benefit from streaming both token outputs and intermediate states back to the user. Without this, users are left waiting for potentially long operations with no feedback. LangGraph Server provides multiple streaming modes optimized for various application needs.
* **[Background Runs](background-run)**: For agents that take longer to process (e.g., hours), maintaining an open connection can be impractical. The LangGraph Server supports launching agent runs in the background and provides both polling endpoints and webhooks to monitor run status effectively.
* **Support for long runs**: Regular server setups often encounter timeouts or disruptions when handling requests that take a long time to complete. LangGraph Server's API provides robust support for these tasks by sending regular heartbeat signals, preventing unexpected connection closures during prolonged processes.
* **Handling Burstiness**: Certain applications, especially those with real-time user interaction, may experience "bursty" request loads where numerous requests hit the server simultaneously. LangGraph Server includes a task queue, ensuring requests are handled consistently without loss, even under heavy loads.
* **[Double-texting](interrupt-concurrent)**: In user-driven applications, it's common for users to send multiple messages rapidly. This "double texting" can disrupt agent flows if not handled properly. LangGraph Server offers built-in strategies to address and manage such interactions.
* **[Checkpointers and memory management](persistence#checkpoints)**: For agents needing persistence (e.g., conversation memory), deploying a robust storage solution can be complex. LangGraph Platform includes optimized [checkpointers](persistence#checkpoints) and a [memory store](persistence#memory-store), managing state across sessions without the need for custom solutions.
* **[Human-in-the-loop support](add-human-in-the-loop)**: In many applications, users require a way to intervene in agent processes. LangGraph Server provides specialized endpoints for human-in-the-loop scenarios, simplifying the integration of manual oversight into agent workflows.
* **[LangGraph Studio](langgraph-studio)**: Enables visualization, interaction, and debugging of agentic systems that implement the LangGraph Server API protocol. Studio also integrates with LangSmith to enable tracing, evaluation, and prompt engineering.
* **[Deployment](deployment-options)**: There are four ways to deploy on LangGraph Platform: [Cloud SaaS](cloud), [Self-Hosted Data Plane](self-hosted-data-plane), [Self-Hosted Control Plane](self-hosted-control-plane), and [Standalone Container](standalone-container).