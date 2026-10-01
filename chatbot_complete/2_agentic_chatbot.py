from pathlib import Path

import chainlit as cl
import dotenv
from openai.types.responses import ResponseTextDeltaEvent

from agents import Runner
from nutrition_agent import nutrition_agent

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


@cl.on_message
async def on_message(message: cl.Message):

    result = Runner.run_streamed(
        nutrition_agent,
        message.content,
    )

    msg = cl.Message(content="")
    async for event in result.stream_events():
        # Stream final message text to screen
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            await msg.stream_token(token=event.data.delta)
            print(event.data.delta, end="", flush=True)

        elif (
            event.type == "raw_response_event"
            and hasattr(event.data, "item")
            and hasattr(event.data.item, "type")
            and event.data.item.type == "function_call"
            and len(event.data.item.arguments) > 0
        ):
            tool_name = "thinking..."
            with cl.Step(name=tool_name, type="tool") as step:
                step.input = event.data.item.arguments
                print(f"\nTool call: {tool_name} with args: {event.data.item.arguments}")
            

    await msg.update()
