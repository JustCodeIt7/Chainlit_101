"""
Episode 1: Getting Started with Chainlit  Installation & Hello World

Learning Objectives:
1. Understand what Chainlit is and its key features for conversational AI
2. Set up the development environment and install the Chainlit package
3. Run a "Hello World" Chainlit app to verify installation and see the default UI

To run this app:
1. Install Chainlit: pip install chainlit
2. Run the app: chainlit run hello_world.py
3. Open your browser to http://localhost:8000

What is Chainlit?
- Open-source Python framework for building conversational AI applications
- Provides a ready-to-use chat interface
- Easy integration with LLMs and AI models
- Built-in support for file uploads, streaming, and user sessions
"""

import chainlit as cl


@cl.on_message
async def main(message: cl.Message):
    """
    This function is called every time a user sends a message.
    It's the core of our conversational app.
    """
    # Get the content of the user's message
    user_input = message.content

    # Create a simple response
    response = f"Hello! You said: '{user_input}'"

    # Send the response back to the user
    await cl.Message(content=response).send()


@cl.on_chat_start
async def start():
    """
    This function is called when a new chat session starts.
    Perfect for sending welcome messages.
    """
    welcome_message = """
    <‰ **Welcome to your first Chainlit app!**

    This is a simple "Hello World" example that echoes back whatever you type.

    **What you can try:**
    - Type any message and see it echoed back
    - Notice how the chat interface is automatically created
    - Observe the clean, modern UI that Chainlit provides out of the box

    **Next steps:**
    - Try typing different messages
    - Notice how each message gets its own bubble
    - See how the chat history is maintained

    Go ahead, type something! =G
    """

    await cl.Message(content=welcome_message).send()


# Additional demonstration of Chainlit features
@cl.on_chat_end
async def end():
    """
    This function is called when the chat session ends.
    Useful for cleanup or farewell messages.
    """
    print("Chat session ended - this appears in the terminal/logs")


# You can also add startup actions (this runs when the server starts)
@cl.on_settings_update
async def setup_agent(settings):
    """
    This function is called when settings are updated.
    Advanced feature - not needed for basic apps.
    """
    print("Settings updated:", settings)


if __name__ == "__main__":
    # This block won't run when using 'chainlit run'
    # But it shows how you might test parts of your code
    print("This is a Chainlit app!")
    print("To run it, use: chainlit run hello_world.py")
    print("Then open http://localhost:8000 in your browser")