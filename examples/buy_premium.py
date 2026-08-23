"""
Example: Buy Telegram Premium
"""

from fragment_api import FragmentAPIClient

# Uses the public production endpoint by default.
client = FragmentAPIClient()

# Your wallet seed phrase (base64 encoded)
SEED = "your_seed_base64_here"

# Buy 3 months Premium
result = client.buy_premium(
    username="@telegram_username",
    duration=3,  # 3, 6, or 12 months
    seed=SEED,
)

if result.success:
    print("✅ Premium purchased!")
    print(f"   Cost: {result.cost_ton} TON")
    print(f"   Transaction ID: {result.transaction_id}")
    if result.expires_at:
        print(f"   Expires at: {result.expires_at}")
else:
    print(f"❌ Error: {result.error}")
