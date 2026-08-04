# Fragment Stars API

<div align="center">

## THE CHEAPEST FRAGMENT API

### KYC 0% · NO-KYC 0.25%

**Public rates. No API key. Verify anytime with [`GET /api/v1/commission/rates`](https://api-fragment.duckdns.org/api/v1/commission/rates).**

</div>

<p align="center">
  <strong>Telegram Stars API for Fragment.com</strong><br>
  Buy Telegram Stars and Premium from your backend with Python SDK or direct REST.<br>
  No API key. KYC 0% forever. No-KYC only 0.25%. TON + USDT on TON.
</p>

<p align="center">
  <a href="https://pypi.org/project/fragment-stars-api/"><img src="https://img.shields.io/pypi/v/fragment-stars-api?color=38BDF8&label=PyPI" alt="PyPI version"></a>
  <img src="https://img.shields.io/pypi/pyversions/fragment-stars-api?color=22C55E" alt="Python versions">
  <a href="https://api-fragment.duckdns.org"><img src="https://img.shields.io/badge/docs-live-06B6D4" alt="Documentation website"></a>
  <a href="https://github.com/bbbuilt/fragment-stars-api"><img src="https://img.shields.io/badge/LIKE_IT%3F-STAR_IT!-FACC15" alt="Like it? Star it!"></a>
  <img src="https://img.shields.io/badge/license-MIT-94A3B8" alt="MIT License">
</p>

<p align="center">
  <a href="#quick-start"><strong>Quick Start</strong></a> ·
  <a href="examples/shop_minimal.py"><strong>Minimal Shop</strong></a> ·
  <a href="docs/rest-api.md"><strong>REST API</strong></a> ·
  <a href="docs/no-kyc-vs-kyc.md"><strong>KYC vs No-KYC</strong></a> ·
  <a href="https://github.com/bbbuilt/tg_stars_premium_shop"><strong>Example Shop</strong></a> ·
  <a href="README.ru.md"><strong>RU</strong></a>
</p>

<p align="center">
  <img src="assets/fragment-api-hero.svg" alt="Lowest-cost Telegram Stars API for Fragment.com with KYC 0% and no-KYC 0.25%" width="100%">
</p>

## What You Get

<table>
  <tr>
    <td width="25%"><strong>No API key</strong><br>Client endpoints accept JSON directly. No issued token, JWT, OAuth, or <code>X-API-Key</code>.</td>
    <td width="25%"><strong>Lowest API fees</strong><br><code>0%</code> KYC forever and only <code>0.25%</code> without KYC. Verify with <code>get_rates()</code>.</td>
    <td width="25%"><strong>TON + USDT</strong><br>Use default <code>ton</code> or pass <code>usdt_ton</code> where supported.</td>
    <td width="25%"><strong>SDK + REST</strong><br>Python package plus raw HTTP examples for Node.js, PHP, Go, and any backend.</td>
  </tr>
</table>

## Start Here

| If you need to... | Open this |
|-------------------|-----------|
| Build a Telegram Stars shop | [Minimal backend](examples/shop_minimal.py) and [shop guide](docs/telegram-stars-shop.md) |
| Copy raw HTTP calls | [REST API guide](docs/rest-api.md) and [direct REST example](examples/direct_rest_payment_methods.py) |
| Choose KYC or no-KYC | [KYC vs No-KYC guide](docs/no-kyc-vs-kyc.md) |
| Debug an API error | [Errors guide](docs/errors.md) |
| Let Codex or Claude integrate it | [Codex skill](CODEX_SKILL.md) / [Claude skill](CLAUDE_SKILL.md) |
| Ask for help | [Integration Help issue](https://github.com/bbbuilt/fragment-stars-api/issues/new?template=integration-help.yml) or [@makecodev](https://t.me/makecodev) |

## Production Endpoint

```text
https://api-fragment.duckdns.org
```

```bash
curl https://api-fragment.duckdns.org/health
```

This standard HTTPS endpoint works on port `443`, including networks that block non-standard ports. Existing integrations using the legacy `:8443` endpoint remain compatible.

Client endpoints do **not** require `Authorization`, `X-API-Key`, JWT, OAuth, or issued API tokens. The API tracks commission by the TON wallet derived from the provided seed. Internal admin endpoints are separate and are not needed for client integrations.

## Quick Start

```bash
pip install fragment-stars-api
```

```python
from fragment_api import FragmentAPIClient

client = FragmentAPIClient()  # Uses https://api-fragment.duckdns.org

result = client.buy_stars(
    username="@telegram_user",
    amount=100,
    seed="your_wallet_seed_base64",
    payment_method="ton",
)

if result.success:
    print(f"Sent {result.amount} Stars")
    print(result.transaction_hash or result.transaction_id)
else:
    print(result.error)
```

To use a self-hosted or legacy endpoint, pass it explicitly as `FragmentAPIClient(base_url)`.

## Build a Telegram Stars Shop in 10 Minutes

1. Install the SDK on your backend.
2. Store `FRAGMENT_WALLET_SEED` in backend environment variables only.
3. Accept `username` and `amount` from your bot/shop.
4. Call `client.buy_stars("@telegram_user", amount, seed=...)`.
5. Return the final status to your user.

Runnable minimal backend:

```bash
pip install fastapi uvicorn fragment-stars-api
export FRAGMENT_WALLET_SEED="base64_seed_phrase"
uvicorn examples.shop_minimal:app --host 0.0.0.0 --port 8000
```

Full guide: [docs/telegram-stars-shop.md](docs/telegram-stars-shop.md). Production-ready shop example: [bbbuilt/tg_stars_premium_shop](https://github.com/bbbuilt/tg_stars_premium_shop).

## Use Cases

| Use case | Recommended path |
|----------|------------------|
| Telegram Stars shop or bot | Use `buy_stars()` from backend and poll queue automatically with SDK. |
| KYC user has Fragment cookies | Pass `fragment_cookies` / `cookies`; API commission stays `0%`. |
| Client does not want cookies | Omit cookies and use no-KYC mode. |
| Client wants USDT pricing | Pass `payment_method="usdt_ton"` for supported Stars flows. |
| Non-Python stack | Use direct REST endpoints; no API key is needed. |
| AI/vibe coding integration | Add `CODEX_SKILL.md` or `CLAUDE_SKILL.md` to the client project first. |

## KYC vs No-KYC

| Mode | Cookies required | API commission | Good for |
|------|------------------|----------------|----------|
| KYC | Yes, user's Fragment cookies | `0%` forever | Lowest cost, users comfortable with Fragment cookies |
| No-KYC | No | `0.25%` | Fast onboarding, shops that do not want user cookies |

KYC can use `ton` or `usdt_ton`. No-KYC Stars can use `ton` or `usdt_ton`; with USDT, Stars base price is paid in USDT on TON and API commission is paid in TON. More detail: [docs/no-kyc-vs-kyc.md](docs/no-kyc-vs-kyc.md).

## Python SDK vs Direct REST

| Option | Best for | Example |
|--------|----------|---------|
| Python SDK | Python bots, FastAPI, Django, background workers | [examples/payment_methods.py](examples/payment_methods.py) |
| Direct REST | Node.js, PHP, Go, Laravel, Java, Rust, custom backends | [docs/rest-api.md](docs/rest-api.md) |
| Minimal shop backend | Fastest copy-paste backend start | [examples/shop_minimal.py](examples/shop_minimal.py) |

## Runnable Examples

- [examples/shop_minimal.py](examples/shop_minimal.py) - shortest backend shop: accept `username`/`amount`, buy Stars.
- [examples/payment_methods.py](examples/payment_methods.py) - KYC / no-KYC with TON and USDT on TON.
- [examples/direct_rest_payment_methods.py](examples/direct_rest_payment_methods.py) - the same four flows with raw HTTP JSON.
- [examples/javascript_fetch.js](examples/javascript_fetch.js) - direct REST from Node.js 18+.
- [examples/php_curl.php](examples/php_curl.php) - direct REST from PHP cURL.
- [examples/go_net_http.go](examples/go_net_http.go) - direct REST from Go `net/http`.
- [examples/with_kyc.py](examples/with_kyc.py) - Fragment cookies setup for KYC mode.

## API Reference

### Direct HTTP Endpoints

Send JSON only. No API key or auth header is required.

| Method | Path | Purpose | Required JSON |
|--------|------|---------|---------------|
| `POST` | `/api/v1/stars/buy` | Buy Stars through the queue | `username`, `amount`, `seed` |
| `GET` | `/api/v1/queue/{request_id}` | Poll a Stars request | none |
| `POST` | `/api/v1/premium/buy` | Buy Premium | `username`, `duration`, `seed` |
| `POST` | `/api/v1/premium/check-eligibility` | Check Premium availability | `username` |
| `GET` | `/api/v1/prices` | Get TON and USDT-on-TON prices | none |
| `GET` | `/api/v1/commission/rates` | Check commission rates | none |

Optional purchase fields: `fragment_cookies`, `fragment_local_storage`, `payment_method`. Default `payment_method` is `ton`; use `usdt_ton` for USDT on TON where supported.

### FragmentAPIClient

```python
FragmentAPIClient(
    base_url: str,
    timeout: float = 30.0,
    poll_timeout: float = 300.0,
)
```

| Method | Description |
|--------|-------------|
| `buy_stars(username, amount, seed, cookies?, local_storage?, payment_method?, wait?)` | Buy Telegram Stars through the queue |
| `buy_premium(username, duration, seed, cookies?, local_storage?, payment_method?, wait?)` | Buy Telegram Premium directly |
| `get_prices()` | Get current TON and USDT-on-TON prices |
| `get_rates()` | Get commission rates |
| `get_queue_status()` | Get queue status and statistics |
| `check_premium_eligibility(username)` | Check if user is eligible for Premium |
| `get_status(request_id)` | Get request status |

## Common Client Mistakes

| Mistake | Correct approach |
|---------|------------------|
| Asking for an API token | Do not use API tokens for client endpoints. Send JSON to the production endpoint. |
| Sending seed from frontend | Keep seed and cookies on backend only. Never expose them in a browser or mobile app. |
| Retrying blindly after an uncertain transaction | Check wallet/TON explorer first. A blind retry can duplicate purchases. |
| Passing username without `@` in direct REST | Use `@telegram_user` format unless your SDK normalizes it. |
| Requesting fewer than 50 Stars | Fragment's minimum is 50. The SDK rejects smaller amounts before any network request or payment. |
| Using KYC without `stel_ton_token` | Connect wallet on Fragment first, then export cookies. |

Full troubleshooting: [docs/errors.md](docs/errors.md).

## Common Errors

| Error | Meaning | What to do |
|-------|---------|------------|
| `VALIDATION_ERROR` | Bad request body, wrong username format, unsupported amount or payment method | Fix the request; usernames should look like `@telegram_user`. |
| `INVALID_FRAGMENT_COOKIES` / `INVALID_FRAGMENT_LOCAL_STORAGE` | Session data is not Base64-encoded JSON | Export JSON again and Base64-encode the complete value. |
| `API_BUSY` | Another Premium browser purchase is active | Wait for it to finish and submit a new request. Do not retry automatically. |
| `INVALID_SEED` / `INVALID_WALLET_SEED` | Wallet seed is missing, malformed, or not base64 encoded correctly | Re-encode the 24-word seed on the backend. |
| `INSUFFICIENT_BALANCE` / `INSUFFICIENT_WALLET_BALANCE` | Wallet has too little TON, USDT on TON, or gas balance | Top up the wallet before creating a new request. |
| `USER_NOT_FOUND` / `TELEGRAM_USER_NOT_FOUND` | Fragment could not find the Telegram user | Check the username and try a new request. |
| `FRAGMENT_ADDITIONAL_VERIFICATION_REQUIRED` | Fragment asks the account for extra verification | Open Fragment manually with that account/cookies and complete the check. |
| `TEMPORARY_FRAGMENT_CONNECTION_ERROR` | Temporary connection problem between the API server and Fragment.com | Submit a new request later. Do not reuse the old `request_id`. |
| `TEMPORARY_FRAGMENT_FORM_NOT_READY` | Fragment page or form did not become ready in time | Submit a new request later. |
| `TON_TRANSACTION_CONFIRMATION_UNCERTAIN` | Transaction signing/sending may be uncertain | Check the wallet/TON explorer before retrying. |

## Fragment Cookies for KYC Mode

KYC mode requires Fragment.com cookies and has **0% API commission permanently**.

Required cookies:

- `stel_token`
- `stel_ssid`
- `stel_ton_token`
- `stel_dt`

Read the full guide: [COOKIES_GUIDE.md](COOKIES_GUIDE.md). If you do not want to handle cookies, use no-KYC mode by omitting the `cookies` parameter.

## Vibe Coding / AI Agent Setup

If a client integrates with Codex, Claude, Cursor, or another AI coding agent, give the agent a ready-made skill file first. It prevents invented API tokens, frontend seed leaks, cookie leaks, and duplicate purchases from blind retries.

- Codex: add [CODEX_SKILL.md](CODEX_SKILL.md) to the client project and reference it from `AGENTS.md`.
- Claude: add [CLAUDE_SKILL.md](CLAUDE_SKILL.md) to the client project or copy it into `CLAUDE.md`.
- AI-readable docs: [llms.txt](https://api-fragment.duckdns.org/llms.txt) / [llms-full.txt](https://api-fragment.duckdns.org/llms-full.txt).

## Need Help Integrating?

- Open an [Integration Help issue](https://github.com/bbbuilt/fragment-stars-api/issues/new?template=integration-help.yml).
- Contact Telegram: [@makecodev](https://t.me/makecodev).
- Show your implementation or ask for feedback in [Integration help / Show your shop](https://github.com/bbbuilt/fragment-stars-api/discussions/2).

## Contributing

Issues and integration feedback are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Do not post wallet seeds, Fragment cookies, private keys, or production customer data in public issues.

## Author

**Basebay** - backend developer focused on automation, bots, and infrastructure tools.

- Telegram: [@makecodev](https://t.me/makecodev)
- GitHub: [bbbuilt](https://github.com/bbbuilt)

## License

MIT License - see [LICENSE](LICENSE).
