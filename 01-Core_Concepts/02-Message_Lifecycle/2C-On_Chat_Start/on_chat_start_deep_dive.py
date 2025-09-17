"""
Episode 2C: Deep Dive into on_chat_start

Learning Objectives:
1. Use on_chat_start to initialize session state
2. Send system/welcome messages before user input
3. Set up cl.user_session with default values (like counters or flags)

The @cl.on_chat_start decorator is your app's initialization point:
- Runs once when a new chat session begins
- Perfect place to set up session variables
- Send welcome messages and instructions
- Initialize any required data structures

Key concepts:
- cl.user_session for storing session-specific data
- Multiple message sending strategies
- User onboarding and setup
"""

import chainlit as cl
import asyncio
from datetime import datetime
import random


@cl.on_chat_start
async def on_chat_start():
    """
    🚀 DEEP DIVE: on_chat_start Event Handler

    This function demonstrates the full power of the chat start event:
    1. Session initialization
    2. Welcome message sequences
    3. User state setup
    4. App configuration
    """

    # ========================================
    # 1. SESSION INITIALIZATION
    # ========================================
    # cl.user_session is a dict-like object that persists data
    # throughout the user's chat session

    # Basic session variables
    cl.user_session.set("session_id", f"session_{random.randint(1000, 9999)}")
    cl.user_session.set("start_time", datetime.now())
    cl.user_session.set("message_count", 0)
    cl.user_session.set("user_preferences", {
        "theme": "default",
        "language": "en",
        "verbose_mode": False
    })

    # App state variables
    cl.user_session.set("current_mode", "chat")
    cl.user_session.set("conversation_context", [])
    cl.user_session.set("user_name", None)

    # ========================================
    # 2. WELCOME MESSAGE SEQUENCE
    # ========================================

    # First message: Immediate welcome
    welcome_msg = cl.Message(
        content="""
        # 🎉 Welcome to Chainlit Deep Dive!

        **Session initialized successfully!** ✨

        I'm preparing your personalized chat experience...
        """,
        author="System"
    )
    await welcome_msg.send()

    # Simulate some initialization work with a brief delay
    await asyncio.sleep(1)

    # Second message: Feature overview
    features_msg = cl.Message(
        content="""
        ## 🛠️ What's Been Set Up:

        ✅ **Session Management** - Your data is tracked across messages
        ✅ **User Preferences** - Customizable settings ready
        ✅ **Context Tracking** - Conversation history maintained
        ✅ **Mode Selection** - Different interaction modes available

        ## 🎯 Available Features:

        **Session Commands:**
        - `status` - View your session information
        - `preferences` - Manage your settings
        - `reset` - Reset session data

        **Interaction Modes:**
        - `chat` - Normal conversation (current)
        - `quiz` - Interactive quiz mode
        - `help` - Detailed help system

        **Try typing your name to personalize the experience!**
        """,
        author="Assistant"
    )
    await features_msg.send()

    # Third message: Interactive setup
    await asyncio.sleep(0.5)

    setup_msg = cl.Message(
        content="""
        ## 👋 Let's Get Started!

        To demonstrate session state management, **tell me your name**
        and I'll personalize your experience.

        Or try any of these commands:
        - `demo` - See session variables in action
        - `preferences` - Customize your settings
        - `advanced` - Explore advanced features

        **Your session ID:** `{}`
        """.format(cl.user_session.get("session_id")),
        author="Setup"
    )
    await setup_msg.send()


@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle messages with full session state awareness
    """
    # Update message counter
    count = cl.user_session.get("message_count", 0) + 1
    cl.user_session.set("message_count", count)

    # Add to conversation context
    context = cl.user_session.get("conversation_context", [])
    context.append({
        "timestamp": datetime.now().isoformat(),
        "message": message.content,
        "count": count
    })
    cl.user_session.set("conversation_context", context)

    user_input = message.content.strip()
    user_name = cl.user_session.get("user_name")

    # ========================================
    # COMMAND ROUTING
    # ========================================

    if user_input.lower() == "status":
        await show_session_status()

    elif user_input.lower() == "preferences":
        await show_preferences_menu()

    elif user_input.lower() == "demo":
        await demonstrate_session_features()

    elif user_input.lower() == "reset":
        await reset_session()

    elif user_input.lower() == "advanced":
        await show_advanced_features()

    elif user_input.lower().startswith("mode"):
        new_mode = user_input.split()[-1] if len(user_input.split()) > 1 else "chat"
        await switch_mode(new_mode)

    elif not user_name and len(user_input.split()) <= 3:
        # Likely a name
        await handle_name_input(user_input)

    else:
        # Regular conversation
        await handle_regular_message(message)


async def show_session_status():
    """Display current session information"""
    session_id = cl.user_session.get("session_id")
    start_time = cl.user_session.get("start_time")
    message_count = cl.user_session.get("message_count")
    user_name = cl.user_session.get("user_name", "Anonymous")
    current_mode = cl.user_session.get("current_mode")
    preferences = cl.user_session.get("user_preferences", {})

    # Calculate session duration
    duration = datetime.now() - start_time
    duration_str = str(duration).split('.')[0]  # Remove microseconds

    status_msg = f"""
    # 📊 Session Status Report

    ## 👤 User Information:
    - **Name:** {user_name}
    - **Session ID:** `{session_id}`
    - **Current Mode:** {current_mode}

    ## ⏱️ Session Metrics:
    - **Started:** {start_time.strftime("%H:%M:%S")}
    - **Duration:** {duration_str}
    - **Messages Sent:** {message_count}

    ## ⚙️ Preferences:
    - **Theme:** {preferences.get('theme', 'default')}
    - **Language:** {preferences.get('language', 'en')}
    - **Verbose Mode:** {'On' if preferences.get('verbose_mode') else 'Off'}

    *This data persists throughout your session!*
    """

    await cl.Message(content=status_msg).send()


async def show_preferences_menu():
    """Show and handle user preferences"""
    preferences = cl.user_session.get("user_preferences", {})

    prefs_msg = f"""
    # ⚙️ User Preferences

    **Current Settings:**
    - Theme: {preferences.get('theme', 'default')}
    - Language: {preferences.get('language', 'en')}
    - Verbose Mode: {'Enabled' if preferences.get('verbose_mode') else 'Disabled'}

    **To change settings, type:**
    - `theme dark` or `theme light`
    - `language es` or `language en`
    - `verbose on` or `verbose off`

    **Example:** Type `theme dark` to switch to dark theme
    """

    await cl.Message(content=prefs_msg).send()


async def demonstrate_session_features():
    """Showcase session management capabilities"""
    context = cl.user_session.get("conversation_context", [])
    start_time = cl.user_session.get("start_time")

    demo_msg = f"""
    # 🎬 Session Features Demo

    ## 💾 Persistent Data Storage:
    Your session has been active for: **{datetime.now() - start_time}**

    ## 📝 Conversation History:
    I remember all {len(context)} of your messages:

    """

    # Show last 3 messages as examples
    for i, msg in enumerate(context[-3:], 1):
        demo_msg += f"**Message #{msg['count']}:** {msg['message'][:50]}...\n"

    demo_msg += """
    ## 🔄 State Persistence:
    - Your name, preferences, and mode are saved
    - Message count increments automatically
    - Context builds throughout the conversation

    **Try refreshing the page** - session data will reset (new session)
    **But within this session** - everything persists!
    """

    await cl.Message(content=demo_msg).send()


async def reset_session():
    """Reset session to initial state"""
    # Reset all session variables
    cl.user_session.set("message_count", 0)
    cl.user_session.set("conversation_context", [])
    cl.user_session.set("user_name", None)
    cl.user_session.set("current_mode", "chat")

    await cl.Message(
        content="""
        # 🔄 Session Reset Complete!

        All session data has been cleared:
        - Message count reset to 0
        - Conversation history cleared
        - User name removed
        - Mode reset to 'chat'

        **Session ID remains the same** (only changes on page refresh)

        You can start fresh! Try telling me your name again.
        """
    ).send()


async def show_advanced_features():
    """Show advanced on_chat_start concepts"""
    advanced_msg = """
    # 🚀 Advanced on_chat_start Features

    ## 1. **Session Initialization Patterns:**
    ```python
    @cl.on_chat_start
    async def setup():
        # Database connections
        cl.user_session.set("db", get_database_connection())

        # AI model initialization
        cl.user_session.set("model", load_ai_model())

        # User authentication
        user = await authenticate_user()
        cl.user_session.set("user", user)
    ```

    ## 2. **Multiple Message Strategies:**
    - **Immediate:** Critical information first
    - **Progressive:** Load features step by step
    - **Interactive:** Gather user input during setup

    ## 3. **Session State Best Practices:**
    - Use descriptive keys: `user_preferences`, not `prefs`
    - Initialize with defaults to avoid KeyErrors
    - Store complex objects (dicts, lists) freely
    - Remember: data persists until page refresh

    ## 4. **Real-world Use Cases:**
    - 🤖 AI chatbots: Load model and conversation history
    - 📊 Analytics: Initialize tracking variables
    - 🎮 Games: Set up player state and game board
    - 📚 Education: Load user progress and curriculum
    """

    await cl.Message(content=advanced_msg).send()


async def handle_name_input(name: str):
    """Handle when user provides their name"""
    cl.user_session.set("user_name", name.title())

    welcome_back = f"""
    # 👋 Nice to meet you, {name.title()}!

    **Your session is now personalized!**

    I've saved your name and will remember it throughout our conversation.
    You can see this by typing `status` anytime.

    ## What would you like to explore?
    - `demo` - See how session data works
    - `preferences` - Customize your experience
    - `advanced` - Learn advanced techniques

    Or just chat with me normally! I'll remember our conversation context.
    """

    await cl.Message(content=welcome_back).send()


async def switch_mode(new_mode: str):
    """Switch interaction mode"""
    valid_modes = ["chat", "quiz", "help"]

    if new_mode in valid_modes:
        cl.user_session.set("current_mode", new_mode)
        await cl.Message(
            content=f"🔄 **Mode switched to: {new_mode}**\n\nMode preferences are saved in your session!"
        ).send()
    else:
        await cl.Message(
            content=f"❌ Invalid mode. Available modes: {', '.join(valid_modes)}"
        ).send()


async def handle_regular_message(message: cl.Message):
    """Handle regular conversation"""
    user_name = cl.user_session.get("user_name", "friend")
    message_count = cl.user_session.get("message_count")
    current_mode = cl.user_session.get("current_mode")

    response = f"""
    **{user_name}**, you said: "{message.content}"

    📊 **Session Context:**
    - This is message #{message_count} in our conversation
    - Current mode: {current_mode}
    - I remember everything from our session!

    **Try:** `status`, `demo`, or `preferences` to see session features in action.
    """

    await cl.Message(content=response).send()


if __name__ == "__main__":
    print("🚀 on_chat_start Deep Dive Demo")
    print("This demonstrates comprehensive session initialization and management.")
    print("Run with: chainlit run on_chat_start_deep_dive.py")