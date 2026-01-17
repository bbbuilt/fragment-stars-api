"""
Example: Buy Telegram Premium
"""

from fragment_api import FragmentAPIClient

# Initialize client with your API server
API_URL = "https://your-api-server.com:8443"
client = FragmentAPIClient(API_URL)

# Your wallet seed phrase (base64 encoded)
SEED = "your_seed_base64_here"

# Buy 3 months Premium
result = client.buy_premium(
    username="telegram_username",
    duration=3,  # 3, 6, or 12 months
    seed=SEED
)

if result.success:
    print(f"✅ Premium purchased!")
    print(f"   Cost: {result.cost_ton} TON")
    print(f"   Transaction: {result.transaction_hash}")
else:
    print(f"❌ Error: {result.error}")
