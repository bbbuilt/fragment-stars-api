"""
Example: Async mode (don't wait for result)

Useful when you want to handle the result later or in a different process.
"""

import time
from fragment_api import FragmentAPIClient, QueueStatus

# Initialize client with your API server
API_URL = "https://your-api-server.com:8443"
client = FragmentAPIClient(API_URL)

SEED = "your_seed_base64_here"

# Start purchase without waiting
response = client.buy_stars(
    username="telegram_username",
    amount=50,
    seed=SEED,
    wait=False  # Don't wait for result
)

print(f"Request submitted!")
print(f"  Request ID: {response.request_id}")
print(f"  Position: {response.position}")
print(f"  Estimated wait: {response.estimated_wait_seconds}s")

# Poll for result manually
while True:
    status = client.get_status(response.request_id)
    print(f"Status: {status.status}")
    
    if status.status == QueueStatus.COMPLETED:
        print(f"✅ Done! Result: {status.result}")
        break
    elif status.status == QueueStatus.FAILED:
        print(f"❌ Failed: {status.error}")
        break
    
    time.sleep(5)
