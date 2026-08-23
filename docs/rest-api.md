# Direct REST API

Use direct REST if your backend is not Python or you do not want to use the SDK. Client endpoints do not require an API key.

Base URL:

```text
https://api.fragment-api.space
```

The legacy `https://api-fragment.duckdns.org` and `https://fragment-api.ydns.eu:8443` endpoints remain compatible.

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

The response contains `data.request_id`. Poll it until completed or failed:

```bash
curl https://api.fragment-api.space/api/v1/queue/REQUEST_ID
```

## Buy Stars with KYC

Add `fragment_cookies` to use KYC mode. KYC API commission is `0%`.
Cookies must be a Base64-encoded JSON object or cookie array. `fragment_local_storage`, when supplied, must be a Base64-encoded JSON object.

```json
{
  "username": "@telegram_user",
  "amount": 100,
  "seed": "your_wallet_seed_base64",
  "fragment_cookies": "fragment_cookies_base64",
  "payment_method": "ton"
}
```

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
