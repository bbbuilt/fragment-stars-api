"""
Example: Check Premium Eligibility

Check if a user is eligible for Telegram Premium purchase.
"""

from fragment_api import FragmentAPIClient

# Uses the public production endpoint by default.
client = FragmentAPIClient()

# Check eligibility
username = "@example_user"
result = client.check_premium_eligibility(username)

print(f"Premium Eligibility for {username}:")
print(f"  Eligible: {result['eligible']}")

if not result['eligible']:
    print(f"  Reason: {result.get('reason', 'Unknown')}")
    if result.get("error_code"):
        print(f"  Error code: {result['error_code']}")
else:
    print("  ✅ User can purchase Premium")
