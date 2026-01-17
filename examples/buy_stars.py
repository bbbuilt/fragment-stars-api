"""
Example: Buy Telegram Stars
"""

from fragment_api import FragmentAPIClient

# Initialize client with your API server
API_URL = "https://your-api-server.com:8443"
client = FragmentAPIClient(API_URL)

# Your wallet seed phrase (base64 encoded)
# echo -n "word1 word2 ... word24" | base64
SEED = "your_seed_base64_here"

# Buy 50 stars for user
result = client.buy_stars(
    username="telegram_username",
    amount=50,
    seed=SEED
)

if result.success:
    print(f"✅ Success!")
    print(f"   Stars sent: {result.amount}")
    print(f"   Cost: {result.cost_ton} TON")
    print(f"   Commission: {result.commission_ton} TON")
    print(f"   Transaction: {result.transaction_hash}")
else:
    print(f"❌ Error: {result.error}")
