import chainlit as cl
from openai import AsyncOpenAI

client = AsyncOpenAI()

# System prompt for the customer support bot
system_prompt = {
    "role": "system",
    "content": "You are a helpful customer support assistant for a fictional company 'InnovateTech'. Respond courteously and concisely to user queries."
}

@cl.on_chat_start
async def on_chat_start():
    """
    Sends a welcome message to the user when the chat session starts.
    """
    await cl.Message(
        content="Hello! I’m your virtual assistant from InnovateTech. How can I assist you with our products today?",
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    """
    Handles incoming user messages and responds using the OpenAI API.
    """
    # Add the system prompt to the message history
    messages = [system_prompt]
    
    # Add the user's message to the history
    messages.append({"role": "user", "content": message.content})

    # Call the OpenAI API
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        max_tokens=250,
    )

    # Send the AI's response
    await cl.Message(content=response.choices[0].message.content).send()