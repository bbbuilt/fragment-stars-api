"""
Example: Buy Telegram Stars
"""

import os

from fragment_api import FragmentAPIClient

# Uses the public production endpoint by default.
client = FragmentAPIClient()

# Base64-encoded supported seed. Keep it in backend environment variables.
SEED = os.environ["FRAGMENT_WALLET_SEED"]

# Buy 50 stars for user
result = client.buy_stars(username="@telegram_username", amount=50, seed=SEED)

if result.success:
    print("✅ Success!")
    print(f"   Stars sent: {result.amount}")
    print(f"   Cost: {result.cost_ton} TON")
    print(f"   Commission: {result.commission_ton} TON")
    print(f"   Transaction ID: {result.transaction_id}")
    if result.transaction_hash:
        print(f"   Transaction hash: {result.transaction_hash}")
else:
    print(f"❌ Error: {result.error}")
