import httpx
import json
import uuid
from typing import Any, Dict, List, Optional

from a2a.client import A2AClient, A2ACardResolver
from a2a.types import (
    AgentCard,
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    SendMessageResponse,
    TextPart,
)


# Extract nested values from a dictionary
def get_nested_value(data: Dict[str, Any], path: str) -> Optional[Any]:
    """Safely get a nested value from a dictionary using a dot-separated path.

    Handles both dictionary keys and list indices in the path.
    Example: "result.parts.0.text" will access data["result"]["parts"][0]["text"]
    """
    keys: List[str] = path.split(sep=".")
    current: Any = data

    for key in keys:
        # Convert to integer for list indexing
        try:
            if key.isdigit():
                key = int(key)
        except (ValueError, TypeError):
            pass

        if isinstance(current, dict) and key in current:
            current = current[key]
        elif (
            isinstance(current, list)
            and isinstance(key, int)
            and 0 <= key < len(current)
        ):
            current = current[key]
        else:
            return None

    return current


# Set public agent card path and base URL
PUBLIC_AGENT_CARD_PATH: str = "/.well-known/agent.json"
BASE_URL: str = "http://localhost:9999"


# Main entry point
async def main() -> None:
    async with httpx.AsyncClient() as httpx_client:

        # Instantiate agent card resolver
        agent_card_resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL,
            agent_card_path=PUBLIC_AGENT_CARD_PATH,
        )
        # Instantiate agent card
        public_agent_card: AgentCard | None = None

        try:
            # Resolve agent card
            print(f"Resolving agent card from {BASE_URL}{PUBLIC_AGENT_CARD_PATH}...")
            public_agent_card = await agent_card_resolver.get_agent_card()
            print(
                f"Successfully resolved agent card:\n{public_agent_card.model_dump_json(indent=2)}"
            )

        except Exception as e:
            print(f"Error resolving agent card: {e}")
            raise RuntimeError("Failed to resolved public agent card")

        # Instantiate A2A client
        a2a_client = A2AClient(
            httpx_client=httpx_client,
            agent_card=public_agent_card,
        )
        print(f"Successfully instantiated A2A client: {a2a_client}")

        # Send message to A2A server
        message_payload = Message(
            messageId=str(object=uuid.uuid4()),
            parts=[
                Part(
                    root=TextPart(
                        text="Hello, how are you?",
                    ),
                ),
            ],
            role=Role.user,
        )
        request = SendMessageRequest(
            id=str(object=uuid.uuid4()),
            params=MessageSendParams(
                message=message_payload,
            ),
        )
        print(f"Sending message to A2A server: {request}")

        try:
            response: SendMessageResponse = await a2a_client.send_message(
                request=request
            )
            print(
                f"Received response from A2A server:\n{response.model_dump_json(indent=2)}"
            )

            # Convert to dictionary
            response_dict: Dict[str, Any] = json.loads(
                s=response.model_dump_json(indent=2)
            )

            # Extract text
            text: Any | None = get_nested_value(
                data=response_dict, path="result.parts.0.text"  # expected TextPart
            )
            if text:
                print(f"Agent message: {text}")
            else:
                print("No text found in response")

        except Exception as e:
            print(f"Error sending message to A2A server:\n{e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main=main())
