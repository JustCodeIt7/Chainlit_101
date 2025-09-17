"""
Episode 2D: Deep Dive into on_message

Learning Objectives:
1. Learn how user messages are received and processed
2. Build conditional logic in handlers
3. Reply with text, formatted Markdown, or code blocks
4. Handle different message types and create intelligent routing

The @cl.on_message decorator is the heart of your conversational app:
- Receives every user message
- Provides access to message content, metadata, and attachments
- Perfect place for routing, processing, and response generation
- Supports complex conditional logic and response formatting
"""

import chainlit as cl
import re
import json
from datetime import datetime
import asyncio


@cl.on_chat_start
async def start():
    """Initialize the on_message deep dive demo"""
    cl.user_session.set("message_history", [])
    cl.user_session.set("user_profile", {
        "name": None,
        "preferences": {},
        "interaction_count": 0
    })

    await cl.Message(
        content="""
        # 💬 Deep Dive: on_message Event Handler

        **Welcome to the comprehensive on_message tutorial!**

        This demo covers:
        - 🎯 **Message routing** - Smart command detection
        - 📝 **Content formatting** - Markdown, code, lists
        - 🔍 **Input parsing** - Extract meaning from text
        - 🧠 **Context awareness** - Remember conversation flow
        - ⚡ **Advanced patterns** - Pro techniques

        ## 🚀 Try These Commands:

        **Basic Examples:**
        - `hello` - Simple greeting with personalization
        - `help` - Comprehensive help system
        - `echo [text]` - Echo back with formatting

        **Formatting Demos:**
        - `markdown` - See rich Markdown examples
        - `code python` - Get Python code samples
        - `list fruits` - Generate formatted lists

        **Advanced Features:**
        - `analyze [text]` - Text analysis with metadata
        - `math 2 + 2` - Mathematical expression parsing
        - `profile` - User profile management

        **Or just chat naturally** - I'll understand context! 🤖
        """
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """
    🎯 DEEP DIVE: Comprehensive Message Handling

    This function demonstrates:
    1. Message parsing and routing
    2. Content extraction and validation
    3. Intelligent response generation
    4. Context management and state updates
    """

    # ========================================
    # 1. MESSAGE PREPROCESSING
    # ========================================

    # Extract and normalize user input
    user_input = message.content.strip()
    original_input = user_input
    user_input_lower = user_input.lower()

    # Update session state
    profile = cl.user_session.get("user_profile", {})
    profile["interaction_count"] = profile.get("interaction_count", 0) + 1
    cl.user_session.set("user_profile", profile)

    # Track message history
    history = cl.user_session.get("message_history", [])
    history.append({
        "timestamp": datetime.now().isoformat(),
        "content": user_input,
        "length": len(user_input),
        "word_count": len(user_input.split())
    })
    # Keep only last 10 messages
    cl.user_session.set("message_history", history[-10:])

    # ========================================
    # 2. INTELLIGENT ROUTING SYSTEM
    # ========================================

    # Route to appropriate handler based on content analysis
    if user_input_lower in ["hello", "hi", "hey", "greeting"]:
        await handle_greeting(user_input)

    elif user_input_lower == "help":
        await handle_help()

    elif user_input_lower.startswith("echo "):
        await handle_echo(user_input[5:])

    elif user_input_lower == "markdown":
        await demonstrate_markdown()

    elif user_input_lower.startswith("code "):
        language = user_input[5:].strip() or "python"
        await demonstrate_code(language)

    elif user_input_lower.startswith("list "):
        topic = user_input[5:].strip() or "items"
        await generate_formatted_list(topic)

    elif user_input_lower.startswith("analyze "):
        text = user_input[8:].strip()
        await perform_text_analysis(text)

    elif user_input_lower.startswith("math "):
        expression = user_input[5:].strip()
        await handle_math(expression)

    elif user_input_lower == "profile":
        await show_user_profile()

    elif user_input_lower in ["history", "messages"]:
        await show_message_history()

    elif user_input_lower.startswith("set name "):
        name = user_input[9:].strip()
        await set_user_name(name)

    elif user_input_lower in ["clear", "reset"]:
        await clear_history()

    else:
        # ========================================
        # 3. INTELLIGENT CONVERSATION HANDLING
        # ========================================
        await handle_natural_conversation(user_input, original_input)


async def handle_greeting(user_input: str):
    """Handle greeting messages with personalization"""
    profile = cl.user_session.get("user_profile", {})
    name = profile.get("name")
    interaction_count = profile.get("interaction_count", 0)

    if name:
        greeting = f"Hello again, **{name}**! 👋"
        context = f"This is our **{interaction_count}** interaction."
    else:
        greeting = "Hello there! 👋"
        context = "I don't know your name yet. Try `set name [your name]` to personalize our chat!"

    response = f"""
    {greeting}

    {context}

    **Message Analysis:**
    - Your greeting: "{user_input}"
    - Detected intent: Friendly greeting
    - Response type: Personalized acknowledgment

    **Try these next:**
    - `help` for all available commands
    - `profile` to see your user information
    - Or just chat naturally with me!
    """

    await cl.Message(content=response).send()


async def handle_help():
    """Comprehensive help system"""
    help_content = """
    # 📚 Complete Command Reference

    ## 🎯 Basic Commands
    | Command | Description | Example |
    |---------|-------------|---------|
    | `hello` | Personalized greeting | `hello` |
    | `help` | This help menu | `help` |
    | `echo [text]` | Echo with formatting | `echo Hello World!` |

    ## 🎨 Formatting Demonstrations
    | Command | Description | Example |
    |---------|-------------|---------|
    | `markdown` | Rich Markdown showcase | `markdown` |
    | `code [lang]` | Code examples | `code python` |
    | `list [topic]` | Formatted lists | `list colors` |

    ## 🔧 Advanced Features
    | Command | Description | Example |
    |---------|-------------|---------|
    | `analyze [text]` | Text analysis | `analyze Hello world` |
    | `math [expr]` | Math evaluation | `math 2 + 2` |
    | `profile` | User information | `profile` |
    | `history` | Message history | `history` |

    ## ⚙️ Settings
    | Command | Description | Example |
    |---------|-------------|---------|
    | `set name [name]` | Set your name | `set name Alice` |
    | `clear` | Clear message history | `clear` |

    ## 💡 **Pro Tips:**
    - Commands are **case-insensitive**
    - You can also chat naturally - I understand context!
    - Check `profile` to see your interaction stats
    - Use `history` to review recent messages

    **Try any command above or just start a conversation!** 🚀
    """

    await cl.Message(content=help_content).send()


async def handle_echo(text: str):
    """Echo text with enhanced formatting"""
    if not text:
        await cl.Message(content="❌ **Echo Error:** Please provide text to echo. Example: `echo Hello World!`").send()
        return

    response = f"""
    # 🔊 Echo Response

    **Original Input:** `{text}`

    **Formatted Output:**
    > {text}

    **Analysis:**
    - Character count: {len(text)}
    - Word count: {len(text.split())}
    - Contains numbers: {'Yes' if any(c.isdigit() for c in text) else 'No'}
    - Contains special chars: {'Yes' if any(not c.isalnum() and not c.isspace() for c in text) else 'No'}

    **Variations:**
    - **Bold:** **{text}**
    - *Italic:* *{text}*
    - `Code:` `{text}`
    """

    await cl.Message(content=response).send()


async def demonstrate_markdown():
    """Showcase rich Markdown formatting"""
    markdown_demo = """
    # 🎨 Markdown Formatting Showcase

    ## Text Styling
    **Bold text** and *italic text* and ***bold italic***

    ~~Strikethrough text~~ and `inline code`

    ## Lists

    ### Unordered List:
    - First item with **bold**
    - Second item with *italic*
    - Third item with `code`
      - Nested item
      - Another nested item

    ### Ordered List:
    1. First step
    2. Second step
    3. Third step

    ## Code Blocks

    ```python
    def hello_chainlit():
        print("Hello from Chainlit!")
        return "Message sent successfully"
    ```

    ```javascript
    const chainlitApp = {
        name: "My App",
        version: "1.0.0",
        run: () => console.log("Running!")
    };
    ```

    ## Blockquotes

    > "The best way to learn Chainlit is by building with it."
    >
    > — *Chainlit Community*

    ## Tables

    | Feature | Status | Priority |
    |---------|--------|----------|
    | Text formatting | ✅ Complete | High |
    | Code highlighting | ✅ Complete | High |
    | File uploads | 🚧 In Progress | Medium |

    ## Links and Images

    [Chainlit Documentation](https://docs.chainlit.io)

    ---

    **Try:** `code python` for code examples or `list animals` for lists!
    """

    await cl.Message(content=markdown_demo).send()


async def demonstrate_code(language: str):
    """Generate code examples for different languages"""
    code_samples = {
        "python": {
            "title": "Python - Chainlit App",
            "code": '''import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Process user message
    user_input = message.content

    # Generate response
    response = f"You said: {user_input}"

    # Send back to user
    await cl.Message(content=response).send()''',
            "description": "A basic Chainlit message handler"
        },
        "javascript": {
            "title": "JavaScript - Async Function",
            "code": '''async function processMessage(message) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const result = await response.json();
        return result.reply;
    } catch (error) {
        console.error('Error:', error);
        return 'Sorry, something went wrong!';
    }
}''',
            "description": "Async message processing with error handling"
        },
        "bash": {
            "title": "Bash - Chainlit Commands",
            "code": '''#!/bin/bash

# Install Chainlit
pip install chainlit

# Run Chainlit app
chainlit run app.py

# Run with specific port
chainlit run app.py --port 8080

# Run in development mode
chainlit run app.py --watch''',
            "description": "Common Chainlit command line operations"
        }
    }

    if language.lower() not in code_samples:
        available = ", ".join(code_samples.keys())
        await cl.Message(
            content=f"❌ **Language not available.** Try: {available}\n\nExample: `code python`"
        ).send()
        return

    sample = code_samples[language.lower()]

    response = f"""
    # 💻 {sample['title']}

    **Language:** {language.title()}
    **Description:** {sample['description']}

    ```{language.lower()}
{sample['code']}
    ```

    ## 🔍 Code Analysis:
    - Lines of code: {len(sample['code'].split(chr(10)))}
    - Contains async/await: {'Yes' if 'async' in sample['code'] or 'await' in sample['code'] else 'No'}
    - Language-specific features: Demonstrated above

    **Try other languages:** `code javascript` or `code bash`
    """

    await cl.Message(content=response).send()


async def generate_formatted_list(topic: str):
    """Generate formatted lists based on topic"""
    list_data = {
        "fruits": ["🍎 Apple", "🍌 Banana", "🍊 Orange", "🍇 Grapes", "🥝 Kiwi"],
        "colors": ["🔴 Red", "🟢 Green", "🔵 Blue", "🟡 Yellow", "🟣 Purple"],
        "animals": ["🐶 Dog", "🐱 Cat", "🐘 Elephant", "🦁 Lion", "🐸 Frog"],
        "programming": ["Python 🐍", "JavaScript 📜", "Go ⚡", "Rust 🦀", "Java ☕"],
        "features": ["💬 Real-time chat", "📁 File uploads", "🎨 Rich formatting", "⚙️ User sessions", "🔄 Streaming responses"]
    }

    if topic.lower() not in list_data:
        available_topics = ", ".join(list_data.keys())
        await cl.Message(
            content=f"❌ **Topic not found.** Available topics: {available_topics}\n\nExample: `list fruits`"
        ).send()
        return

    items = list_data[topic.lower()]

    # Create different list formats
    unordered_list = "\n".join([f"- {item}" for item in items])
    ordered_list = "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])

    response = f"""
    # 📝 Formatted Lists: {topic.title()}

    ## Unordered List:
{unordered_list}

    ## Ordered List:
{ordered_list}

    ## Table Format:
    | # | Item |
    |---|------|
    """ + "\n".join([f"| {i+1} | {item} |" for i, item in enumerate(items)]) + f"""

    **List Statistics:**
    - Total items: {len(items)}
    - Topic: {topic.title()}
    - Format variations: 3 (unordered, ordered, table)

    **Try other topics:** `list programming` or `list animals`
    """

    await cl.Message(content=response).send()


async def perform_text_analysis(text: str):
    """Perform comprehensive text analysis"""
    if not text:
        await cl.Message(content="❌ **Analysis Error:** Please provide text to analyze. Example: `analyze Hello world!`").send()
        return

    # Perform various text analyses
    word_count = len(text.split())
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))
    sentence_count = len([s for s in text.split('.') if s.strip()])

    # Character type analysis
    uppercase_count = sum(1 for c in text if c.isupper())
    lowercase_count = sum(1 for c in text if c.islower())
    digit_count = sum(1 for c in text if c.isdigit())
    special_count = sum(1 for c in text if not c.isalnum() and not c.isspace())

    # Word analysis
    words = text.split()
    unique_words = len(set(word.lower() for word in words))
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0

    analysis = f"""
    # 🔍 Text Analysis Results

    **Original Text:**
    > {text}

    ## 📊 Basic Statistics
    | Metric | Count |
    |--------|-------|
    | Characters (total) | {char_count} |
    | Characters (no spaces) | {char_count_no_spaces} |
    | Words | {word_count} |
    | Unique words | {unique_words} |
    | Sentences | {sentence_count} |

    ## 🔤 Character Breakdown
    | Type | Count | Percentage |
    |------|-------|------------|
    | Uppercase | {uppercase_count} | {(uppercase_count/char_count*100):.1f}% |
    | Lowercase | {lowercase_count} | {(lowercase_count/char_count*100):.1f}% |
    | Digits | {digit_count} | {(digit_count/char_count*100):.1f}% |
    | Special chars | {special_count} | {(special_count/char_count*100):.1f}% |

    ## 📈 Advanced Metrics
    - **Average word length:** {avg_word_length:.1f} characters
    - **Lexical diversity:** {(unique_words/word_count*100):.1f}% (unique/total words)
    - **Reading estimate:** ~{word_count//200 + 1} minute(s) (200 WPM)

    ## 🎯 Content Analysis
    - **Contains questions:** {'Yes' if '?' in text else 'No'}
    - **Contains exclamations:** {'Yes' if '!' in text else 'No'}
    - **Likely language:** English (basic detection)
    - **Tone indicators:** {'Excited' if '!' in text else 'Neutral' if '?' in text else 'Calm'}

    **Try analyzing different types of text!**
    """

    await cl.Message(content=analysis).send()


async def handle_math(expression: str):
    """Handle mathematical expressions safely"""
    if not expression:
        await cl.Message(content="❌ **Math Error:** Please provide an expression. Example: `math 2 + 2`").send()
        return

    try:
        # Simple safe evaluation (only basic operations)
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Contains invalid characters")

        # Evaluate safely
        result = eval(expression)

        response = f"""
        # 🧮 Mathematical Calculation

        **Expression:** `{expression}`
        **Result:** `{result}`

        ## 📊 Calculation Details:
        - Input type: Mathematical expression
        - Operations detected: {', '.join(set(c for c in expression if c in '+-*/'))}
        - Result type: {type(result).__name__}
        - Decimal places: {len(str(result).split('.')[-1]) if '.' in str(result) else 0}

        ## ✅ Validation:
        - Safe characters only: ✅
        - Valid expression: ✅
        - Calculation successful: ✅

        **Try more examples:** `math 10 * 5`, `math (2 + 3) * 4`
        """

    except Exception as e:
        response = f"""
        # ❌ Mathematical Error

        **Expression:** `{expression}`
        **Error:** {str(e)}

        ## 🔧 Common Issues:
        - **Invalid characters:** Only use numbers, +, -, *, /, (, )
        - **Syntax errors:** Check parentheses and operators
        - **Division by zero:** Ensure denominators aren't zero

        ## ✅ Valid Examples:
        - `math 2 + 2`
        - `math (10 - 5) * 3`
        - `math 15 / 3`

        **Try a simpler expression!**
        """

    await cl.Message(content=response).send()


async def show_user_profile():
    """Display user profile and session information"""
    profile = cl.user_session.get("user_profile", {})
    history = cl.user_session.get("message_history", [])

    # Calculate session stats
    total_interactions = profile.get("interaction_count", 0)
    total_characters = sum(msg.get("length", 0) for msg in history)
    total_words = sum(msg.get("word_count", 0) for msg in history)

    profile_display = f"""
    # 👤 User Profile & Session Stats

    ## 🔍 Profile Information
    - **Name:** {profile.get('name', 'Not set (use `set name [your name]`)')}
    - **Session interactions:** {total_interactions}
    - **Messages in history:** {len(history)}

    ## 📊 Communication Stats
    - **Total characters typed:** {total_characters:,}
    - **Total words typed:** {total_words:,}
    - **Average message length:** {(total_characters / len(history)):.1f} chars per message
    - **Average words per message:** {(total_words / len(history)):.1f} words

    ## 🕒 Recent Activity
    """

    # Show last 3 messages
    if history:
        profile_display += "**Last 3 messages:**\n"
        for i, msg in enumerate(history[-3:], 1):
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
            preview = msg["content"][:30] + "..." if len(msg["content"]) > 30 else msg["content"]
            profile_display += f"{i}. `[{timestamp}]` {preview}\n"
    else:
        profile_display += "No message history yet.\n"

    profile_display += """
    ## ⚙️ Profile Management
    - **Set name:** `set name [your name]`
    - **View history:** `history`
    - **Clear history:** `clear`

    **Your data persists throughout this session!**
    """

    await cl.Message(content=profile_display).send()


async def show_message_history():
    """Display detailed message history"""
    history = cl.user_session.get("message_history", [])

    if not history:
        await cl.Message(content="📭 **No message history yet.** Start chatting to build your history!").send()
        return

    history_display = f"""
    # 📜 Message History ({len(history)} messages)

    """

    for i, msg in enumerate(history, 1):
        timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M:%S")
        preview = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]

        history_display += f"""
    **Message #{i}** `[{timestamp}]`
    > {preview}
    *{msg['word_count']} words, {msg['length']} characters*

    """

    history_display += f"""
    ## 📈 History Statistics:
    - **Total messages:** {len(history)}
    - **Total characters:** {sum(msg['length'] for msg in history):,}
    - **Total words:** {sum(msg['word_count'] for msg in history):,}
    - **Time span:** {history[0]['timestamp'][:19]} to {history[-1]['timestamp'][:19]}

    **Tip:** Use `clear` to reset history or `profile` for more stats.
    """

    await cl.Message(content=history_display).send()


async def set_user_name(name: str):
    """Set user name in profile"""
    if not name:
        await cl.Message(content="❌ **Name Error:** Please provide a name. Example: `set name Alice`").send()
        return

    profile = cl.user_session.get("user_profile", {})
    old_name = profile.get("name")
    profile["name"] = name.title()
    cl.user_session.set("user_profile", profile)

    if old_name:
        message = f"✅ **Name updated!** Changed from '{old_name}' to **{name.title()}**"
    else:
        message = f"✅ **Name set!** Nice to meet you, **{name.title()}**! 👋"

    message += "\n\n**Your name is now saved in your session. Try:**\n- `profile` to see your updated information\n- `hello` for a personalized greeting"

    await cl.Message(content=message).send()


async def clear_history():
    """Clear message history"""
    cl.user_session.set("message_history", [])

    await cl.Message(
        content="""
        # 🧹 History Cleared!

        ✅ **Message history has been reset.**

        - All previous messages removed
        - Session stats reset
        - User profile preserved (name, etc.)

        **Start fresh!** Your next message will begin a new history.
        """
    ).send()


async def handle_natural_conversation(user_input: str, original_input: str):
    """Handle natural conversation with context awareness"""
    profile = cl.user_session.get("user_profile", {})
    history = cl.user_session.get("message_history", [])
    name = profile.get("name", "friend")
    interaction_count = profile.get("interaction_count", 0)

    # Simple sentiment analysis
    positive_words = ["good", "great", "awesome", "excellent", "wonderful", "amazing", "love", "like"]
    negative_words = ["bad", "terrible", "awful", "hate", "dislike", "horrible", "worst"]

    sentiment = "neutral"
    if any(word in user_input.lower() for word in positive_words):
        sentiment = "positive"
    elif any(word in user_input.lower() for word in negative_words):
        sentiment = "negative"

    # Context from recent messages
    context_hint = ""
    if len(history) > 1:
        recent_topics = [msg['content'].lower() for msg in history[-3:]]
        if any('help' in topic for topic in recent_topics):
            context_hint = "I notice you were exploring help commands earlier. "
        elif any('code' in topic for topic in recent_topics):
            context_hint = "Continuing our code discussion, "

    response = f"""
    Hey **{name}**! {context_hint}You said:

    > {original_input}

    ## 🤖 AI Analysis:
    - **Sentiment detected:** {sentiment.title()} {['😐', '😊', '😔'][['neutral', 'positive', 'negative'].index(sentiment)]}
    - **Message length:** {len(user_input)} characters, {len(user_input.split())} words
    - **Interaction #:** {interaction_count}
    - **Context awareness:** {'Active (considering recent messages)' if context_hint else 'Fresh conversation'}

    ## 💡 Smart Suggestions:
    Based on your message, you might want to try:
    - `help` - See all available commands
    - `analyze {user_input[:20]}...` - Deep analysis of your text
    - `profile` - Check your conversation stats

    **I understand natural language!** Try asking questions, making statements, or just chatting. I'll provide contextual responses while tracking our conversation.

    **Pro tip:** Use specific commands for structured interactions, or keep chatting naturally for conversational responses! 🚀
    """

    await cl.Message(content=response).send()


if __name__ == "__main__":
    print("💬 on_message Deep Dive Demo")
    print("This demonstrates comprehensive message handling, routing, and response generation.")
    print("Run with: chainlit run on_message_deep_dive.py")