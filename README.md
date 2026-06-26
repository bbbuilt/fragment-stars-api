# Fragment Stars API

<p align="center">
  <img src="https://img.shields.io/pypi/v/fragment-stars-api?color=blue" alt="PyPI version">
  <img src="https://img.shields.io/pypi/pyversions/fragment-stars-api" alt="Python versions">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

**Python SDK for purchasing Telegram Stars and Premium via Fragment.com**

Buy Telegram Stars and Premium subscriptions programmatically using TON blockchain. Simple API, automatic transaction signing, queue management for Stars.

<p align="center">
  <strong>LIKE IT? <a href="https://github.com/bbbuilt/fragment-stars-api">STAR IT!</a></strong>
</p>

[🇷🇺 Русская версия](README.ru.md)

- Documentation website: https://api-fragment.duckdns.org
- Production API endpoint: `https://fragment-api.ydns.eu:8443`
- Example Telegram shop: https://github.com/bbbuilt/tg_stars_premium_shop
- AI integration prompts: [Codex](CODEX_SKILL.md) / [Claude](CLAUDE_SKILL.md) / [llms.txt](https://api-fragment.duckdns.org/llms.txt) / [llms-full.txt](https://api-fragment.duckdns.org/llms-full.txt)

## Production Endpoint and Auth

Use this endpoint for direct HTTP calls and SDK clients:

```text
https://fragment-api.ydns.eu:8443
```

Normal client endpoints do **not** require issued API tokens, `X-API-Key`, JWT, OAuth, or `Authorization` headers. The API identifies and tracks commission debt by the wallet derived from the provided seed. Only internal admin endpoints use `X-Admin-Key`.

Health check:

```bash
curl https://fragment-api.ydns.eu:8443/health
```

`/health` returns the current API availability status.

## Vibe Coding / AI Agent Setup

If a client integrates this API with Codex, Claude, Cursor, or another AI coding agent, give the agent the ready-made skill file first. This prevents common mistakes like inventing API tokens, putting wallet seeds in frontend code, or retrying a purchase twice.

### Codex

1. Add [CODEX_SKILL.md](CODEX_SKILL.md) to the client's project.
2. If the project uses `AGENTS.md`, add:

```md
@CODEX_SKILL.md
```

3. Ask Codex: `Integrate Fragment Stars API using the project skill.`

### Claude

1. Add [CLAUDE_SKILL.md](CLAUDE_SKILL.md) to the client's project.
2. Copy its content into `CLAUDE.md`, or tell Claude to read `CLAUDE_SKILL.md` before coding.
3. Ask Claude: `Integrate Fragment Stars API following CLAUDE_SKILL.md.`

Important rules for AI agents:

- Client API calls do not need issued API tokens or `X-API-Key`.
- Wallet seeds and Fragment cookies must stay backend-only.
- KYC mode is permanently free with `0%` API commission.
- Do not blindly retry after a transaction may have been signed or sent.

## Features

- ⭐ **Buy Telegram Stars** — gift stars to any Telegram user
- 💎 **Buy Telegram Premium** — 3, 6, or 12 month subscriptions
- 🔐 **KYC is free forever** — KYC mode has 0% API commission; call `get_rates()` if you want to verify rates before use
- 💵 **TON or USDT on TON** — pass `payment_method="usdt_ton"` when you want Fragment to invoice in USDT; default stays `ton`
- 🧩 **Two modes** — KYC with your Fragment cookies, or Non-KYC without user cookies
- ⚡ **Automatic transactions** — just provide seed phrase, SDK handles the rest
- 📊 **Queue management** — Stars purchases are queued and polled automatically
- 🛡️ **Type hints** — full typing support for IDE autocompletion

## Installation

```bash
pip install fragment-stars-api
```


## Runnable Examples

The `examples/` directory contains copy-paste integrations:

- [`examples/payment_methods.py`](examples/payment_methods.py) — KYC / Non-KYC with TON and USDT-on-TON.
- [`examples/direct_rest_payment_methods.py`](examples/direct_rest_payment_methods.py) — the same four flows with raw HTTP JSON.
- [`examples/with_kyc.py`](examples/with_kyc.py) — Fragment cookies setup for KYC mode.

## Quick Start

```python
from fragment_api import FragmentAPIClient

# Initialize with the production API server
client = FragmentAPIClient("https://fragment-api.ydns.eu:8443")

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

client = FragmentAPIClient("https://fragment-api.ydns.eu:8443")

result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="your_wallet_seed_base64"
)

print(f"Success: {result.success}")
print(f"Transaction ID: {result.transaction_id}")
```

### Payment Method Matrix: KYC / Non-KYC + TON / USDT on TON

All existing integrations keep working because `payment_method` defaults to `ton`.
Full runnable examples are in [`examples/payment_methods.py`](examples/payment_methods.py) and [`examples/direct_rest_payment_methods.py`](examples/direct_rest_payment_methods.py).

#### 1. Non-KYC + TON

No Fragment cookies are passed. API uses the owner Fragment session.

```python
result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="your_wallet_seed_base64",
    payment_method="ton",
)
```

#### 2. Non-KYC + USDT on TON

No Fragment cookies are passed. Stars base price is paid in USDT on TON; API commission is paid in TON.

```python
result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="your_wallet_seed_base64",
    payment_method="usdt_ton",
)
```

#### 3. KYC + TON

Pass Fragment cookies. API commission is always `0%`.

```python
result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="your_wallet_seed_base64",
    cookies="fragment_cookies_base64",
    payment_method="ton",
)
```

#### 4. KYC + USDT on TON

Pass Fragment cookies and choose USDT on TON. API commission is still `0%`.

```python
result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="your_wallet_seed_base64",
    cookies="fragment_cookies_base64",
    payment_method="usdt_ton",
)
```

Behavior:

- KYC mode accepts `ton` or `usdt_ton` and keeps API commission at `0%`.
- Non-KYC Stars accepts `ton` or `usdt_ton`; with `usdt_ton`, the Stars base price is paid in USDT on TON and the API commission is paid in TON.
- Non-KYC Premium currently uses TON.
- Use `client.get_prices()` or `GET /api/v1/prices` to display both TON and USDT-on-TON rates before purchase.

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
| `buy_stars(username, amount, seed, cookies?, local_storage?, payment_method?, wait?)` | Buy Telegram Stars through the queue |
| `buy_premium(username, duration, seed, cookies?, local_storage?, payment_method?, wait?)` | Buy Telegram Premium directly |
| `get_prices()` | Get current TON and USDT-on-TON prices |
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
- TON wallet with sufficient balance for gas and TON purchases
- For `payment_method="usdt_ton"`: USDT on TON balance, plus a small TON balance for gas and API commission
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
