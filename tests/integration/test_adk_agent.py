"""
Integration test for meeting scheduler ADK agent.
"""

import pytest
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from app.agent import root_agent

@pytest.mark.asyncio
async def test_meeting_scheduler_adk_agent():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name="meeting_scheduler_test"
    )
    
    session = await session_service.create_session(
        app_name="meeting_scheduler_test",
        user_id="test_user"
    )
    
    from google.genai.types import Content, Part
    new_msg = Content(role="user", parts=[Part.from_text(text="Check available slots for 2026-09-30")])
    events = []
    for event in runner.run(
        new_message=new_msg,
        session_id=session.id,
        user_id="test_user"
    ):
        events.append(event)
        
    assert len(events) > 0
    print("\n✓ ADK root_agent runner test PASSED successfully!")
