"""
Example: Check Queue Status

Monitor the current queue length.
"""

from fragment_api import FragmentAPIClient

# Uses the public production endpoint by default.
client = FragmentAPIClient()

# Get queue status
status = client.get_queue_status()

print("Queue Status:")
print(f"  Queue length: {status['queue_length']}")
print(f"  Estimated wait time: {status['estimated_wait_seconds']}s")
