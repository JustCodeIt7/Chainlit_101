"""
Episode 2B: Chainlit Events Overview – The Lifecycle

Learning Objectives:
1. Learn what **events** are and why Chainlit apps revolve around them
2. Explore the common decorators: @cl.on_chat_start, @cl.on_message, and @cl.on_stop
3. Run a simple logging example to see lifecycle events firing

Events are the building blocks of Chainlit applications:
- They respond to user actions (starting chat, sending messages, etc.)
- Each event has a specific decorator and purpose
- Understanding the lifecycle helps you build better apps

Common Event Decorators:
- @cl.on_chat_start - When a new chat session begins
- @cl.on_message - When user sends a message
- @cl.on_stop - When user cancels streaming/stops operation
- @cl.on_chat_end - When chat session ends
- @cl.on_settings_update - When user updates settings
"""

import chainlit as cl
import asyncio
from datetime import datetime


def log_event(event_name: str, details: str = ""):
    """Helper function to log events with timestamps"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] 🔥 EVENT: {event_name} {details}")


@cl.on_chat_start
async def on_chat_start():
    """
    🚀 LIFECYCLE EVENT #1: Chat Start
    This fires when a new user opens the chat interface
    Perfect for: welcome messages, initializing session data, setup
    """
    log_event("on_chat_start", "- New chat session initiated")

    # Initialize session data (we'll explore this more in Episode 2C)
    cl.user_session.set("message_count", 0)
    cl.user_session.set("start_time", datetime.now().isoformat())

    welcome_msg = """
    # 🔄 Chainlit Events Lifecycle Demo

    **Welcome!** You just triggered the `@cl.on_chat_start` event.

    ## Available Events to Test:

    🟢 **on_chat_start** ← Just fired!
    🔵 **on_message** ← Fires when you type
    🟡 **on_stop** ← Type 'stream' to test
    🔴 **on_chat_end** ← Fires when you close/refresh

    **Try typing anything to trigger `on_message`!**

    *Check your terminal/console to see the event logs* 📋
    """

    await cl.Message(content=welcome_msg).send()


@cl.on_message
async def on_message(message: cl.Message):
    """
    💬 LIFECYCLE EVENT #2: Message Received
    This fires every time the user sends a message
    Perfect for: processing input, generating responses, routing logic
    """
    log_event("on_message", f"- Received: '{message.content[:30]}...'")

    # Update session data
    count = cl.user_session.get("message_count", 0)
    cl.user_session.set("message_count", count + 1)

    user_input = message.content.lower().strip()

    # Demonstrate different responses based on input
    if user_input == "stream":
        await demonstrate_streaming(message)
    elif user_input == "events":
        await show_event_details()
    elif user_input == "count":
        msg_count = cl.user_session.get("message_count", 0)
        start_time = cl.user_session.get("start_time", "Unknown")
        await cl.Message(
            content=f"📊 **Session Stats:**\n- Messages sent: {msg_count}\n- Started at: {start_time}"
        ).send()
    else:
        # Standard echo response
        await cl.Message(
            content=f"""
            ✅ **on_message event fired!**

            You sent: "{message.content}"

            **Try these commands:**
            - `stream` - Test the on_stop event
            - `events` - Learn about all events
            - `count` - See your session stats

            *Message #{cl.user_session.get("message_count", 0)}*
            """
        ).send()


async def demonstrate_streaming(original_message: cl.Message):
    """
    Demo function to show streaming and the on_stop event
    """
    log_event("demonstrate_streaming", "- Starting streaming demo")

    msg = cl.Message(content="")
    await msg.send()

    demo_text = """
    🔄 Streaming demonstration in progress...

    This is a simulated streaming response.
    While this streams, you can click the STOP button
    to trigger the @cl.on_stop event!

    Watch your terminal for the event log when you stop this.

    This streaming will continue for about 10 seconds...
    """

    # Simulate streaming by sending text word by word
    words = demo_text.split()
    for i, word in enumerate(words):
        await asyncio.sleep(0.3)  # Delay to simulate streaming
        current_content = " ".join(words[:i+1])
        await msg.update(content=current_content)


async def show_event_details():
    """Show detailed information about all Chainlit events"""
    log_event("show_event_details", "- Displaying event documentation")

    event_info = """
    # 📋 Complete Chainlit Events Reference

    ## Core Lifecycle Events:

    ### 🚀 `@cl.on_chat_start`
    - **When:** New chat session begins
    - **Use for:** Welcome messages, session setup, initialization
    - **Frequency:** Once per session

    ### 💬 `@cl.on_message`
    - **When:** User sends any message
    - **Use for:** Processing input, generating responses
    - **Frequency:** Every user message

    ### ⏹️ `@cl.on_stop`
    - **When:** User clicks stop during streaming
    - **Use for:** Cleanup, partial results, cancellation handling
    - **Frequency:** When user manually stops

    ### 🔚 `@cl.on_chat_end`
    - **When:** Chat session ends (close tab, refresh)
    - **Use for:** Cleanup, saving session data
    - **Frequency:** Once per session end

    ## Advanced Events:

    ### ⚙️ `@cl.on_settings_update`
    - **When:** User changes app settings
    - **Use for:** Reconfiguring behavior based on preferences

    ### 📁 `@cl.on_file_upload`
    - **When:** User uploads a file
    - **Use for:** Processing uploaded documents, images, etc.

    **Next:** Try the 'stream' command to see `on_stop` in action!
    """

    await cl.Message(content=event_info).send()


@cl.on_stop
async def on_stop():
    """
    ⏹️ LIFECYCLE EVENT #3: Stop Requested
    This fires when the user clicks the stop button during streaming
    Perfect for: cleanup, saving partial work, cancellation handling
    """
    log_event("on_stop", "- User requested to stop streaming")

    await cl.Message(
        content="""
        🛑 **on_stop event fired!**

        You successfully triggered the stop event by clicking the stop button!

        This event is useful for:
        - Cleaning up resources
        - Saving partial work
        - Graceful cancellation

        Check your terminal to see the event log! 📋
        """
    ).send()


@cl.on_chat_end
async def on_chat_end():
    """
    🔚 LIFECYCLE EVENT #4: Chat End
    This fires when the chat session ends (user closes tab, refreshes, etc.)
    Perfect for: cleanup, saving session data, analytics
    """
    msg_count = cl.user_session.get("message_count", 0)
    start_time = cl.user_session.get("start_time", "Unknown")

    log_event("on_chat_end", f"- Session ended. Messages: {msg_count}, Started: {start_time}")

    # In a real app, you might save this data to a database
    print(f"💾 Session Summary:")
    print(f"   Messages exchanged: {msg_count}")
    print(f"   Started at: {start_time}")
    print(f"   Ended at: {datetime.now().isoformat()}")


# Optional: Additional event for demonstration
@cl.on_settings_update
async def on_settings_update(settings):
    """
    ⚙️ ADVANCED EVENT: Settings Update
    This fires when user updates app settings (requires settings configuration)
    """
    log_event("on_settings_update", f"- Settings changed: {settings}")
    print(f"🔧 Settings updated: {settings}")


if __name__ == "__main__":
    print("🔄 Chainlit Events Lifecycle Demo")
    print("Run with: chainlit run events_lifecycle.py")
    print("Watch the terminal for event logs as you interact with the app!")