# a2a_basic

This project provides a basic example of the A2A SDK. It contains a single agent and a client that invokes it.
This the fundamental concepts of creating and interacting with an A2A agent.

## Agent Server

The agent server is a simple HTTP server that listens for requests and responds with a greeting message.

- `__main__.py`: The entry point for the agent server. It configures and runs the server.
- `agent_executor.py`: Defines the `GreetingAgent` and its executor (`GreetingAgentExecutor`) for the A2A framework.

### Running the Agent Server

```pwsh
uv run a2a_basic .
```

## Client

The client is a simple script that sends a request to the agent server and prints the response.

- `client.py`: The entry point for the client. It sends a request to the agent server and prints the response.

### Running the Client

```pwsh
uv run client.py
```
