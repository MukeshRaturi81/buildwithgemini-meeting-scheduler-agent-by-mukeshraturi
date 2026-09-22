"""
Tools for the Meeting Scheduler Agent.
Simulates calendar lookup, meeting creation, cancellation, and listing.
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

# In-memory database to store booked meetings
BOOKED_MEETINGS: Dict[str, dict] = {}
_MEETING_COUNTER = 100


def get_available_slots(date: str) -> dict:
    """
    Checks calendar availability for a given date.
    
    Args:
        date: The target date in YYYY-MM-DD format (e.g., '2026-09-23').
        
    Returns:
        dict: A summary containing available time slots for the requested date.
    """
    slots = ["09:00 AM", "10:30 AM", "01:00 PM", "02:30 PM", "04:00 PM"]
    booked_times = [m["time"] for m in BOOKED_MEETINGS.values() if m["date"] == date]
    available = [s for s in slots if s not in booked_times]
    
    return {
        "date": date,
        "available_slots": available,
        "total_slots": len(available),
        "status": "success"
    }


def schedule_meeting(
    title: str,
    date: str,
    time: str,
    duration_minutes: int = 30,
    attendees: List[str] = None,
    notes: str = ""
) -> dict:
    """
    Schedules a new meeting and saves it to the calendar.
    
    Args:
        title: Subject or topic of the meeting.
        date: Date in YYYY-MM-DD format.
        time: Start time (e.g., '02:00 PM' or '14:00').
        duration_minutes: Meeting duration in minutes (default is 30).
        attendees: List of attendee email addresses or names.
        notes: Agenda or notes for the meeting.
        
    Returns:
        dict: Confirmation details including assigned Meeting ID and status.
    """
    global _MEETING_COUNTER
    _MEETING_COUNTER += 1
    meeting_id = f"MTG-{_MEETING_COUNTER}"
    
    if attendees is None:
        attendees = []
        
    meeting_record = {
        "meeting_id": meeting_id,
        "title": title,
        "date": date,
        "time": time,
        "duration_minutes": duration_minutes,
        "attendees": attendees,
        "notes": notes,
        "status": "CONFIRMED",
        "created_at": datetime.now().isoformat()
    }
    
    BOOKED_MEETINGS[meeting_id] = meeting_record
    
    return {
        "status": "SUCCESS",
        "message": f"Meeting '{title}' scheduled successfully for {date} at {time}.",
        "meeting_details": meeting_record
    }


def cancel_meeting(meeting_id: str) -> dict:
    """
    Cancels an existing meeting by its Meeting ID.
    
    Args:
        meeting_id: The unique meeting identifier (e.g., 'MTG-101').
        
    Returns:
        dict: Cancellation confirmation status.
    """
    if meeting_id in BOOKED_MEETINGS:
        cancelled = BOOKED_MEETINGS.pop(meeting_id)
        cancelled["status"] = "CANCELLED"
        return {
            "status": "SUCCESS",
            "message": f"Meeting {meeting_id} ('{cancelled['title']}') has been cancelled.",
            "cancelled_meeting": cancelled
        }
    else:
        return {
            "status": "ERROR",
            "message": f"Meeting ID '{meeting_id}' not found.",
            "meeting_id": meeting_id
        }


def list_scheduled_meetings() -> dict:
    """
    Lists all currently scheduled meetings.
    
    Returns:
        dict: Active meeting list and count.
    """
    return {
        "total_meetings": len(BOOKED_MEETINGS),
        "meetings": list(BOOKED_MEETINGS.values())
    }
