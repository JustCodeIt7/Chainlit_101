"""
Episode 3: Your First Chainlit App – Echo Bot to AI Assistant

Learning Objectives:
1. Implement a simple echo chatbot using Chainlit's message handler.
2. Extend the bot to generate AI responses using an LLM (OpenAI's API).
3. Learn how to send messages back to the user through Chainlit's API.

How to run this app:
1. (Optional) Create a virtual environment and install dependencies.
2. Install Chainlit: pip install chainlit
3. Install OpenAI & python-dotenv for LLM support: pip install openai python-dotenv
4. Set your OpenAI API key in an .env file (OPENAI_API_KEY=...) or export it in the shell.
5. Start the app: chainlit run 03-echo_to_ai.py
6. Open your browser to http://localhost:8000

Episode overview:
- We start with an Echo Bot that mirrors the user's message.
- When an API key is available, we upgrade the bot to call OpenAI for AI-generated replies.
- The handler demonstrates how to send Chainlit messages back to the UI.
"""

import os
from typing import Optional

import chainlit as cl

try:
    # Loading environment variables lets us keep credentials out of our codebase.
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency for tutorials
    load_dotenv = None

try:
    import openai
except ImportError:  # pragma: no cover - tutorial code should still run in echo mode
    openai = None


if load_dotenv:
    load_dotenv()  # Loads .env variables if the file exists.

# Prefer environment variables for secrets. Fallback to echo mode if none is set.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


async def call_openai(prompt: str) -> Optional[str]:
    """Request a chat completion from OpenAI and return the assistant reply.

    Returns None when the OpenAI client is unavailable so the app can fall back
    to echo mode without raising runtime errors in the tutorial environment.
    """

    if not (openai and OPENAI_API_KEY):
        return None

    # cl.make_async wraps blocking calls so the Chainlit event loop stays responsive.
    completion = await cl.make_async(openai.ChatCompletion.create)(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    ai_message = completion["choices"][0]["message"]["content"]
    return ai_message.strip()


@cl.on_chat_start
async def on_chat_start():
    """Send guidance to the user depending on whether AI mode is available."""

    if openai and OPENAI_API_KEY:
        intro = (
            "🤖 **AI Assistant mode enabled!**\n\n"
            "Your messages will be routed to OpenAI's GPT model for a helpful reply."
        )
    else:
        intro = (
            "🪞 **Echo Bot mode active.**\n\n"
            "Install `openai` and set `OPENAI_API_KEY` to unlock AI responses."
        )

    await cl.Message(content=intro).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Main message handler that powers both the Echo Bot and AI Assistant."""

    user_input = message.content.strip()

    ai_response = await call_openai(user_input)

    if ai_response:
        await cl.Message(content=ai_response).send()
        return

    echo_message = f"Echo Bot: {user_input or 'Please type something!'}"
    await cl.Message(content=echo_message).send()


@cl.on_chat_end
async def on_chat_end():
    """Log chat termination for visibility while developing the tutorial."""

    print("Chat session ended – thanks for testing the Echo/AI bot!")


if __name__ == "__main__":
    print("This is a Chainlit app. Use 'chainlit run 03-echo_to_ai.py' to launch it.")
