# Fragment Stars API Integration Instructions for Claude

Use these instructions when integrating Fragment Stars API into a Telegram shop, bot, backend, worker, or direct REST client.

## Ground Truth

- Docs: https://wemakecode.ru/fragment-api
- Production API endpoint: `https://fragment-api.ydns.eu:8443`
- Example shop: https://github.com/bbbuilt/tg_stars_premium_shop
- Python SDK: `pip install fragment-stars-api`
- Normal client API calls do **not** require issued API tokens, `X-API-Key`, JWT, OAuth, or `Authorization` headers.
- Only `/admin` endpoints use `X-Admin-Key`; never request this for normal customer integrations.
- KYC mode is permanently free: `0%` API commission when the client provides their own Fragment cookies.
- If the user wants to verify current rates, call `GET /api/v1/commission/rates` or SDK `get_rates()`.

## Integration Approach

Prefer Python SDK for Python projects:

```python
from fragment_api import FragmentAPIClient

client = FragmentAPIClient("https://fragment-api.ydns.eu:8443")
rates = client.get_rates()
```

Use REST directly for other languages.

## Security Constraints

- Keep wallet seed, Fragment cookies, and Fragment localStorage only on the backend/server side.
- Never put secrets in frontend/browser code.
- Never log seeds, cookies, or localStorage.
- Do not invent API-token issuance or API-key authentication for client endpoints.
- Use HTTPS only.

## Purchase Modes

KYC mode:

- Send `fragment_cookies` and optionally `fragment_local_storage` from the user's own Fragment session.
- Purchases happen through the user's Fragment account.
- API commission is `0%` forever.

Non-KYC mode:

- Do not send Fragment cookies.
- API uses owner cookies.
- Commission is configured server-side; read rates from `/api/v1/commission/rates`.

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

## Queue and Status

Stars purchases are queued. After a `202` response with `request_id`, poll:

```text
GET https://fragment-api.ydns.eu:8443/api/v1/queue/{request_id}
```

Stop polling on `completed`, `failed`, or timeout. Premium usually returns the final result directly.

## Duplicate Purchase Prevention

Never blindly retry after any of these events:

- transaction hash returned,
- transaction signing started,
- transaction was sent,
- network error happened after signing/sending,
- order state is unknown.

Instead, check queue status, wallet transactions, saved shop order state, or ask an operator. Blind retries can create duplicate Stars/Premium purchases.

## Build Checklist

1. Add config: `FRAGMENT_API_URL=https://fragment-api.ydns.eu:8443`.
2. Implement a backend-only API wrapper: buy stars, buy premium, get rates, poll queue.
3. Add shop-level idempotency: one paid customer order must map to one Fragment purchase attempt.
4. Store secrets in environment variables or encrypted storage, never in git.
5. Sanitize usernames and amounts before calling the API.
6. Show useful error messages to admins without exposing secrets.
7. For KYC, guide users through Fragment cookie extraction and tell them cookies can expire.

## Common Errors

- `USER_NOT_FOUND`: ask user to check Telegram username.
- `INVALID_SEED`: seed is missing, malformed, or unsupported.
- `INVALID_COOKIES`: Fragment session cookies are invalid or expired.
- `INSUFFICIENT_BALANCE`: wallet lacks TON.
- `RATE_LIMIT_EXCEEDED`: slow down requests.
- `FRAGMENT_ERROR` / 5xx: external service issue. Do not retry if transaction may already have been sent.

## Hard Rules

- No `X-API-Key` for normal client calls.
- No frontend secret handling.
- No blind retries after possible transaction send.
- No real seeds/cookies in examples, tests, screenshots, commits, or logs.
