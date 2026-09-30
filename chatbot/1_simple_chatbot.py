from pathlib import Path

import chainlit as cl
import dotenv

dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


@cl.on_message
async def on_message(message: cl.Message):
    await cl.Message(content=f"Received: {message.content}").send()
