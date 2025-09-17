# Chainlit 101 - YouTube Series Code

This repository contains all the code examples for the **Chainlit 101** YouTube tutorial series.

## 📁 Project Structure

```
01-Core_Concepts/
├── 01-Hello_world/
│   └── hello_world.py              # Episode 1: Getting Started & Hello World
└── 02-Message_Lifecycle/
    ├── 2A-Project_Setup/
    │   └── project_setup.py        # Episode 2A: Project Setup & File Structure
    ├── 2B-Events_Overview/
    │   └── events_lifecycle.py     # Episode 2B: Chainlit Events Overview
    ├── 2C-On_Chat_Start/
    │   └── on_chat_start_deep_dive.py  # Episode 2C: Deep Dive into on_chat_start
    ├── 2D-On_Message/
    │   └── on_message_deep_dive.py     # Episode 2D: Deep Dive into on_message
    └── 2E-Multiple_Messages/
        └── multiple_messages_updates.py # Episode 2E: Multiple Messages & Updates
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install chainlit
```

### Running the Examples

Each file can be run independently:

```bash
# Episode 1: Hello World
chainlit run 01-Core_Concepts/01-Hello_world/hello_world.py

# Episode 2A: Project Setup
chainlit run 01-Core_Concepts/02-Message_Lifecycle/2A-Project_Setup/project_setup.py

# Episode 2B: Events Overview
chainlit run 01-Core_Concepts/02-Message_Lifecycle/2B-Events_Overview/events_lifecycle.py

# Episode 2C: on_chat_start Deep Dive
chainlit run 01-Core_Concepts/02-Message_Lifecycle/2C-On_Chat_Start/on_chat_start_deep_dive.py

# Episode 2D: on_message Deep Dive
chainlit run 01-Core_Concepts/02-Message_Lifecycle/2D-On_Message/on_message_deep_dive.py

# Episode 2E: Multiple Messages & Updates
chainlit run 01-Core_Concepts/02-Message_Lifecycle/2E-Multiple_Messages/multiple_messages_updates.py
```

## 📚 Episode Guide

### Episode 1: Getting Started with Chainlit
- **File:** `hello_world.py`
- **Topics:** Installation, basic setup, first Chainlit app
- **Key Concepts:** `@cl.on_message`, `@cl.on_chat_start`, basic responses
- **Lines of Code:** ~92

### Episode 2A: Project Setup & File Structure
- **File:** `project_setup.py`
- **Topics:** Project organization, file structure, configuration
- **Key Concepts:** Directory layout, `.chainlit/` folder, `public/` assets
- **Lines of Code:** ~85

### Episode 2B: Chainlit Events Overview
- **File:** `events_lifecycle.py`
- **Topics:** Event system, lifecycle management, decorators
- **Key Concepts:** All major event decorators, session logging, event timing
- **Lines of Code:** ~180

### Episode 2C: Deep Dive into on_chat_start
- **File:** `on_chat_start_deep_dive.py`
- **Topics:** Session initialization, user state, welcome sequences
- **Key Concepts:** `cl.user_session`, progressive onboarding, data persistence
- **Lines of Code:** ~285

### Episode 2D: Deep Dive into on_message
- **File:** `on_message_deep_dive.py`
- **Topics:** Message routing, content formatting, intelligent responses
- **Key Concepts:** Command parsing, Markdown formatting, context awareness
- **Lines of Code:** ~295

### Episode 2E: Multiple Messages & Updates
- **File:** `multiple_messages_updates.py`
- **Topics:** Sequential messages, real-time updates, progress indicators
- **Key Concepts:** Message chaining, `msg.update()`, UX patterns
- **Lines of Code:** ~280

## 🎯 Learning Path

1. **Start with Episode 1** - Get Chainlit running and understand the basics
2. **Episode 2A** - Learn proper project organization
3. **Episode 2B** - Understand the event system foundation
4. **Episode 2C** - Master session initialization
5. **Episode 2D** - Build intelligent message handling
6. **Episode 2E** - Create engaging user experiences

## 🔧 Key Features Demonstrated

- ✅ Basic Chainlit setup and configuration
- ✅ Event-driven architecture
- ✅ Session state management
- ✅ Message routing and command handling
- ✅ Rich content formatting (Markdown, code, tables)
- ✅ Real-time message updates
- ✅ Progress indicators and loading states
- ✅ Interactive demos (quizzes, stories, reports)
- ✅ Professional UX patterns

## 💡 Usage Tips

- Each file is self-contained and can be run independently
- Check the terminal output for event logging and debugging info
- All code is under 300 lines per file as requested
- Examples include extensive comments and documentation
- Interactive demos are included in most files

## 🤝 Contributing

This code is designed for educational purposes. Feel free to:
- Modify examples for your own learning
- Extend functionality with additional features
- Use as a foundation for your own Chainlit projects

## 📖 Additional Resources

- [Chainlit Documentation](https://docs.chainlit.io)
- [Chainlit GitHub](https://github.com/Chainlit/chainlit)
- [Python AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)

---

**Happy coding!** 🚀 Each example builds upon the previous ones, so follow the episode order for the best learning experience.