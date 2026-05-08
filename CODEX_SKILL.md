---
name: fragment-stars-api-integration
description: Use this skill when integrating Fragment Stars API for Telegram Stars or Premium purchases, building a shop/bot/backend around it, debugging API calls, or writing docs/examples for clients. It prevents invented API-key auth, unsafe frontend seed handling, duplicate purchases, and retry bugs.
---

# Fragment Stars API Integration Skill for Codex

Use this skill when the user asks to integrate Fragment Stars API, add Telegram Stars/Premium purchases, wire a shop bot, or debug direct API/SDK usage.

## Canonical Facts

- Documentation site: https://wemakecode.ru/fragment-api
- Production API endpoint: `https://fragment-api.ydns.eu:8443`
- Example shop repository: https://github.com/bbbuilt/tg_stars_premium_shop
- Python package: `fragment-stars-api`
- Client API does **not** require issued API tokens or `X-API-Key`.
- Admin routes are separate and use `X-Admin-Key`; never ask normal API clients for this.
- KYC mode is free forever: `0%` API commission when the client provides their own Fragment cookies.
- Clients may call `GET /api/v1/commission/rates` or SDK `get_rates()` if they want to verify rates before use.

## Integration Decision

Prefer the Python SDK for Python bots/backends:

```bash
pip install fragment-stars-api
```

```python
from fragment_api import FragmentAPIClient

client = FragmentAPIClient("https://fragment-api.ydns.eu:8443")
rates = client.get_rates()
```

Use direct REST for non-Python stacks.

## Security Rules

- Never put wallet seed, Fragment cookies, or Fragment localStorage in browser/frontend code.
- Send purchase requests only from a trusted backend, worker, or bot server.
- Treat `seed`, `fragment_cookies`, and `fragment_local_storage` as secrets.
- Do not log seeds/cookies/localStorage.
- Do not invent API-key setup, token issuance, OAuth, JWT, or `Authorization` headers for client API calls.
- Use HTTPS endpoint only.

## Purchase Modes

KYC mode:

- Client provides `fragment_cookies` and optionally `fragment_local_storage` from their own Fragment session.
- Purchase is made through the client Fragment account.
- API commission is `0%` permanently.

Non-KYC mode:

- Client does not provide Fragment cookies.
- API uses server owner cookies.
- Commission is configured by the service; check `/api/v1/commission/rates`.

## Direct REST Examples

Buy Stars:

```bash
curl -X POST https://fragment-api.ydns.eu:8443/api/v1/stars/buy \
  -H "Content-Type: application/json" \
  -d '{
    "username": "@username",
    "amount": 50,
    "seed": "BASE64_WALLET_SEED",
    "fragment_cookies": "BASE64_FRAGMENT_COOKIES"
  }'
```

Buy Premium:

```bash
curl -X POST https://fragment-api.ydns.eu:8443/api/v1/premium/buy \
  -H "Content-Type: application/json" \
  -d '{
    "username": "@username",
    "duration": 3,
    "seed": "BASE64_WALLET_SEED",
    "fragment_cookies": "BASE64_FRAGMENT_COOKIES"
  }'
```

Check rates:

```bash
curl https://fragment-api.ydns.eu:8443/api/v1/commission/rates
```

## Queue Handling

Stars purchases are queued. If `POST /api/v1/stars/buy` returns `202` with `request_id`, poll:

```bash
GET https://fragment-api.ydns.eu:8443/api/v1/queue/{request_id}
```

Premium usually returns the final result directly, but handle API errors consistently.

## Critical Retry Rule

Do **not** blindly retry purchase requests after:

- a transaction hash was returned,
- the API says transaction was sent,
- the network failed after transaction signing/sending,
- the request status is unknown.

Instead, check queue status, transaction history, wallet activity, or ask for manual confirmation. Blind retry can buy Stars/Premium twice.

## Implementation Checklist

1. Store endpoint in config: `FRAGMENT_API_URL=https://fragment-api.ydns.eu:8443`.
2. Keep secrets server-side only.
3. Add a purchase service wrapper with clear methods: `buy_stars`, `buy_premium`, `get_rates`, `get_queue_status`.
4. Normalize Telegram usernames: accept with or without `@`, but send a valid username according to the API/SDK you use.
5. Poll Stars queue until `completed`, `failed`, or timeout.
6. Surface API error messages to admins/operators without leaking secrets.
7. Add idempotency at the shop/bot level: do not process the same paid order twice.
8. For KYC onboarding, link users to the cookie guide and validate cookies before first purchase when possible.

## Common Error Guidance

- `USER_NOT_FOUND`: username not found by Fragment/Telegram. Ask user to verify username.
- `INVALID_SEED`: seed is missing, not base64, or not a supported wallet seed format.
- `INVALID_COOKIES`: Fragment cookies/localStorage are malformed or expired.
- `INSUFFICIENT_BALANCE`: wallet lacks TON for purchase plus gas.
- `RATE_LIMIT_EXCEEDED`: slow down requests; API rate limits by client/IP.
- `FRAGMENT_ERROR` or 5xx: external Fragment/TON provider issue; do not retry after possible transaction send.

## What Not To Do

- Do not add `X-API-Key` to client requests.
- Do not ask the API owner to issue tokens for normal clients.
- Do not expose seeds/cookies to frontend JavaScript.
- Do not auto-repeat a failed purchase if the failure happened after transaction capture/sign/send.
- Do not hardcode test seeds, real cookies, or wallet secrets into git.
