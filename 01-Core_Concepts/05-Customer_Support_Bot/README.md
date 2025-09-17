# Episode 6: Customer Support Bot - FAQs and Multi-step Logic

This episode demonstrates how to build a customer support bot with FAQ handling and multi-step logic using Chainlit's step decorators.

## Features

### 1. FAQ Database
- Pre-defined frequently asked questions and answers
- Covers common support topics: billing, passwords, refunds, etc.
- Smart matching using similarity algorithms

### 2. Multi-step Processing
- **@cl.step(type="tool")** for FAQ searching with visual feedback
- **@cl.step(type="llm")** for fallback responses
- Transparent processing with loading indicators

### 3. Smart Question Matching
- Combines text similarity and keyword overlap
- Confidence scoring for match quality
- Adjustable threshold for FAQ matching

## How It Works

1. **User asks a question** → Bot receives the message
2. **Search FAQ step** → `@cl.step` shows "🔎 Searching knowledge base..."
3. **Match evaluation** → Algorithm finds best FAQ match with confidence score
4. **Response generation**:
   - **FAQ match found** → Returns pre-written answer with confidence %
   - **No match** → Uses LLM fallback step for custom response

## Running the Bot

```bash
chainlit run support_bot.py
```

## Example Interactions

**FAQ Match:**
- User: "How do I reset my password?"
- Bot shows search step → Returns FAQ answer with 95% confidence

**No Match:**
- User: "Can you help me with a custom integration?"
- Bot shows search step → Falls back to LLM response

## Key Learning Points

- **@cl.step decorator** provides visual feedback for multi-step processes
- **FAQ matching** combines multiple algorithms for better accuracy
- **Fallback mechanisms** ensure the bot always provides helpful responses
- **Confidence scoring** shows users how certain the bot is about answers