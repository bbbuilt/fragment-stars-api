"""
Example: Check Premium Eligibility

Check if a user is eligible for Telegram Premium purchase.
"""

from fragment_api import FragmentAPIClient

# Initialize client
client = FragmentAPIClient("https://your-server.com:8443")

# Check eligibility
username = "example_user"
result = client.check_premium_eligibility(username)

print(f"Premium Eligibility for @{username}:")
print(f"  Eligible: {result['eligible']}")

if not result['eligible']:
    print(f"  Reason: {result.get('reason', 'Unknown')}")
else:
    print("  ✅ User can purchase Premium")
