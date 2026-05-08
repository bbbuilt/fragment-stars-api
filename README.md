# Fragment Stars API

<p align="center">
  <img src="https://img.shields.io/pypi/v/fragment-stars-api?color=blue" alt="PyPI version">
  <img src="https://img.shields.io/pypi/pyversions/fragment-stars-api" alt="Python versions">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

**Python SDK for purchasing Telegram Stars and Premium via Fragment.com**

Buy Telegram Stars and Premium subscriptions programmatically using TON blockchain. Simple API, automatic transaction signing, queue management for Stars.

[🇷🇺 Русская версия](README.ru.md)

- Documentation website: https://wemakecode.ru/fragment-api
- Example Telegram shop: https://github.com/bbbuilt/tg_stars_premium_shop

## Features

- ⭐ **Buy Telegram Stars** — gift stars to any Telegram user
- 💎 **Buy Telegram Premium** — 3, 6, or 12 month subscriptions
- 🔐 **KYC is free forever** — KYC mode has 0% API commission; call `get_rates()` if you want to verify rates before use
- 🧩 **Two modes** — KYC with your Fragment cookies, or Non-KYC without user cookies
- ⚡ **Automatic transactions** — just provide seed phrase, SDK handles the rest
- 📊 **Queue management** — Stars purchases are queued and polled automatically
- 🛡️ **Type hints** — full typing support for IDE autocompletion

## Installation

```bash
pip install fragment-stars-api
```

## Quick Start

```python
from fragment_api import FragmentAPIClient

# Initialize with your API server
client = FragmentAPIClient("https://your-api-server.com:8443")

# Buy 50 stars for user
result = client.buy_stars("username", 50, seed="your_seed_base64")

if result.success:
    print(f"✅ Sent {result.amount} stars!")
    print(f"💰 Cost: {result.cost_ton} TON")
else:
    print(f"❌ Error: {result.error}")
```

## Usage Examples

### Buy Stars (No KYC)

Uses owner's Fragment account. Higher commission, but no user cookies needed.

```python
from fragment_api import FragmentAPIClient

client = FragmentAPIClient("https://your-api-server.com:8443")

result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="your_wallet_seed_base64"
)

print(f"Success: {result.success}")
print(f"Transaction ID: {result.transaction_id}")
```

### Buy Stars (With KYC)

Uses user's Fragment cookies. KYC mode has **0% API commission permanently**.

```python
result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="wallet_seed_base64",
    cookies="user_fragment_cookies_base64"
)
```

### Buy Premium

Premium purchases are processed immediately by the API and return the final result directly.

```python
# 3 months
result = client.buy_premium("username", 3, seed="...")

# 6 months
result = client.buy_premium("username", 6, seed="...")

# 12 months
result = client.buy_premium("username", 12, seed="...")
```

### Check Commission Rates

KYC mode is free forever, but you can call the API before using it if you want to verify the currently configured rates.

```python
rates = client.get_rates()

print(f"No KYC rate: {rates.rate_no_kyc}%")
print(f"With KYC rate: {rates.rate_with_kyc}%")
```

### Check Queue Status

```python
status = client.get_queue_status()

print(f"Queue length: {status['queue_length']}")
print(f"Estimated wait: {status['estimated_wait_seconds']}s")
```

### Check Premium Eligibility

```python
result = client.check_premium_eligibility("username")

if result['eligible']:
    print("✅ User can purchase Premium")
else:
    print(f"❌ Not eligible: {result.get('reason', 'Unknown reason')}")
```

### Async Mode (Don't Wait)

```python
# Returns immediately with request_id
response = client.buy_stars("user", 50, seed="...", wait=False)
print(f"Request ID: {response.request_id}")
print(f"Position in queue: {response.position}")

# Check status later
status = client.get_status(response.request_id)
print(f"Status: {status.status}")
```

## API Reference

### FragmentAPIClient

```python
FragmentAPIClient(
    base_url: str,              # Required - your API server URL
    timeout: float = 30.0,
    poll_timeout: float = 300.0
)
```

### Methods

| Method | Description |
|--------|-------------|
| `buy_stars(username, amount, seed, cookies?, local_storage?, wait?)` | Buy Telegram Stars through the queue |
| `buy_premium(username, duration, seed, cookies?, local_storage?, wait?)` | Buy Telegram Premium directly |
| `get_rates()` | Get commission rates |
| `get_queue_status()` | Get queue status and statistics |
| `check_premium_eligibility(username)` | Check if user is eligible for Premium |
| `get_status(request_id)` | Get request status |

### Exceptions

```python
from fragment_api import FragmentAPIError, QueueTimeoutError

try:
    result = client.buy_stars("user", 50, seed="...")
except QueueTimeoutError:
    print("Request timed out")
except FragmentAPIError as e:
    print(f"Error [{e.error_code}]: {e.message}")
```

## How It Works

1. **For Stars**, you call `buy_stars()` and the API adds the request to the queue
2. **The SDK polls** `GET /api/v1/queue/:request_id` until the Stars purchase is completed or failed
3. **For Premium**, you call `buy_premium()` and the API returns the final purchase result directly
4. **Server opens** Fragment.com in headless browser
5. **Server signs** TON transaction with your seed phrase
6. **Stars/Premium delivered** to recipient's Telegram

## Requirements

- Python 3.9+
- TON wallet with sufficient balance
- Wallet seed phrase (24 words, base64 encoded)

### How to encode seed phrase

```bash
echo -n "word1 word2 word3 ... word24" | base64
```

### How to get Fragment cookies (for KYC mode)

KYC mode requires your Fragment.com cookies and has **0% API commission permanently**.

> 📖 **[See detailed Cookie Guide](https://github.com/bbbuilt/fragment-stars-api/blob/main/COOKIES_GUIDE.md)** for step-by-step instructions with screenshots and troubleshooting.

#### Quick Guide

**Required cookies:**
- `stel_token` - Session authentication token
- `stel_ssid` - Session ID  
- `stel_ton_token` - TON wallet connection token (**CRITICAL - required for purchases**)
- `stel_dt` - Timezone offset

**Steps:**

1. **Login to Fragment**: Go to https://fragment.com and login via Telegram
2. **Connect TON Wallet**: Click "Connect Wallet" and connect Tonkeeper/MyTonWallet
3. **Open DevTools**: Press F12 → Application → Cookies → https://fragment.com
4. **Copy cookie values**: Copy the Value field for each required cookie
5. **Create JSON**:
   ```json
   {
       "stel_token": "your_value",
       "stel_ssid": "your_value",
       "stel_ton_token": "your_value",
       "stel_dt": "-180"
   }
   ```
6. **Encode to base64**:
   ```bash
   cat cookies.json | base64 -w 0
   ```
7. **Use in code**:
   ```python
   result = client.buy_stars(
       username="user",
       amount=50,
       seed="your_seed_base64",
       cookies="your_cookies_base64"
   )
   ```

> ⚠️ **Important**: The `stel_ton_token` cookie is **required** for purchases. Make sure your TON wallet is connected on fragment.com before extracting cookies!

> 💡 **Tip**: KYC mode is free forever when you provide Fragment cookies. If you don't want to deal with cookies, use No-KYC mode (just omit the `cookies` parameter); it has a commission but no cookies are needed.

## Author

**Basebay** — Backend developer focused on automation, bots, and infrastructure tools.

- Telegram: [@makecodev](https://t.me/makecodev)
- GitHub: [bbbuilt](https://github.com/bbbuilt)

## Support

- GitHub Issues: [fragment-stars-api/issues](https://github.com/bbbuilt/fragment-stars-api/issues)
- Telegram: [@makecodev](https://t.me/makecodev)

## License

MIT License - see [LICENSE](LICENSE) file.
