"""
Meeting Scheduler Agent powered by Google GenAI SDK.
Wires simulated calendar tools into Gemini for automated function calling.
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import (
    get_available_slots,
    schedule_meeting,
    cancel_meeting,
    list_scheduled_meetings
)

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY is missing from environment or .env file.")
    sys.exit(1)

# Initialize GenAI Client
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are an intelligent and helpful Meeting Scheduler AI Assistant.
Your job is to manage calendar events by interacting with calendar tools.

Capabilities:
1. Check open time slots for a given date (`get_available_slots`).
2. Schedule meetings with title, date, time, duration, attendees, and notes (`schedule_meeting`).
3. List all scheduled meetings (`list_scheduled_meetings`).
4. Cancel existing meetings by meeting ID (`cancel_meeting`).

Guidelines:
- If a user asks to schedule a meeting, ensure you have the date, time, title, and attendees. If any detail is missing, ask for it concisely or use reasonable defaults.
- Always provide clear, formatted confirmation details whenever a meeting is booked or cancelled.
- Maintain a polite, efficient, and professional tone.
"""

TOOLS = [
    get_available_slots,
    schedule_meeting,
    cancel_meeting,
    list_scheduled_meetings
]


def get_chat_session():
    """
    Creates and returns a new multi-turn chat session with AFC enabled.
    """
    return client.chats.create(
        model="gemini-3.6-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=TOOLS,
            temperature=0.2,
        )
    )



# Default persistent chat session for convenience
_chat_session = None

def chat_with_agent(prompt: str) -> str:
    """
    Sends a prompt to the Gemini Meeting Scheduler Agent.
    
    Args:
        prompt: User's natural language request.
        
    Returns:
        str: Agent's response text.
    """
    global _chat_session
    if _chat_session is None:
        _chat_session = get_chat_session()
        
    response = _chat_session.send_message(prompt)
    return response.text



def main():
    print("=" * 60)
    print("📅 Meeting Scheduler Agent (Google GenAI SDK)")
    print("Type 'exit' or 'quit' to end the chat.")
    print("=" * 60)
    
    # Interactive chat loop
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            print("\nAgent thinking...")
            reply = chat_with_agent(user_input)
            print(f"\nAgent: {reply}")
            
        except KeyboardInterrupt:
            print("\nSession ended.")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()
