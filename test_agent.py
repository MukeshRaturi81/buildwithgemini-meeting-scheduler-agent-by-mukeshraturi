"""
Test script for verifying meeting scheduler agent function execution.
"""

from agent import chat_with_agent

def run_tests():
    print("--- Test 1: Checking available slots ---")
    response1 = chat_with_agent("What slots are available on 2026-09-25?")
    print("Response:\n", response1)

    print("\n--- Test 2: Scheduling a meeting ---")
    response2 = chat_with_agent(
        "Please schedule a 45-minute meeting titled 'Q3 Roadmap Sync' with Mukesh (mukesh@example.com) on 2026-09-25 at 10:30 AM."
    )
    print("Response:\n", response2)

    print("\n--- Test 3: Listing scheduled meetings ---")
    response3 = chat_with_agent("Can you show me all currently scheduled meetings?")
    print("Response:\n", response3)

if __name__ == "__main__":
    run_tests()
