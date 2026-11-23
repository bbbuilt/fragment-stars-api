# Direct REST API

Use direct REST if your backend is not Python or you do not want to use the SDK. Client endpoints do not require an API key.

Base URL:

```text
https://api.fragment-api.space
```

The legacy `https://api-fragment.duckdns.org` and `https://fragment-api.ydns.eu:8443` endpoints remain compatible.

## Read-Only Connectivity Check

No wallet data is required and no purchase is made:

```bash
curl https://api.fragment-api.space/health
curl https://api.fragment-api.space/api/v1/prices
curl https://api.fragment-api.space/api/v1/commission/rates
```

Purchase calls below send the seed to the hosted API for signing and spend funds when valid credentials are supplied. Keep them server-to-server, use a dedicated wallet, and read [SECURITY.md](../SECURITY.md).

## Resolve a 12-Word Wallet Account

Use this backend-only request when a client knows a TON address but does not know the BIP39 V5R1 `account_index`:

```bash
curl -X POST https://api.fragment-api.space/api/v1/wallet/resolve \
  -H 'Content-Type: application/json' \
  -d '{
    "seed": "your_wallet_seed_base64",
    "wallet_address": "your_public_ton_wallet_address"
  }'
```

You may send `account_index` instead of `wallet_address`, or send both to verify the pairing. Do not use query parameters: seeds must not appear in URLs or access logs.

```json
{
  "success": true,
  "data": {
    "wallet_address": "resolved_public_ton_address",
    "wallet_version": "v5r1",
    "seed_format": "bip39-12",
    "account_index": 3
  }
}
```

All purchase endpoints accept these optional fields too. With a 12-word seed, omitting both selects index `0`.

## Buy Stars

`amount` must be an integer from `50` to `1,000,000`. Smaller requests are rejected before payment.

```bash
curl -X POST https://api.fragment-api.space/api/v1/stars/buy \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "@telegram_user",
    "amount": 100,
    "seed": "your_wallet_seed_base64",
    "account_index": 3,
    "payment_method": "ton"
  }'
```

An accepted request contains `data.request_id`. Persist it with your order ID and poll until a final status (`completed`, `failed`, or `timeout`):

```bash
curl https://api.fragment-api.space/api/v1/queue/REQUEST_ID
```

Use the actual ID from the response, not the placeholder above. `queued` and `processing` are not completion. A timeout or failed status does not by itself establish whether funds moved; inspect error details and wallet history before another purchase. Do not automatically repeat the POST if the response is lost.

## Buy Stars with KYC

Add `fragment_cookies` to use KYC mode. KYC API commission is `0%`.
Cookies must be a Base64-encoded JSON object or cookie array. `fragment_local_storage`, when supplied, must be a Base64-encoded JSON object.

```json
{
  "username": "@telegram_user",
  "amount": 100,
  "seed": "your_wallet_seed_base64",
  "fragment_cookies": "fragment_cookies_base64",
  "payment_method": "ton",
  "max_cost": "2.96"
}
```

`max_cost` is optional and only valid for KYC Stars. Send a positive decimal string: TON supports up to 9 fractional digits; USDT on TON supports up to 6. The actual Fragment amount is paid, not the full limit. Network costs are separate. When omitted, the original quote stays the limit.

If checkout exceeds the limit, the API does not sign that payment and the queue reports `FRAGMENT_PRICE_CHANGED`. Read the existing request and get a fresh quote before starting a new one. In the legacy two-step TON flow, set the limit on `POST /api/v1/stars/pay`, not on `/stars/create`. Use only an API deployment that supports this field.

## Buy Stars with USDT on TON

```json
{
  "username": "@telegram_user",
  "amount": 100,
  "seed": "your_wallet_seed_base64",
  "payment_method": "usdt_ton"
}
```

## Buy Premium

```bash
curl -X POST https://api.fragment-api.space/api/v1/premium/buy \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "@telegram_user",
    "duration": 3,
    "seed": "your_wallet_seed_base64",
    "payment_method": "ton"
  }'
```

Valid `duration` values are `3`, `6`, and `12`.

Premium currently returns a final result directly; do not assume it has the Stars polling contract. No-KYC Premium uses TON; KYC can use USDT on TON where supported. [Premium guide](telegram-premium-api.md).

## Other Useful Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/health` | API availability check |
| `GET` | `/api/v1/prices` | TON and USDT-on-TON prices |
| `GET` | `/api/v1/commission/rates` | Commission rates |
| `POST` | `/api/v1/premium/check-eligibility` | Premium eligibility check |
| `POST` | `/api/v1/wallet/resolve` | Resolve or verify `wallet_address` / `account_index` |

## Language Examples

- Node.js: [examples/javascript_fetch.js](../examples/javascript_fetch.js)
- Wallet resolution in Node.js: [examples/resolve_wallet_index.js](../examples/resolve_wallet_index.js)
- Wallet resolution in Python REST: [examples/resolve_wallet_index_rest.py](../examples/resolve_wallet_index_rest.py)
- PHP: [examples/php_curl.php](../examples/php_curl.php)
- Go: [examples/go_net_http.go](../examples/go_net_http.go)

[Python walkthrough](python.md) · [Node.js walkthrough](nodejs.md) · [Errors](errors.md) · [Back to README](../README.md)
