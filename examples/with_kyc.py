"""
Example: Buy Stars with KYC (lower commission)

KYC mode uses user's Fragment cookies for lower commission rate.
"""

from fragment_api import FragmentAPIClient

# Initialize client with your API server
API_URL = "https://your-api-server.com:8443"
client = FragmentAPIClient(API_URL)

# Your wallet seed phrase (base64 encoded)
SEED = "your_seed_base64_here"

# User's Fragment cookies (base64 encoded)
# 1. Login to fragment.com
# 2. Export cookies as JSON
# 3. cat cookies.json | base64
COOKIES = "user_cookies_base64_here"

# Buy with KYC (lower commission)
result = client.buy_stars(
    username="telegram_username",
    amount=100,
    seed=SEED,
    cookies=COOKIES  # This enables KYC mode
)

if result.success:
    print(f"✅ Success with KYC!")
    print(f"   Mode: {result.mode}")  # 'kyc'
    print(f"   Commission rate: {result.commission_rate}%")
else:
    print(f"❌ Error: {result.error}")
