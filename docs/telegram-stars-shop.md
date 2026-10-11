# Build a Telegram Stars Shop

Use Fragment Stars API to connect a Telegram bot or web checkout to Stars purchases. This guide describes a minimal integration, not a complete production payment system. Start with [Python](python.md), [Node.js](nodejs.md), or [direct REST](rest-api.md).

## Backend Flow

1. Your bot or web checkout receives `username` and `amount`.
2. Your backend validates the order and keeps wallet secrets server-side.
3. Your backend calls `POST /api/v1/stars/buy` or `FragmentAPIClient.buy_stars()`.
4. The API creates a queued request and processes the Fragment purchase.
5. Your backend returns success or a clear failure message to the customer.

Never put wallet seed phrases, Fragment cookies, or localStorage in frontend code.

Purchase requests send those credentials to the hosted API. Use a dedicated operating wallet and read [SECURITY.md](../SECURITY.md).

## Minimal Python Backend

Use the copy-paste example in [examples/shop_minimal.py](../examples/shop_minimal.py):

```bash
pip install fastapi uvicorn fragment-stars-api
export FRAGMENT_WALLET_SEED="base64_seed_phrase"
uvicorn examples.shop_minimal:app --host 127.0.0.1 --port 8000
```

This local demo has no customer authentication or payment verification. Do not expose its purchase route publicly: a caller could spend your wallet balance. The following request performs a real purchase when valid credentials and a real recipient are configured:

```bash
curl -X POST http://127.0.0.1:8000/buy-stars \
  -H 'Content-Type: application/json' \
  -d '{"username":"@telegram_user","amount":100}'
```

## Production Checklist

- Store `FRAGMENT_WALLET_SEED` in backend environment variables.
- Authenticate callers and verify customer payment before submitting a purchase. The upstream API needs no issued API key, but your shop still needs access control.
- Persist your own order ID and deduplication state before submission. Do not assume a client-generated key is enforced by an undocumented API header.
- Keep `FRAGMENT_COOKIES` backend-only if you use KYC mode.
- Normalize usernames to `@telegram_user` before direct REST calls.
- Show users a pending status while queue processing is running.
- Do not blindly retry after an uncertain TON transaction.
- Log your own `order_id` and the API `request_id` together.
- On failure, check whether a payment was sent or a refund is pending before allowing another purchase; a failed response alone is not permission to charge again.

## Recommended Shop UX

- Show exact Stars amount and recipient before purchase.
- Show payment method: TON or USDT on TON.
- Show that KYC mode has `0%` API commission when cookies are used.
- Show a clear support link with `order_id` and `request_id`.

## Full Example Shop

A larger Telegram shop example is available here:

[bbbuilt/tg_stars_premium_shop](https://github.com/bbbuilt/tg_stars_premium_shop)

## Estimate Your Costs

Read `GET /api/v1/prices` and `GET /api/v1/commission/rates` before checkout. Your retail price, Fragment's price, network costs and API commission are different amounts. Do not advertise the API's 0% KYC commission as free Stars.

Keep a user-visible pending state until the API reports completion. For customer support, retain the shop order ID, API request ID and sanitized final result, never the seed or cookies.

[KYC/no-KYC comparison](no-kyc-vs-kyc.md) · [Premium integration](telegram-premium-api.md) · [Back to README](../README.md)
