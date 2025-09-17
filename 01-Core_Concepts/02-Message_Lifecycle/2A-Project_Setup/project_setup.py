"""
Episode 2A: Chainlit Project Setup & File Structure

Learning Objectives:
1. Understand the default file/folder layout of a Chainlit project
2. Learn where to put your app.py, config, and assets
3. See how Chainlit auto-detects the entry file

To set up a new Chainlit project:
1. Create a new directory: mkdir my_chainlit_app
2. Navigate to it: cd my_chainlit_app
3. Initialize project: chainlit init
4. Or manually create the structure shown below

Project Structure:
my_chainlit_app/
├── app.py                 # Main application file (default entry point)
├── .chainlit/             # Configuration directory
│   ├── config.toml        # App configuration
│   └── translations/      # Internationalization files
├── public/                # Static assets (images, CSS, JS)
│   ├── logo.png
│   └── favicon.ico
└── requirements.txt       # Python dependencies
"""

import chainlit as cl


# Demonstration of how Chainlit auto-detects the entry file
# When you run 'chainlit run' without specifying a file,
# Chainlit looks for these files in order:
# 1. app.py
# 2. main.py
# 3. chainlit_app.py

@cl.on_chat_start
async def start():
    """Welcome message explaining project structure"""
    await cl.Message(
        content="""
        # 📁 Chainlit Project Structure Demo

        Welcome! This demonstrates a well-organized Chainlit project.

        ## File Organization:
        - **app.py** - Main entry point (this file!)
        - **.chainlit/** - Configuration folder
        - **public/** - Static assets (logos, favicons)
        - **requirements.txt** - Dependencies

        ## Key Points:
        1. Chainlit auto-detects `app.py` as the entry file
        2. Keep your main logic here for simple projects
        3. For complex apps, split into modules and import them

        Type 'structure' to see more details!
        """
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle different commands to demonstrate project concepts"""
    user_input = message.content.lower().strip()

    if user_input == "structure":
        response = """
        ## 🏗️ Detailed Project Structure

        ```
        my_chainlit_app/
        ├── app.py              ← You are here!
        ├── .chainlit/
        │   ├── config.toml     ← App settings
        │   └── translations/   ← Multi-language support
        ├── public/
        │   ├── logo.png        ← Custom branding
        │   └── favicon.ico     ← Browser icon
        ├── utils/              ← Custom modules
        │   ├── __init__.py
        │   └── helpers.py
        └── requirements.txt    ← Dependencies
        ```

        **Try typing:** `config`, `assets`, or `modules`
        """

    elif user_input == "config":
        response = """
        ## ⚙️ Configuration (.chainlit/config.toml)

        ```toml
        [project]
        name = "My Awesome Chatbot"
        description = "A demo of Chainlit structure"

        [UI]
        show_readme_as_default = true
        default_collapse_content = true

        [meta]
        generated_by = "1.0.0"
        ```

        This file controls app behavior, UI settings, and more!
        """

    elif user_input == "assets":
        response = """
        ## 🎨 Static Assets (public/ folder)

        - **logo.png** - Displayed in the sidebar
        - **favicon.ico** - Browser tab icon
        - **custom.css** - Override default styles
        - **avatar.png** - Custom bot avatar

        Chainlit automatically serves files from `public/`
        """

    elif user_input == "modules":
        response = """
        ## 📦 Organizing Larger Projects

        ```python
        # app.py
        import chainlit as cl
        from utils.ai_helpers import get_ai_response
        from utils.database import save_conversation

        @cl.on_message
        async def main(message):
            response = await get_ai_response(message.content)
            await save_conversation(message.content, response)
            await cl.Message(content=response).send()
        ```

        Split functionality into logical modules!
        """

    else:
        response = f"""
        You said: "{message.content}"

        **Available commands:**
        - `structure` - See detailed file layout
        - `config` - Learn about configuration
        - `assets` - Understand static files
        - `modules` - Organizing larger projects
        """

    await cl.Message(content=response).send()