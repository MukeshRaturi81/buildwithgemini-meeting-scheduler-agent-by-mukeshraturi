"""
Unit tests for meeting scheduler tools.
"""

from tools import get_available_slots, schedule_meeting, cancel_meeting, list_scheduled_meetings

def test_tools():
    # Test slot lookup
    slots = get_available_slots("2026-09-23")
    assert slots["status"] == "success"
    assert len(slots["available_slots"]) > 0
    print("✓ get_available_slots passed:", slots)

    # Test schedule meeting
    result = schedule_meeting(
        title="Project Sync",
        date="2026-09-23",
        time="02:30 PM",
        duration_minutes=30,
        attendees=["alice@example.com", "bob@example.com"],
        notes="Discuss Phase 2 deployment"
    )
    assert result["status"] == "SUCCESS"
    meeting_id = result["meeting_details"]["meeting_id"]
    print("✓ schedule_meeting passed:", result["message"])

    # Test list meetings
    meetings = list_scheduled_meetings()
    assert meetings["total_meetings"] == 1
    print("✓ list_scheduled_meetings passed:", meetings["total_meetings"], "meeting(s)")

    # Test cancel meeting
    cancel_res = cancel_meeting(meeting_id)
    assert cancel_res["status"] == "SUCCESS"
    print("✓ cancel_meeting passed:", cancel_res["message"])

    # Confirm list is empty after cancellation
    assert list_scheduled_meetings()["total_meetings"] == 0
    print("All tool tests passed successfully!")

if __name__ == "__main__":
    test_tools()
