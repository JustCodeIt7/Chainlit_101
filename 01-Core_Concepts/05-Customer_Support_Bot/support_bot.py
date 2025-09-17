import chainlit as cl
import asyncio
from typing import Optional, Dict, List
import difflib

FAQ_DATABASE = {
    "What are your business hours?": "Our business hours are Monday to Friday, 9 AM to 6 PM EST. We're closed on weekends and major holidays.",
    "How do I reset my password?": "To reset your password, go to the login page and click 'Forgot Password'. Enter your email address and we'll send you a reset link.",
    "How can I contact customer support?": "You can contact us through this chat, email us at support@company.com, or call us at 1-800-SUPPORT during business hours.",
    "What payment methods do you accept?": "We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and bank transfers.",
    "How do I cancel my subscription?": "You can cancel your subscription by going to Account Settings > Billing > Cancel Subscription. You'll retain access until the end of your current billing period.",
    "Where can I find my invoice?": "Your invoices are available in your account dashboard under Billing > Invoice History. You can download them as PDF files.",
    "Do you offer refunds?": "We offer a 30-day money-back guarantee for all new subscriptions. Contact support within 30 days for a full refund.",
    "How do I update my billing information?": "Go to Account Settings > Billing > Payment Methods to update your credit card or billing address.",
    "Is my data secure?": "Yes, we use industry-standard encryption and security measures. Your data is encrypted both in transit and at rest.",
    "Do you have a mobile app?": "Yes, you can download our mobile app from the App Store (iOS) or Google Play Store (Android)."
}

def find_best_faq_match(user_question: str, threshold: float = 0.6) -> Optional[Dict[str, str]]:
    user_question_lower = user_question.lower()
    best_match = None
    best_score = 0

    for faq_question, faq_answer in FAQ_DATABASE.items():
        faq_question_lower = faq_question.lower()

        similarity = difflib.SequenceMatcher(None, user_question_lower, faq_question_lower).ratio()

        keywords_in_user = set(user_question_lower.split())
        keywords_in_faq = set(faq_question_lower.split())
        keyword_overlap = len(keywords_in_user.intersection(keywords_in_faq)) / max(len(keywords_in_user), 1)

        combined_score = (similarity * 0.7) + (keyword_overlap * 0.3)

        if combined_score > best_score and combined_score >= threshold:
            best_score = combined_score
            best_match = {
                "question": faq_question,
                "answer": faq_answer,
                "confidence": combined_score
            }

    return best_match

@cl.step(type="tool")
async def search_faq(user_question: str) -> Optional[Dict[str, str]]:
    await cl.sleep(1)

    match = find_best_faq_match(user_question)

    if match:
        await cl.sleep(0.5)
        return match
    else:
        await cl.sleep(0.5)
        return None

@cl.step(type="llm")
async def generate_llm_response(user_question: str) -> str:
    await cl.sleep(1.5)

    response = f"""I understand you're asking about: "{user_question}"

While I don't have a specific answer in my FAQ database, I'd be happy to help you with this question. For immediate assistance, please:

1. Check our help documentation at help.company.com
2. Contact our support team at support@company.com
3. Call us at 1-800-SUPPORT during business hours

Is there anything else I can help you with today?"""

    return response

@cl.on_chat_start
async def start():
    await cl.Message(
        content="""# 🎧 Customer Support Bot

Welcome to our customer support! I'm here to help you with:

**📋 Common Questions:**
- Account and billing issues
- Password resets
- Payment methods
- Refund policies
- Technical support
- Business hours

Just ask me your question and I'll search our knowledge base to find the best answer for you!

*How can I assist you today?*"""
    ).send()

@cl.on_message
async def main(message: cl.Message):
    user_question = message.content.strip()

    if not user_question:
        await cl.Message(content="Please ask me a question and I'll do my best to help you!").send()
        return

    faq_result = await search_faq(user_question)

    if faq_result:
        confidence_percentage = int(faq_result["confidence"] * 100)

        response = f"""## ✅ Found in Knowledge Base (Match: {confidence_percentage}%)

**Q: {faq_result["question"]}**

{faq_result["answer"]}

---
*Was this helpful? If you need more specific assistance, please let me know!*"""

        await cl.Message(content=response).send()
    else:
        llm_response = await generate_llm_response(user_question)
        await cl.Message(content=llm_response).send()

if __name__ == "__main__":
    cl.run()