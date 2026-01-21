"""
Example: Check Queue Status

Monitor the current queue status and processing statistics.
"""

from fragment_api import FragmentAPIClient

# Initialize client
client = FragmentAPIClient("https://your-server.com:8443")

# Get queue status
status = client.get_queue_status()

print("Queue Status:")
print(f"  Pending requests: {status['pending']}")
print(f"  Processing: {status['processing']}")
print(f"  Total processed: {status['total_processed']}")
print(f"  Average wait time: {status.get('average_wait_seconds', 'N/A')}s")

if status.get('is_paused'):
    print("  ⚠️ Queue is currently paused")
