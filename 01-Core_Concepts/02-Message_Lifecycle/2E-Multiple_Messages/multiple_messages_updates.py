"""
Episode 2E: Handling Multiple Messages & Updates

Learning Objectives:
1. Learn to send multiple messages in sequence
2. Update an existing message after async work
3. Simulate "typing..." feedback and progressive responses
4. Master message flow control and user experience patterns

Advanced message handling techniques:
- Sequential message sending for complex responses
- Real-time message updates during processing
- Progress indicators and loading states
- Message chaining and threading
- User experience optimization
"""

import chainlit as cl
import asyncio
import random
from datetime import datetime


@cl.on_chat_start
async def start():
    """Initialize with a multi-message welcome sequence"""

    # Message 1: Immediate welcome
    welcome = cl.Message(content="# 🚀 Welcome to Multi-Message Demo!")
    await welcome.send()

    # Small delay for effect
    await asyncio.sleep(0.5)

    # Message 2: Loading indicator
    loading = cl.Message(content="⏳ **Initializing advanced message handling...**")
    await loading.send()

    # Simulate some setup work
    await asyncio.sleep(1.5)

    # Message 3: Update the loading message
    await loading.update(content="✅ **Setup complete!** All systems ready.")

    # Message 4: Feature overview
    await asyncio.sleep(0.5)
    overview = cl.Message(
        content="""
        ## 🎯 Multi-Message Patterns Demo

        **This tutorial demonstrates:**
        - 📤 **Sequential sending** - Multiple messages in order
        - 🔄 **Real-time updates** - Modify messages after sending
        - ⏱️ **Progress indicators** - Show work in progress
        - 🎭 **Simulated typing** - Natural conversation flow

        ## 🧪 Try These Demos:

        **Basic Patterns:**
        - `sequence` - Send multiple messages in order
        - `update` - Update a message in real-time
        - `progress` - Show a progress bar simulation

        **Advanced Patterns:**
        - `typing` - Simulate natural typing speed
        - `stream` - Character-by-character streaming
        - `complex` - Complex multi-step process

        **Interactive Demos:**
        - `story` - Interactive story with choices
        - `quiz` - Multi-message quiz format
        - `report` - Generate a detailed report

        **Start with `sequence` to see basic multi-message flow!** 🎬
        """
    )
    await overview.send()


@cl.on_message
async def handle_message(message: cl.Message):
    """Route to appropriate multi-message demonstration"""
    command = message.content.lower().strip()

    if command == "sequence":
        await demo_sequential_messages()
    elif command == "update":
        await demo_message_updates()
    elif command == "progress":
        await demo_progress_indicator()
    elif command == "typing":
        await demo_typing_simulation()
    elif command == "stream":
        await demo_character_streaming()
    elif command == "complex":
        await demo_complex_workflow()
    elif command == "story":
        await demo_interactive_story()
    elif command == "quiz":
        await demo_multi_message_quiz()
    elif command == "report":
        await demo_report_generation()
    elif command == "help":
        await show_help_menu()
    else:
        await handle_default_response(message.content)


async def demo_sequential_messages():
    """Demonstrate sending multiple messages in sequence"""

    # Step 1: Announce the demo
    await cl.Message(
        content="## 📤 Sequential Messages Demo\n\nWatch as I send multiple messages in order..."
    ).send()

    await asyncio.sleep(1)

    # Step 2: First message
    await cl.Message(
        content="**Message 1:** This is the first message in the sequence."
    ).send()

    await asyncio.sleep(0.8)

    # Step 3: Second message
    await cl.Message(
        content="**Message 2:** Here's the second message, sent after a short delay."
    ).send()

    await asyncio.sleep(0.8)

    # Step 4: Third message
    await cl.Message(
        content="**Message 3:** And this is the third message in our sequence."
    ).send()

    await asyncio.sleep(1)

    # Step 5: Summary
    await cl.Message(
        content="""
        ✅ **Sequential Demo Complete!**

        **Key Points:**
        - Each message is sent independently
        - `await` ensures proper ordering
        - Delays create natural conversation flow
        - Great for step-by-step instructions

        **Try:** `update` to see message modification in action!
        """
    ).send()


async def demo_message_updates():
    """Demonstrate updating messages in real-time"""

    # Create initial message
    status_msg = cl.Message(content="🔄 **Starting message update demo...**")
    await status_msg.send()

    # Simulate different stages of work
    stages = [
        ("⏳ Step 1: Preparing data...", 1.0),
        ("🔍 Step 2: Processing information...", 1.2),
        ("📊 Step 3: Analyzing results...", 1.0),
        ("✨ Step 4: Finalizing output...", 0.8),
        ("✅ **Demo complete!** Message updated 4 times in real-time.", 0)
    ]

    for content, delay in stages:
        await status_msg.update(content=content)
        if delay > 0:
            await asyncio.sleep(delay)

    # Send a follow-up message
    await asyncio.sleep(0.5)
    await cl.Message(
        content="""
        ## 🔄 Message Updates Explained

        **What happened:**
        1. Created one message object
        2. Updated its content 5 times
        3. Each update replaced the previous content
        4. Same message bubble, different content

        **Use cases:**
        - Progress indicators
        - Status updates
        - Real-time information
        - Replacing temporary content

        **Try:** `progress` for a progress bar example!
        """
    ).send()


async def demo_progress_indicator():
    """Show a progress bar simulation"""

    # Create progress message
    progress_msg = cl.Message(content="🚀 **Starting progress demo...**")
    await progress_msg.send()

    await asyncio.sleep(1)

    # Simulate progress from 0 to 100%
    for i in range(0, 101, 10):
        # Create progress bar
        filled = "█" * (i // 10)
        empty = "░" * (10 - i // 10)
        bar = f"[{filled}{empty}]"

        content = f"""
        ## 📊 Processing Data...

        **Progress:** {i}%
        ```
        {bar} {i}%
        ```

        **Status:** {'Complete!' if i == 100 else f'Working... {i}/100'}
        """

        await progress_msg.update(content=content)
        await asyncio.sleep(0.3)

    # Final update
    await asyncio.sleep(0.5)
    await progress_msg.update(
        content="""
        ## ✅ Processing Complete!

        **Progress:** 100%
        ```
        [██████████] 100%
        ```

        **Result:** All data processed successfully!
        **Time taken:** ~3 seconds
        **Items processed:** 100/100

        Progress bars are perfect for long-running operations!
        """
    )

    await cl.Message(
        content="**Try:** `typing` to see simulated natural typing speed!"
    ).send()


async def demo_typing_simulation():
    """Simulate natural typing with delays"""

    # Start typing indicator
    typing_msg = cl.Message(content="💭 *Thinking...*")
    await typing_msg.send()

    await asyncio.sleep(1)

    # Simulate typing a longer response
    full_text = """Hello! I'm simulating natural typing speed to make our conversation feel more human-like.

Notice how this text appears to be "typed" at a realistic speed, rather than appearing instantly.

This technique is great for:
• Creating engaging user experiences
• Building suspense in interactive stories
• Making AI responses feel more natural
• Providing time for users to read along

The typing speed can be adjusted based on your needs!"""

    # Clear typing indicator and start typing simulation
    await typing_msg.update(content="")

    current_text = ""
    for char in full_text:
        current_text += char
        await typing_msg.update(content=current_text + "▋")  # Show cursor

        # Variable typing speed for realism
        if char == ".":
            await asyncio.sleep(0.3)  # Pause after sentences
        elif char == "\n":
            await asyncio.sleep(0.2)  # Pause after lines
        elif char == " ":
            await asyncio.sleep(0.05)  # Brief pause after words
        else:
            await asyncio.sleep(0.03)  # Normal typing speed

    # Remove cursor
    await typing_msg.update(content=current_text)

    await cl.Message(
        content="**Try:** `stream` to see character-by-character streaming!"
    ).send()


async def demo_character_streaming():
    """Demonstrate character-by-character streaming"""

    await cl.Message(content="## 🔤 Character Streaming Demo").send()

    stream_msg = cl.Message(content="")
    await stream_msg.send()

    # Text to stream
    streaming_text = """# Character-by-Character Streaming

This is **character streaming** - each character appears one by one!

**Benefits:**
• Real-time response feeling
• Engaging user experience
• Perfect for AI chat applications
• Shows "thinking" process

**Implementation:**
```python
for char in text:
    current += char
    await msg.update(content=current)
    await asyncio.sleep(0.05)
```

Streaming complete! ✨"""

    # Stream the text
    current_content = ""
    for char in streaming_text:
        current_content += char
        await stream_msg.update(content=current_content)
        await asyncio.sleep(0.02)  # Fast streaming

    await asyncio.sleep(0.5)
    await cl.Message(
        content="**Try:** `complex` for a complex multi-step workflow demo!"
    ).send()


async def demo_complex_workflow():
    """Demonstrate a complex multi-message workflow"""

    # Step 1: Introduction
    await cl.Message(
        content="## ⚙️ Complex Workflow Demo\n\nSimulating a real-world multi-step process..."
    ).send()

    await asyncio.sleep(1)

    # Step 2: Create status tracker
    status_tracker = cl.Message(content="🔄 **Initializing workflow...**")
    await status_tracker.send()

    # Step 3: Multiple parallel "workers"
    workers = []
    for i in range(3):
        worker = cl.Message(content=f"👷 **Worker {i+1}:** Idle")
        await worker.send()
        workers.append(worker)
        await asyncio.sleep(0.3)

    await asyncio.sleep(1)

    # Step 4: Start processing
    await status_tracker.update(content="🚀 **Workflow started!** Processing in parallel...")

    # Simulate parallel work
    tasks = [
        ("Data Collection", ["Connecting to database", "Fetching records", "Validating data", "Complete"]),
        ("Analysis", ["Loading models", "Running calculations", "Generating insights", "Complete"]),
        ("Reporting", ["Creating template", "Populating data", "Formatting output", "Complete"])
    ]

    # Process tasks in parallel simulation
    for step in range(4):
        for i, (task_name, steps) in enumerate(tasks):
            if step < len(steps):
                status = "✅" if steps[step] == "Complete" else "🔄"
                await workers[i].update(
                    content=f"👷 **Worker {i+1} ({task_name}):** {status} {steps[step]}"
                )

        await asyncio.sleep(1.5)

    # Step 5: Final summary
    await status_tracker.update(content="✅ **All workflows complete!**")

    await asyncio.sleep(0.5)

    # Step 6: Results summary
    await cl.Message(
        content="""
        ## 📋 Workflow Results

        **Completed Tasks:**
        ✅ Data Collection - 1,247 records processed
        ✅ Analysis - 15 insights generated
        ✅ Reporting - PDF report created

        **Performance:**
        - Total time: ~8 seconds
        - Parallel processing: 3 workers
        - Success rate: 100%

        **Complex workflows demonstrate:**
        - Multiple message coordination
        - Real-time status updates
        - Parallel process simulation
        - Professional UX patterns

        **Try:** `story` for an interactive story experience!
        """
    ).send()


async def demo_interactive_story():
    """Create an interactive story with multiple messages"""

    # Chapter 1
    await cl.Message(
        content="""
        # 📚 Interactive Story Demo

        ## Chapter 1: The Mysterious Cave

        You find yourself standing at the entrance of a dark cave.
        Strange symbols glow faintly on the walls, and you hear
        distant echoes from within.

        **What do you do?**
        """
    ).send()

    # Choice presentation
    await asyncio.sleep(0.5)
    choice_msg = cl.Message(
        content="""
        **Choose your action:**

        🔦 **A)** Enter the cave with your flashlight
        🗣️ **B)** Call out to see if anyone responds
        🚶 **C)** Walk away and find another path
        📝 **D)** Examine the symbols more closely

        *(In a real app, you'd wait for user input. For this demo, I'll continue automatically...)*
        """
    )
    await choice_msg.send()

    # Simulate waiting for choice
    await asyncio.sleep(2)
    await choice_msg.update(
        content="""
        **Choose your action:**

        🔦 **A)** Enter the cave with your flashlight ← *You chose this!*
        🗣️ **B)** Call out to see if anyone responds
        🚶 **C)** Walk away and find another path
        📝 **D)** Examine the symbols more closely

        *Processing your choice...*
        """
    )

    await asyncio.sleep(1.5)

    # Chapter 2
    await cl.Message(
        content="""
        ## Chapter 2: Inside the Cave

        You step into the cave, your flashlight cutting through the darkness.
        The air is cool and damp. As you venture deeper, you discover a
        magnificent underground chamber filled with ancient artifacts!

        **Suddenly, you hear footsteps behind you...**
        """
    ).send()

    await asyncio.sleep(2)

    # Cliffhanger ending
    suspense = cl.Message(content="*Something approaches in the darkness...*")
    await suspense.send()

    await asyncio.sleep(1.5)

    await suspense.update(
        content="""
        **To be continued...** 📖

        ## 🎭 Interactive Story Features Demonstrated:

        ✅ **Chapter progression** - Sequential story delivery
        ✅ **Choice presentation** - Multiple options display
        ✅ **Choice confirmation** - Show user selection
        ✅ **Suspense building** - Timed reveals
        ✅ **Cliffhanger endings** - Keep users engaged

        **In a real interactive story app:**
        - Wait for actual user input
        - Branch story based on choices
        - Save story progress in session
        - Support multiple story paths

        **Try:** `quiz` for a multi-message quiz format!
        """
    )


async def demo_multi_message_quiz():
    """Create a multi-message quiz experience"""

    # Quiz introduction
    await cl.Message(
        content="""
        # 🧠 Multi-Message Quiz Demo

        **Welcome to the Chainlit Knowledge Quiz!**

        This demonstrates how to create engaging quiz experiences
        using multiple messages and real-time updates.

        **Quiz Rules:**
        - 3 questions total
        - Multiple choice format
        - Immediate feedback
        - Running score tracking

        **Let's begin!** 🚀
        """
    ).send()

    await asyncio.sleep(1)

    # Score tracker
    score_msg = cl.Message(content="📊 **Score: 0/0** (0%)")
    await score_msg.send()

    questions = [
        {
            "question": "What is Chainlit primarily used for?",
            "options": ["A) Web scraping", "B) Building chat interfaces", "C) Database management", "D) Image processing"],
            "correct": "B",
            "explanation": "Chainlit is a Python framework for building conversational AI applications with chat interfaces."
        },
        {
            "question": "Which decorator handles user messages in Chainlit?",
            "options": ["A) @cl.on_start", "B) @cl.on_message", "C) @cl.handle_message", "D) @cl.chat_handler"],
            "correct": "B",
            "explanation": "@cl.on_message is the main decorator for handling incoming user messages."
        },
        {
            "question": "How do you send a message to the user in Chainlit?",
            "options": ["A) cl.send(message)", "B) return message", "C) await cl.Message(content).send()", "D) print(message)"],
            "correct": "C",
            "explanation": "You create a cl.Message object with content and await its send() method."
        }
    ]

    score = 0

    for i, q in enumerate(questions, 1):
        await asyncio.sleep(1)

        # Question
        question_msg = cl.Message(
            content=f"""
            ## Question {i}/3

            **{q['question']}**

            {chr(10).join(q['options'])}

            *(In a real quiz, you'd wait for user input. Auto-selecting for demo...)*
            """
        )
        await question_msg.send()

        # Simulate thinking time
        await asyncio.sleep(2)

        # Simulate random answer (for demo)
        user_answer = random.choice(["A", "B", "C", "D"])
        is_correct = user_answer == q["correct"]
        if is_correct:
            score += 1

        # Show answer feedback
        feedback_icon = "✅" if is_correct else "❌"
        await question_msg.update(
            content=f"""
            ## Question {i}/3 - {feedback_icon} {'Correct!' if is_correct else 'Incorrect'}

            **{q['question']}**

            {chr(10).join(q['options'])}

            **Your answer:** {user_answer}
            **Correct answer:** {q['correct']}

            **Explanation:** {q['explanation']}
            """
        )

        # Update score
        percentage = (score / i) * 100
        await score_msg.update(content=f"📊 **Score: {score}/{i}** ({percentage:.0f}%)")

        await asyncio.sleep(1.5)

    # Final results
    await asyncio.sleep(1)
    final_percentage = (score / len(questions)) * 100

    performance = "Excellent! 🏆" if score == 3 else "Good job! 👍" if score >= 2 else "Keep learning! 📚"

    await cl.Message(
        content=f"""
        # 🎉 Quiz Complete!

        ## Final Results:
        **Score:** {score}/{len(questions)} ({final_percentage:.0f}%)
        **Performance:** {performance}

        ## 🎓 Quiz Features Demonstrated:
        ✅ **Progressive questions** - One at a time
        ✅ **Real-time scoring** - Updated after each question
        ✅ **Immediate feedback** - Right/wrong with explanations
        ✅ **Visual indicators** - ✅/❌ for quick recognition
        ✅ **Final summary** - Complete performance overview

        **Multi-message quizzes create engaging, educational experiences!**

        **Try:** `report` for a comprehensive report generation demo!
        """
    ).send()


async def demo_report_generation():
    """Demonstrate generating a detailed report with multiple messages"""

    # Report introduction
    await cl.Message(
        content="""
        # 📊 Report Generation Demo

        **Generating comprehensive analysis report...**

        This demonstrates how to build detailed reports using
        multiple messages for better organization and readability.
        """
    ).send()

    await asyncio.sleep(1)

    # Progress tracker
    progress = cl.Message(content="🔄 **Preparing report sections...** (0/5)")
    await progress.send()

    # Section 1: Executive Summary
    await asyncio.sleep(1)
    await progress.update(content="📝 **Generating Executive Summary...** (1/5)")
    await asyncio.sleep(1.5)

    await cl.Message(
        content="""
        ## 📋 Executive Summary

        **Report Date:** {date}
        **Analysis Period:** Last 30 days
        **Status:** Complete

        **Key Findings:**
        - System performance: 99.2% uptime
        - User engagement: +15% increase
        - Response time: Average 0.3s
        - Error rate: 0.1% (within target)

        **Recommendations:** Continue current optimization strategies
        """.format(date=datetime.now().strftime("%Y-%m-%d"))
    ).send()

    # Section 2: Performance Metrics
    await progress.update(content="📈 **Analyzing Performance Metrics...** (2/5)")
    await asyncio.sleep(1.5)

    await cl.Message(
        content="""
        ## 📈 Performance Metrics

        | Metric | Current | Target | Status |
        |--------|---------|--------|---------|
        | Uptime | 99.2% | 99.0% | ✅ Above target |
        | Response Time | 0.3s | 0.5s | ✅ Above target |
        | Throughput | 1,250 req/min | 1,000 req/min | ✅ Above target |
        | Error Rate | 0.1% | 0.5% | ✅ Below target |

        **Trend Analysis:**
        - Performance improved 8% over last month
        - Peak usage: 2-4 PM daily
        - No significant outages recorded
        """
    ).send()

    # Section 3: User Analytics
    await progress.update(content="👥 **Processing User Analytics...** (3/5)")
    await asyncio.sleep(1.5)

    await cl.Message(
        content="""
        ## 👥 User Analytics

        **Active Users:**
        - Daily active: 2,847 (+12%)
        - Weekly active: 15,423 (+8%)
        - Monthly active: 48,291 (+15%)

        **User Behavior:**
        - Average session: 8.3 minutes
        - Messages per session: 12.7
        - Return rate: 67%

        **Popular Features:**
        1. Message formatting (89% usage)
        2. File uploads (45% usage)
        3. Code examples (34% usage)

        **Geographic Distribution:**
        - North America: 45%
        - Europe: 32%
        - Asia-Pacific: 18%
        - Other: 5%
        """
    ).send()

    # Section 4: Technical Insights
    await progress.update(content="🔧 **Compiling Technical Insights...** (4/5)")
    await asyncio.sleep(1.5)

    await cl.Message(
        content="""
        ## 🔧 Technical Insights

        **System Resources:**
        ```
        CPU Usage:     ████████░░ 80%
        Memory:        ██████░░░░ 60%
        Disk I/O:      ███░░░░░░░ 30%
        Network:       █████░░░░░ 50%
        ```

        **Performance Bottlenecks:**
        - Database queries: Optimized (-20% latency)
        - Memory usage: Stable
        - Network bandwidth: Well within limits

        **Recent Optimizations:**
        ✅ Implemented connection pooling
        ✅ Added Redis caching layer
        ✅ Optimized database indexes
        ✅ Upgraded server infrastructure

        **Upcoming Improvements:**
        🔄 WebSocket implementation
        🔄 CDN integration
        🔄 Auto-scaling setup
        """
    ).send()

    # Section 5: Recommendations
    await progress.update(content="💡 **Finalizing Recommendations...** (5/5)")
    await asyncio.sleep(1.5)

    await cl.Message(
        content="""
        ## 💡 Recommendations & Next Steps

        ### Immediate Actions (Next 7 days)
        1. **Monitor peak hours** - Scale resources for 2-4 PM traffic
        2. **Update documentation** - Reflect recent feature additions
        3. **User feedback collection** - Deploy satisfaction survey

        ### Short-term Goals (Next 30 days)
        1. **WebSocket implementation** - Reduce latency by 40%
        2. **Mobile optimization** - Improve mobile user experience
        3. **Advanced analytics** - Deploy user behavior tracking

        ### Long-term Strategy (Next 90 days)
        1. **AI integration** - Implement smart response suggestions
        2. **Multi-language support** - Expand to 5 new languages
        3. **Enterprise features** - SSO, advanced permissions

        ### Resource Requirements
        - **Development time:** 2-3 weeks
        - **Budget estimate:** $15,000-$25,000
        - **Team members:** 3-4 developers

        **Priority Rating:** High ⭐⭐⭐⭐⭐
        """
    ).send()

    # Final completion
    await progress.update(content="✅ **Report generation complete!** (5/5)")

    await asyncio.sleep(1)

    await cl.Message(
        content="""
        # ✅ Report Generation Complete!

        ## 📊 Report Summary:
        - **Total sections:** 5
        - **Generation time:** ~12 seconds
        - **Data points analyzed:** 25+
        - **Recommendations:** 9 actionable items

        ## 🎯 Multi-Message Report Benefits:

        ✅ **Organized structure** - Clear section separation
        ✅ **Progressive loading** - Show progress to users
        ✅ **Digestible chunks** - Easier to read and understand
        ✅ **Visual appeal** - Tables, charts, and formatting
        ✅ **Professional presentation** - Business-ready output

        **Multi-message reports are perfect for:**
        - Business analytics dashboards
        - System monitoring summaries
        - User activity reports
        - Performance evaluations
        - Research findings

        **🎉 You've completed all multi-message demos!**
        Type `help` to see all available commands again.
        """
    ).send()


async def show_help_menu():
    """Display comprehensive help menu"""
    help_content = """
    # 📖 Multi-Message & Updates Help

    ## 🎬 Demo Commands:

    ### Basic Patterns
    | Command | Description |
    |---------|-------------|
    | `sequence` | Multiple messages in order |
    | `update` | Real-time message updates |
    | `progress` | Progress bar simulation |

    ### Advanced Techniques
    | Command | Description |
    |---------|-------------|
    | `typing` | Natural typing simulation |
    | `stream` | Character streaming |
    | `complex` | Multi-step workflow |

    ### Interactive Examples
    | Command | Description |
    |---------|-------------|
    | `story` | Interactive story experience |
    | `quiz` | Multi-message quiz format |
    | `report` | Professional report generation |

    ## 🔧 Technical Concepts:

    **Sequential Messages:**
    ```python
    await cl.Message("First").send()
    await cl.Message("Second").send()
    ```

    **Message Updates:**
    ```python
    msg = cl.Message("Loading...")
    await msg.send()
    await msg.update(content="Complete!")
    ```

    **Progressive Updates:**
    ```python
    for i in range(100):
        await msg.update(f"Progress: {i}%")
        await asyncio.sleep(0.1)
    ```

    **Start exploring with any command above!** 🚀
    """

    await cl.Message(content=help_content).send()


async def handle_default_response(user_input: str):
    """Handle unrecognized commands with helpful suggestions"""

    # First message: Acknowledge input
    await cl.Message(
        content=f"""
        **You said:** "{user_input}"

        I didn't recognize that command, but let me help you explore the available demos!
        """
    ).send()

    await asyncio.sleep(0.5)

    # Second message: Show suggestions
    suggestions = cl.Message(content="🔍 **Finding relevant demos for you...**")
    await suggestions.send()

    await asyncio.sleep(1)

    # Update with actual suggestions
    await suggestions.update(
        content="""
        ## 💡 Available Demos:

        **Quick Start:**
        - `sequence` - See basic multi-message flow
        - `update` - Watch messages change in real-time

        **Interactive:**
        - `story` - Experience an interactive story
        - `quiz` - Try a knowledge quiz

        **Advanced:**
        - `progress` - See progress indicators
        - `complex` - Multi-step workflow simulation

        **Type `help` for the complete command list!**

        **Or try `sequence` to get started** 🎯
        """
    )


if __name__ == "__main__":
    print("📨 Multiple Messages & Updates Demo")
    print("This demonstrates advanced message handling patterns, updates, and user experience techniques.")
    print("Run with: chainlit run multiple_messages_updates.py")