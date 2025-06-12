"""
Defines the GreetingAgent and its executor for the A2A framework.

This module contains:
- GreetingAgent: A simple agent that produces a greeting message.
- GreetingAgentExecutor: Manages the execution lifecycle of the GreetingAgent
  within the A2A server environment.
"""

from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.utils import new_agent_text_message

from pydantic import BaseModel


class GreetingAgent(BaseModel):
    """
    A simple agent that returns a predefined greeting string.

    This agent demonstrates the basic structure of an agent's core logic.
    It inherits from pydantic.BaseModel for potential future configuration
    or state management, though it's not strictly necessary for this simple case.
    """

    async def invoke(self) -> str:
        """
        Generates and returns a greeting message.

        This is the primary action method of the agent.

        Returns:
            str: A fixed greeting message.
        """
        return "Hello World! This is a greeting from the A2A GreetingAgent."


class GreetingAgentExecutor(AgentExecutor):
    """
    An executor responsible for managing the GreetingAgent's lifecycle and interaction
    with the A2A framework.

    It handles the execution of the agent's `invoke` method and sends the
    result back through the event queue.
    """

    def __init__(self) -> None:
        """
        Initializes the GreetingAgentExecutor.

        Creates an instance of the GreetingAgent that this executor will manage.
        """
        super().__init__()  # It's good practice to call super().__init__()
        self.agent = GreetingAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Executes the GreetingAgent's primary task.

        This method is called by the A2A framework when the agent needs to perform
        its action. It invokes the agent, gets the result, and enqueues it as
        a text message event.

        Args:
            context: The request context, providing information about the
                     incoming request. Not directly used by this simple agent.
            event_queue: The event queue used to send events (like the agent's
                         response) back to the A2A framework.
        """
        result: str = await self.agent.invoke()
        await event_queue.enqueue_event(event=new_agent_text_message(text=result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Handles a request to cancel the agent's execution.

        For this simple agent, cancellation is not implemented and will raise
        an exception. In more complex, long-running agents, this method
        should implement graceful cancellation logic.

        Args:
            context: The request context.
            event_queue: The event queue.

        Raises:
            Exception: Indicating that cancellation is not implemented.
        """
        # For a real agent,  might be appropriate to send a cancellation confirmation event:
        # await event_queue.enqueue_event(event=new_agent_text_message(text="GreetingAgent execution cancelled."))
        # And then perform actual cleanup or stop ongoing tasks.
        raise Exception("Cancel not implemented for GreetingAgent")
