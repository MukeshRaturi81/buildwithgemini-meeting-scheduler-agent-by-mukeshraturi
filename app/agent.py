"""
Meeting Scheduler ADK Root Agent.
Defines root_agent for local testing and Vertex AI Agent Runtime deployment.
"""

from google.adk.agents import Agent
from google.adk.models import Gemini

from app.tools import (
    get_available_slots,
    schedule_meeting,
    cancel_meeting,
    list_scheduled_meetings
)

SYSTEM_INSTRUCTION = """
You are an intelligent and helpful Meeting Scheduler AI Assistant.
Your job is to manage calendar events by interacting with calendar tools.

Capabilities:
1. Check open time slots for a given date (`get_available_slots`).
2. Schedule meetings with title, date, time, duration, attendees, and notes (`schedule_meeting`).
3. List all scheduled meetings (`list_scheduled_meetings`).
4. Cancel existing meetings by meeting ID (`cancel_meeting`).

Guidelines:
- If a user asks to schedule a meeting, ensure you have the date, time, title, and attendees.
- Provide clear, formatted confirmation details whenever a meeting is booked or cancelled.
- Maintain a polite, efficient, and professional tone.
"""

root_agent = Agent(
    name="root_agent",
    model=Gemini(model="gemini-flash-latest"),
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        get_available_slots,
        schedule_meeting,
        cancel_meeting,
        list_scheduled_meetings
    ]
)

from google.adk.apps import App

app = App(root_agent=root_agent, name="app")
