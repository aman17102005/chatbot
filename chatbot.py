"""
Saathi Bot - A Rule-Based AI Chatbot
DecodeLabs AI Internship | Project 1
Author: Aman Kapuria

How it works (IPO model):
  INPUT   -> read what the user types and clean it (lowercase, trim spaces)
  PROCESS -> find the matching intent using dictionaries (no long if-elif ladder)
  OUTPUT  -> print a reply, or a fallback reply if the bot doesn't understand
The bot keeps running in a loop until the user types an exit command.
"""

import random
import string
from datetime import datetime

BOT_NAME = "Saathi"

# ---------------------------------------------------------------
# 1. VOCABULARY: many ways a user can say the same thing.
#    Each phrase points to one "intent" (topic).
# ---------------------------------------------------------------
PHRASE_TO_INTENT = {
    # greeting
    "hi": "greeting", "hello": "greeting", "hey": "greeting",
    "hii": "greeting",
    "good morning": "greeting", "good evening": "greeting",
    # how are you
    "how are you": "how_are_you", "how r u": "how_are_you",
    "whats up": "how_are_you",
    # bot's name / identity
    "what is your name": "bot_name", "who are you": "bot_name",
    "your name": "bot_name",
    # help
    "help": "help", "what can you do": "help", "menu": "help",
    # thanks
    "thanks": "thanks", "thank you": "thanks",
    # study tips
    "study tips": "study_tips", "how to study": "study_tips",
    "exam tips": "study_tips",
    # motivation
    "motivate me": "motivation", "i am sad": "motivation",
    "i am tired": "motivation", "motivation": "motivation",
    # joke
    "tell me a joke": "joke", "joke": "joke",
    # time and date
    "time": "time", "what is the time": "time",
    "date": "date", "what is the date": "date", "today": "date",
}

# ---------------------------------------------------------------
# 2. KNOWLEDGE BASE: each intent has a few replies.
#    One is picked at random so the bot feels less robotic.
# ---------------------------------------------------------------
RESPONSES = {
    "greeting": [
        "Hi! I'm Saathi, your college buddy bot.",
        "Hello there! How can I help you today?",
        "Hey! Nice to see you.",
    ],
    "how_are_you": [
        "I'm doing great, thanks for asking! How about you?",
        "All good here, just waiting to chat with you!",
    ],
    "bot_name": [
        f"I'm {BOT_NAME}, a rule-based chatbot built by Aman for the DecodeLabs AI internship.",
    ],
    "help": [
        "You can ask me: hi, how are you, study tips, motivate me, "
        "tell me a joke, time, date, or tell me your name with 'my name is ...'. "
        "Type 'bye' to leave.",
    ],
    "thanks": [
        "You're welcome!",
        "Anytime, Saathi is always here!",
    ],
    "study_tips": [
        "Study in 25-minute blocks with 5-minute breaks (Pomodoro).",
        "Solve last year's papers first. Questions repeat more than you think!",
        "Teach the topic to a friend. If you can explain it, you know it.",
    ],
    "motivation": [
        "Small steps every day beat one big jump. Keep going!",
        "Tough days don't last, but tough people do. You've got this!",
    ],
    "joke": [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the student eat his homework? The teacher said it was a piece of cake!",
    ],
}

FALLBACK_REPLY = "Sorry, I didn't understand that. Type 'help' to see what I can do."
EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye"}


def clean_input(raw_text):
    """Phase 1: Sanitization - lowercase, remove extra spaces and punctuation."""
    text = raw_text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return " ".join(text.split())  # turns many spaces into one


def get_reply(user_text, memory):
    """Phase 2 + 3: find the intent and build a reply."""

    # Special rule: remember the user's name (nested condition)
    if user_text.startswith("my name is"):
        name = user_text.replace("my name is", "", 1).strip()
        if name:
            memory["name"] = name.title()
            return f"Nice to meet you, {memory['name']}! I'll remember that."
        else:
            return "You forgot to tell me your name!"

    if user_text in ("what is my name", "whats my name"):
        if "name" in memory:
            return f"Your name is {memory['name']}."
        else:
            return "You haven't told me yet. Say 'my name is ...'"

    # Dictionary lookup: phrase -> intent (with fallback)
    intent = PHRASE_TO_INTENT.get(user_text, "unknown")

    # Live answers that can't be stored as fixed text
    if intent == "time":
        return "It's " + datetime.now().strftime("%I:%M %p") + " right now."
    if intent == "date":
        return "Today is " + datetime.now().strftime("%A, %d %B %Y") + "."

    # Dictionary lookup: intent -> replies (with fallback)
    options = RESPONSES.get(intent)
    if options is None:
        return FALLBACK_REPLY

    reply = random.choice(options)
    if intent == "greeting" and "name" in memory:
        reply = f"Hello again, {memory['name']}! " + reply
    return reply


def main():
    print("=" * 55)
    print(f"  {BOT_NAME} Bot - Rule-Based AI Chatbot (DecodeLabs)")
    print("  Type 'help' for options, 'bye' to exit.")
    print("=" * 55)

    memory = {}  # stores things like the user's name during the chat

    # The heartbeat: keep running until the exit command
    while True:
        try:
            raw_input_text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{BOT_NAME}: Goodbye! Take care.")
            break

        user_text = clean_input(raw_input_text)

        if user_text == "":
            print(f"{BOT_NAME}: Please type something.")
            continue

        if user_text in EXIT_COMMANDS:
            name = memory.get("name", "friend")
            print(f"{BOT_NAME}: Goodbye, {name}! See you soon.")
            break

        print(f"{BOT_NAME}: {get_reply(user_text, memory)}")


if __name__ == "__main__":
    main()
