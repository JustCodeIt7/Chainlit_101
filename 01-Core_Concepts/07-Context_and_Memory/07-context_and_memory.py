"""
Episode 7: Managing Context and Memory in Chainlit

Learning Objectives:
1) Understand why globals don't work for per-user state.
2) Use cl.user_session to store/retrieve data across messages in a chat.
3) Implement simple memory: remember user's name and previous questions.

How to run:
1) pip install chainlit
2) chainlit run 01-Core_Concepts/07-Context_and_Memory/07-context_and_memory.py -w
3) Open http://localhost:8000 and try:
   - "My name is Alice"
   - "What's my name?"
   - Ask a few questions ending with ? then "What was my last question?"
   - Observe the per-session message number in each reply.

Notes:
- cl.user_session stores data PER CHAT SESSION (tab/conversation), not globally.
- The small global counter below is for demo only to show why globals are shared.
"""

from __future__ import annotations

from typing import List, Optional
import re

import chainlit as cl


# Demonstration-only: A global counter that increments for every message handled
# by this Python process (all users/sessions). This illustrates why globals are
# a bad fit for per-user state in multi-user apps.
global_message_counter = 0


def extract_name(text: str) -> Optional[str]:
    """Extract a likely name from user input.

    Supports patterns like:
    - "my name is Alice"
    - "I'm Alice" / "I am Alice"
    Returns the first capitalized token after the cue. Keeps it simple on purpose.
    """

    text_norm = text.strip()

    # Try a few simple patterns. Keep it intentionally lightweight for the tutorial.
    patterns = [
        r"\bmy\s+name\s+is\s+([A-Za-z][A-Za-z\-']*)",
        r"\bi\s*am\s+([A-Za-z][A-Za-z\-']*)",
        r"\bi'm\s+([A-Za-z][A-Za-z\-']*)",
    ]

    for pat in patterns:
        m = re.search(pat, text_norm, flags=re.IGNORECASE)
        if m:
            candidate = m.group(1).strip()
            # Normalize: capitalize first letter only to keep it friendly.
            return candidate[:1].upper() + candidate[1:]

    return None


def is_name_query(text: str) -> bool:
    t = text.lower()
    return "what's my name" in t or "what is my name" in t


def is_last_question_query(text: str) -> bool:
    t = text.lower()
    return (
        "what was my last question" in t
        or "what's my last question" in t
        or "previous question" in t
        or "last question" in t
    )


def is_reset_command(text: str) -> bool:
    t = text.lower().strip()
    return t in {"reset", "reset memory", "forget", "forget me"}


@cl.on_chat_start
async def on_chat_start():
    """Initialize per-session state using cl.user_session."""

    cl.user_session.set("counter", 0)  # per-session message counter
    cl.user_session.set("name", None)  # remembered user name
    cl.user_session.set("last_questions", [])  # recent questions (strings)

    welcome = (
        "🧠 Context & Memory Demo\n\n"
        "This chat remembers simple info during YOUR session only.\n"
        "Try: 'My name is Alice', then ask 'What's my name?'.\n"
        "Ask a few questions (end with ?), then: 'What was my last question?'.\n\n"
        "Note: A global counter is shown to illustrate why globals are shared\n"
        "across users and are NOT suitable for per-user memory."
    )
    await cl.Message(content=welcome).send()


@cl.on_message
async def on_message(message: cl.Message):
    global global_message_counter

    text = (message.content or "").strip()

    # Increment global counter (all users). For demo only.
    global_message_counter += 1

    # Retrieve session state
    counter: int = cl.user_session.get("counter") or 0
    name: Optional[str] = cl.user_session.get("name")
    last_questions: List[str] = cl.user_session.get("last_questions") or []

    # Handle reset requests
    if is_reset_command(text):
        cl.user_session.set("counter", 0)
        cl.user_session.set("name", None)
        cl.user_session.set("last_questions", [])
        await cl.Message(
            content=(
                "🔄 Memory reset for THIS session. I no longer remember your name "
                "or previous questions here."
            )
        ).send()
        return

    # Update per-session counter
    counter += 1
    cl.user_session.set("counter", counter)

    # Store last questions (only those ending with '?'), keep max 5
    if text.endswith("?"):
        last_questions.append(text)
        last_questions = last_questions[-5:]
        cl.user_session.set("last_questions", last_questions)

    # If the user tells us their name, remember it
    possible_name = extract_name(text)
    name_updated_msg = None
    if possible_name:
        name = possible_name
        cl.user_session.set("name", name)
        name_updated_msg = f"Got it — I'll remember your name is {name} for this session."

    # Handle queries about name
    if is_name_query(text):
        if name:
            reply_text = f"You told me your name is {name}."
        else:
            reply_text = (
                "I don't know your name yet. You can say 'My name is Alice'."
            )
        reply_text += f"\n_(This is message #{counter} in our conversation.)_"
        reply_text += (
            f"\n_(Global messages handled by this Python process so far: {global_message_counter}.)_"
        )
        await cl.Message(content=reply_text).send()
        return

    # Handle queries about the last question
    if is_last_question_query(text):
        if last_questions:
            last_q = last_questions[-1]
            reply_text = f"Your last question was: “{last_q}”."
        else:
            reply_text = "I haven't recorded any questions yet — ask me something ending with a '?'."
        reply_text += f"\n_(This is message #{counter} in our conversation.)_"
        reply_text += (
            f"\n_(Global messages handled by this Python process so far: {global_message_counter}.)_"
        )
        await cl.Message(content=reply_text).send()
        return

    # Default reply: echo with session/global counters and optional name ack
    parts: List[str] = []
    if text:
        parts.append(f"You said: {text}")
    else:
        parts.append("Please type something for me to remember!")

    if name_updated_msg:
        parts.append(name_updated_msg)

    parts.append(f"_(This is message #{counter} in our conversation.)_")
    parts.append(
        f"_(Global messages handled by this Python process so far: {global_message_counter}.)_"
    )

    await cl.Message(content="\n\n".join(parts)).send()


@cl.on_chat_end
async def on_chat_end():
    # This fires when the user closes the chat or the session ends.
    # Session data is ephemeral and tied to this conversation only.
    print("Chat session ended — session memory cleared.")


if __name__ == "__main__":
    print(
        "This is a Chainlit app. Use 'chainlit run 01-Core_Concepts/07-Context_and_Memory/07-context_and_memory.py' to launch it."
    )
