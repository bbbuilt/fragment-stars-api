"""
Example: Buy Stars with KYC (lower commission)

KYC mode uses user's Fragment cookies for lower commission rate.

IMPORTANT: You need Fragment.com cookies to use KYC mode.
See README.md section "How to get Fragment cookies" for detailed instructions.

Required cookies:
- stel_token: Session authentication token
- stel_ssid: Session ID
- stel_ton_token: TON wallet connection token (REQUIRED for purchases)
- stel_dt: Timezone offset

Cookie format (JSON):
{
    "stel_token": "your_value_here",
    "stel_ssid": "your_value_here", 
    "stel_ton_token": "your_value_here",
    "stel_dt": "-180"
}

Then encode to base64:
    cat cookies.json | base64 -w 0
"""

from fragment_api import FragmentAPIClient

# Initialize client with your API server
API_URL = "https://your-api-server.com:8443"
client = FragmentAPIClient(API_URL)

# Your wallet seed phrase (base64 encoded)
# echo -n "word1 word2 ... word24" | base64
SEED = "your_seed_base64_here"

# User's Fragment cookies (base64 encoded)
# IMPORTANT: These must be from a Fragment account with connected TON wallet
# 
# How to get cookies:
# 1. Login to fragment.com in Chrome
# 2. Connect your TON wallet (Tonkeeper/MyTonWallet)
# 3. Open DevTools (F12) → Application → Cookies → https://fragment.com
# 4. Copy values of: stel_token, stel_ssid, stel_ton_token, stel_dt
# 5. Create JSON file with these cookies
# 6. Encode to base64: cat cookies.json | base64 -w 0
COOKIES = "user_cookies_base64_here"

# Buy with KYC (lower commission)
result = client.buy_stars(
    username="telegram_username",
    amount=100,
    seed=SEED,
    cookies=COOKIES  # This enables KYC mode with lower commission
)

if result.success:
    print(f"✅ Success with KYC!")
    print(f"   Mode: {result.mode}")  # 'kyc'
    print(f"   Commission rate: {result.commission_rate * 100}%")
    print(f"   Cost: {result.cost_ton} TON")
    print(f"   Commission: {result.commission_ton} TON")
else:
    print(f"❌ Error: {result.error}")
    if hasattr(result, 'error_code'):
        print(f"   Error code: {result.error_code}")
        
        # Common errors:
        if result.error_code == 'INVALID_COOKIES':
            print("\n💡 Tip: Your cookies may be expired or invalid.")
            print("   Try getting fresh cookies from fragment.com")
        elif result.error_code == 'WALLET_CONNECTION_FAILED':
            print("\n💡 Tip: Make sure your Fragment account has a connected TON wallet")
            print("   The stel_ton_token cookie is required for purchases")

