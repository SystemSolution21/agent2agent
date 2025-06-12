"""
Main entry point for the A2A Greeting Agent server.
This script configures and launches the agent server.
"""

import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from agent_executor import GreetingAgentExecutor


def main() -> None:
    """
    Configures and runs the A2A Greeting Agent server.

    This function defines the agent's skills and metadata (AgentCard),
    sets up the request handler with the GreetingAgentExecutor,
    initializes the A2AStarletteApplication, and starts the Uvicorn server.
    """

    # Agent skill
    skill = AgentSkill(
        id="greet",
        name="Greet",
        description="Returns a greeting.",
        tags=["greeting", "hello", "world"],
        examples=["hello", "hi", "hey"],
    )

    # Agent card
    agent_card = AgentCard(
        name="Greeting Agent",
        description="A simple agent that returns a greeting.",
        url="http://localhost:9999/",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        skills=[skill],
        version="0.0.1",
        capabilities=AgentCapabilities(),
    )

    # Request handler
    request_handler = DefaultRequestHandler(
        agent_executor=GreetingAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # Server app
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    # Run server
    uvicorn.run(app=server.build(), host="0.0.0.0", port=9999)


if __name__ == "__main__":
    main()
