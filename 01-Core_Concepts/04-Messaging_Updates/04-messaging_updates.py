"""
Episode 4: Chainlit Messaging – Sending and Updating Responses

Learning Objectives:
1. Send multiple messages or notifications for a single user query.
2. Update an existing message to show progress or refined results.
3. Use Markdown formatting in Chainlit responses for richer output.

How to run this app:
1. Install Chainlit if needed: pip install chainlit
2. Start the app: chainlit run 04-messaging_updates.py
3. Open your browser to http://localhost:8000

Episode overview:
- Demonstrates sending an immediate acknowledgement and additional messages.
- Shows how to update a previously sent message using Chainlit's API.
- Highlights Markdown rendering with formatted lists and code blocks.
"""

import asyncio

import chainlit as cl


@cl.on_chat_start
async def intro_message():
    intro = (
        "**Welcome to Episode 4!**\n\n"
        "Type any message to see how we can acknowledge you immediately, "
        "stream updates, and finish with a polished Markdown response."
    )
    await cl.Message(content=intro).send()


@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip() or "(no input provided)"

    status_message = cl.Message(content="⌛️ Processing your request...")
    await status_message.send()

    await cl.Message(author="system", content="System: Listening for updates...").send()

    await asyncio.sleep(1.0)
    await status_message.update(content="✍️ Drafting a helpful response...")

    await asyncio.sleep(1.0)
    await cl.Message(content="💡 Tip: You can send multiple messages while you work!").send()

    final_content = (
        "**All set!** Here's how Chainlit handled your request:\n\n"
        f"- **User prompt:** `{user_input}`\n"
        "- **What happened:**\n"
        "  1. Immediate acknowledgement\n"
        "  2. Progress update\n"
        "  3. Final Markdown-rich message\n\n"
        "```python\n"
        "async def handle_message(message):\n"
        "    status = await cl.Message(content='Working...').send()\n"
        "    await status.update(content='Done!')\n"
        "```\n"
    )

    await status_message.update(content=final_content)


@cl.on_chat_end
async def on_chat_end():
    print("Episode 4 example chat ended.")


if __name__ == "__main__":
    print("Use 'chainlit run 04-messaging_updates.py' to launch this example.")
