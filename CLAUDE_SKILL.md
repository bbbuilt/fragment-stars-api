# Fragment Stars API Integration Instructions for Claude

Use these instructions when integrating Fragment Stars API into a Telegram shop, bot, backend, worker, or direct REST client.

## Ground Truth

- Docs: https://fragment-api.space
- Production API endpoint: `https://api.fragment-api.space`
- Example shop: https://github.com/bbbuilt/tg_stars_premium_shop
- Python SDK: `pip install fragment-stars-api`
- Normal client API calls do **not** require issued API tokens, `X-API-Key`, JWT, OAuth, or `Authorization` headers.
- KYC mode is permanently free: `0%` API commission when the client provides their own Fragment cookies.
- Non-KYC mode has a `0.25%` API commission and does not require Fragment cookies.
- If the user wants to verify current rates, call `GET /api/v1/commission/rates` or SDK `get_rates()`.
- `payment_method` is optional and defaults to `ton`; supported values are `ton` and `usdt_ton`.
- For Non-KYC Stars with `payment_method="usdt_ton"`, Stars base cost is paid in USDT on TON and API commission is paid in TON.
- Non-KYC commission is accumulated per wallet and collected at `1 TON`; client code must not create its own commission transfer. TON orders fold collection into the main prepayment, while USDT-on-TON Stars uses one TON collection only at the threshold.
- Read `commission_balance_ton` from purchase responses when displaying the accumulated balance.

## Integration Approach

Prefer Python SDK for Python projects:

```python
from fragment_api import FragmentAPIClient

client = FragmentAPIClient()
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
- API commission is `0.25%`; read the live public value from `/api/v1/commission/rates`.

Payment methods:

- Default: omit `payment_method` or send `"ton"`.
- USDT on TON: send `"payment_method": "usdt_ton"`.
- KYC mode supports TON and USDT on TON with `0%` API commission.
- Non-KYC Stars supports TON and USDT on TON; Non-KYC Premium currently uses TON.
- Use `GET /api/v1/prices` before checkout to show `price_per_star_ton`, `price_per_star_usdt_ton`, and Premium `base_ton` / `base_usdt_ton`.

## Direct REST Examples

Buy Stars:

```bash
curl -X POST https://api.fragment-api.space/api/v1/stars/buy \
  -H "Content-Type: application/json" \
  -d '{
    "username": "@username",
    "amount": 50,
    "seed": "BASE64_WALLET_SEED",
    "fragment_cookies": "BASE64_FRAGMENT_COOKIES",
    "payment_method": "ton"
  }'
```

Buy Premium:

```bash
curl -X POST https://api.fragment-api.space/api/v1/premium/buy \
  -H "Content-Type: application/json" \
  -d '{
    "username": "@username",
    "duration": 3,
    "seed": "BASE64_WALLET_SEED",
    "fragment_cookies": "BASE64_FRAGMENT_COOKIES",
    "payment_method": "ton"
  }'
```

Check rates:

```bash
curl https://api.fragment-api.space/api/v1/commission/rates
```

## Queue and Status

Stars `amount` must be at least `50`. Reject smaller shop orders locally before calling the API.

Stars purchases are queued. After a `202` response with `request_id`, poll:

```text
GET https://api.fragment-api.space/api/v1/queue/{request_id}
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

1. Add config: `FRAGMENT_API_URL=https://api.fragment-api.space`.
2. Implement a backend-only API wrapper: buy stars, buy premium, get rates, poll queue.
3. Add shop-level idempotency: one paid customer order must map to one Fragment purchase attempt.
4. Store secrets in environment variables or encrypted storage, never in git.
5. Sanitize usernames and amounts before calling the API.
6. Show useful error messages to operators without exposing secrets.
7. For KYC, guide users through Fragment cookie extraction and tell them cookies can expire.

## Common Errors

- `USER_NOT_FOUND`: ask user to check Telegram username.
- `INVALID_SEED`: seed is missing, malformed, or unsupported.
- `INVALID_COOKIES`: Fragment session cookies are invalid or expired.
- `INVALID_FRAGMENT_COOKIES` / `INVALID_FRAGMENT_LOCAL_STORAGE`: session payload is not Base64-encoded JSON; fix it locally and do not retry unchanged.
- `API_BUSY`: one Premium browser purchase is active; respect `Retry-After` and never create an automatic retry loop.
- `INSUFFICIENT_BALANCE`: wallet lacks TON.
- `RATE_LIMIT_EXCEEDED`: slow down requests.
- `FRAGMENT_ERROR` / 5xx: external service issue. Do not retry if transaction may already have been sent.

## Hard Rules

- No `X-API-Key` for normal client calls.
- No frontend secret handling.
- No blind retries after possible transaction send.
- No real seeds/cookies in examples, tests, screenshots, commits, or logs.
