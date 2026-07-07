# Build a Telegram Stars Shop

This guide shows the shortest safe backend flow for a Telegram Stars shop using Fragment Stars API.

## Backend Flow

1. Your bot or web checkout receives `username` and `amount`.
2. Your backend validates the order and keeps wallet secrets server-side.
3. Your backend calls `POST /api/v1/stars/buy` or `FragmentAPIClient.buy_stars()`.
4. The API creates a queued request and processes the Fragment purchase.
5. Your backend returns success or a clear failure message to the customer.

Never put wallet seed phrases, Fragment cookies, or localStorage in frontend code.

## Minimal Python Backend

Use the copy-paste example in [examples/shop_minimal.py](../examples/shop_minimal.py):

```bash
pip install fastapi uvicorn fragment-stars-api
export FRAGMENT_WALLET_SEED="base64_seed_phrase"
uvicorn examples.shop_minimal:app --host 0.0.0.0 --port 8000
```

Test it locally:

```bash
curl -X POST http://127.0.0.1:8000/buy-stars \
  -H 'Content-Type: application/json' \
  -d '{"username":"@telegram_user","amount":100}'
```

## Production Checklist

- Store `FRAGMENT_WALLET_SEED` in backend environment variables.
- Keep `FRAGMENT_COOKIES` backend-only if you use KYC mode.
- Normalize usernames to `@telegram_user` before direct REST calls.
- Show users a pending status while queue processing is running.
- Do not blindly retry after an uncertain TON transaction.
- Log your own `order_id` and the API `request_id` together.
- Ask customers to retry with a new request only after a clear failed response.

## Recommended Shop UX

- Show exact Stars amount and recipient before purchase.
- Show payment method: TON or USDT on TON.
- Show that KYC mode has `0%` API commission when cookies are used.
- Show a clear support link with `order_id` and `request_id`.

## Full Example Shop

A larger Telegram shop example is available here:

https://github.com/bbbuilt/tg_stars_premium_shop
