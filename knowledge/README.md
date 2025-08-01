# Knowledge Base

This folder contains documentation and reference materials for the GHL LangGraph Agent project.

## Files

### Core Concepts
- `langgraph_overview.md` - Why developers choose LangGraph and learning path for basics
- `langgraph_platform_overview.md` - Overview of LangGraph Platform features and deployment options
- `langgraph_platform_plans.md` - LangGraph Platform pricing plans (Plus vs Enterprise) and features
- `langgraph_server_overview.md` - LangGraph Server API, assistants, persistence, and deployment info
- `langgraph_data_plane.md` - Data plane architecture, Postgres/Redis usage, autoscaling, and features
- `langgraph_control_plane.md` - Control plane UI, deployment types, database provisioning, and monitoring
- `langgraph_application_structure.md` - Application file structure, configuration, and deployment requirements

### Setup Guides
- `langgraph_setup_requirements.md` - How to set up a LangGraph application with requirements.txt (Python)
- `langgraph_setup_pyproject.md` - How to set up a LangGraph application with pyproject.toml (Python)
- `langgraph_setup_javascript.md` - How to set up a LangGraph.js application (JavaScript/TypeScript)

### Tutorials
- `langgraph_tutorial_basic_chatbot.md` - Build a basic chatbot with StateGraph, nodes, and edges
- `langgraph_tutorial_add_tools.md` - Add tools to your chatbot with bind_tools and conditional edges
- `langgraph_tutorial_add_memory.md` - Add persistent memory with checkpointers and thread_id
- `langgraph_tutorial_human_in_the_loop.md` - Add human-in-the-loop controls with interrupt and Command
- `langgraph_tutorial_customize_state.md` - Add custom fields to state and update state from tools
- `langgraph_tutorial_time_travel.md` - Use time travel to rewind and explore alternative paths

### Deployment
- `langgraph_deploy_cloud.md` - Step-by-step guide to deploy on LangGraph Cloud via LangSmith
- `langgraph_run_locally.md` - Step-by-step guide to run LangGraph applications locally with langgraph dev

### Advanced Topics
- `langgraph_dockerfile_customization.md` - How to customize the Dockerfile for additional dependencies
- `langgraph_rebuild_runtime.md` - How to rebuild graphs at runtime based on configuration
- `langgraph_assistants_overview.md` - Assistants for managing configurations separately from graph logic
- `langgraph_manage_assistants.md` - How to create, configure, and manage assistants
- `langgraph_use_threads.md` - How to create, view, and inspect threads for state persistence
- `langgraph_background_runs.md` - How to kick off background runs for long running jobs
- `langgraph_multiple_agents_thread.md` - How to run multiple agents on the same thread
- `langgraph_cron_jobs.md` - How to use cron jobs to run assistants on a schedule
- `langgraph_stateless_runs.md` - How to create stateless runs without persistent state
- `langgraph_configurable_headers.md` - How to configure headers for runtime configuration
- `langgraph_time_travel_api.md` - How to use time travel functionality via the server API
- `langgraph_mcp_endpoint.md` - Model Context Protocol (MCP) implementation in LangGraph Server
- `langgraph_webhooks.md` - Use webhooks for event-driven communication from LangGraph Platform
- `langgraph_double_texting.md` - Handle concurrent user inputs with reject, enqueue, interrupt, or rollback strategies
- `langgraph_interrupt_concurrent.md` - Detailed guide on using the interrupt strategy for double-texting
- `langgraph_rollback_concurrent.md` - Guide on using the rollback strategy for double-texting
- `langgraph_reject_concurrent.md` - Guide on using the reject strategy for double-texting
- `langgraph_enqueue_concurrent.md` - Guide on using the enqueue strategy for double-texting
- `langgraph_authentication_access_control.md` - Complete guide to authentication and authorization system
- `langgraph_custom_authentication.md` - How to implement custom authentication handlers and enable agent authentication
- `langgraph_setup_custom_auth.md` - Step-by-step tutorial for setting up token-based authentication
- `langgraph_resource_authorization.md` - Tutorial for implementing private conversations with resource-level access control
- `langgraph_connect_auth_provider.md` - Tutorial for integrating OAuth2 with real authentication providers like Supabase
- `langgraph_openapi_auth_documentation.md` - How to document custom authentication schemes in OpenAPI
- `langgraph_scalability_resilience.md` - Platform architecture for horizontal scaling and fault tolerance
- `langgraph_custom_lifespan_events.md` - How to add startup and shutdown handlers for resource initialization
- `langgraph_custom_middleware.md` - How to add custom middleware for logging, headers, and security policies
- `langgraph_custom_routes.md` - How to add custom HTTP endpoints using FastAPI or other ASGI frameworks
- `langgraph_data_storage_privacy.md` - Data storage, privacy policies, and telemetry for CLI, server, and Studio
- `langgraph_ttl_configuration.md` - How to configure time-to-live for checkpoints and cross-thread memories
- `langgraph_semantic_search.md` - How to add semantic search to cross-thread store with embeddings
- `langgraph_integrate_frameworks.md` - How to integrate AutoGen, CrewAI, and other frameworks with LangGraph
- `langgraph_react_integration.md` - Comprehensive guide to integrating LangGraph with React using useStream hook

### Tools & SDK
- `langgraph_cli_overview.md` - LangGraph CLI commands and installation guide
- `langgraph_cli_complete.md` - Complete LangGraph CLI documentation with configuration and all commands
- `langgraph_python_sdk_reference.md` - LangGraph Python SDK reference with client types and usage patterns
- `langgraph_studio_overview.md` - LangGraph Studio IDE features and modes for agent development
- `langgraph_studio_run_application.md` - How to run and submit inputs to applications in LangGraph Studio
- `langgraph_studio_manage_assistants.md` - How to view, edit, and manage assistants in LangGraph Studio
- `langgraph_studio_manage_threads.md` - How to view, create, and edit thread state in LangGraph Studio
- `langgraph_studio_iterate_prompts.md` - How to edit prompts using direct node editing and LangSmith Playground
- `langgraph_studio_debug_traces.md` - How to debug LangSmith traces and clone threads for local testing
- `langgraph_studio_add_node_dataset.md` - How to add node inputs/outputs to LangSmith datasets for evaluation
- `langgraph_studio_troubleshooting.md` - Troubleshooting Safari/Brave connection issues and graph edge problems
- `langgraph_studio_usage.md` - How to use LangGraph Studio for debugging and testing graphs
- `langgraph_streaming_api.md` - Comprehensive guide to streaming outputs from LangGraph API server
- `langgraph_server_api_reference.md` - Server API reference and authentication for LangGraph deployments
- `langgraph_server_changelog.md` - Complete changelog for LangGraph Server releases (v0.2.41 - v0.2.116)
- `langgraph_control_plane_api.md` - Control Plane API reference for programmatically managing deployments
- `langgraph_environment_variables.md` - Complete list of environment variables for configuring LangGraph Server

## Usage

These files contain important documentation that helps understand:
- LangGraph deployment patterns
- Configuration requirements
- Best practices for project structure

Add more documentation files as needed to build up the knowledge base.