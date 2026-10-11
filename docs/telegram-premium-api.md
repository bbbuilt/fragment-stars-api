# Telegram Premium API: Python and REST

Gift 3, 6, or 12 months of Telegram Premium from a backend using Fragment Stars API. This is an independent integration service, not an official Telegram or Fragment API. The production endpoint is `https://api.fragment-api.space`.

## Check Price and Recipient

Read current prices before checkout, without providing a seed:

```bash
curl https://api.fragment-api.space/api/v1/prices
```

The `premium` section contains `3_months`, `6_months` and `12_months` prices. Check recipient eligibility separately:

```bash
curl -X POST https://api.fragment-api.space/api/v1/premium/check-eligibility \
  -H 'Content-Type: application/json' \
  -d '{"username":"@telegram_user"}'
```

An eligibility check is not a price reservation or purchase guarantee. The recipient's state and Fragment availability can change before checkout. Read the returned reason when gifting is unavailable.

## Python Purchase

The following operation spends funds and sends your seed to the hosted API for signing. Configure a dedicated operating wallet on your backend; read [SECURITY.md](../SECURITY.md). Replace `@telegram_user` with the actual user.

```python
import os
from fragment_api import FragmentAPIClient

with FragmentAPIClient(timeout=120) as client:
    result = client.buy_premium(
        username="@telegram_user",
        duration=3,
        seed=os.environ["FRAGMENT_WALLET_SEED"],
        payment_method="ton",
    )
    if result.success:
        print(result.transaction_hash or result.transaction_id)
    else:
        print(result.error)
```

This is no-KYC because cookies are omitted. Add `cookies=os.environ["FRAGMENT_COOKIES"]` to use your own Fragment session in KYC mode. Base64-encode supported seed/session values as documented; Base64 does not encrypt them.

## Direct REST Purchase

This illustrates the request shape; placeholders are not usable credentials:

```json
{
  "username": "@telegram_user",
  "duration": 3,
  "seed": "YOUR_BASE64_ENCODED_WALLET_SEED",
  "payment_method": "ton"
}
```

Send JSON with `POST /api/v1/premium/buy`. No API key or authorization header is needed. KYC adds `fragment_cookies` and, if needed, `fragment_local_storage`.

| Mode | API fee | Payment method |
|---|---|---|
| KYC | 0% forever | TON or USDT on TON where supported |
| No-KYC | 0.25% | TON |

Stars pricing, Premium pricing, blockchain costs and API commission are distinct. Check [mode and commission rules](no-kyc-vs-kyc.md) rather than hardcoding a TON quote.

## Completion and Errors

- The current Premium endpoint returns a final purchase result directly; unlike Stars, it does not normally return a queued request ID. The SDK retains support for older queued responses.
- `wait=False` does not turn the current Premium endpoint into an asynchronous job API.
- `API_BUSY` means another purchase is active; observe `Retry-After` and do not run a tight retry loop.
- `FRAGMENT_ADDITIONAL_VERIFICATION_REQUIRED` requires action on the same Fragment account. Do not bypass the check or silently switch payment mode.
- An HTTP timeout is not proof of non-payment. Check your wallet/history and contact support before repeating the purchase.

[Python guide](python.md) · [REST reference](rest-api.md) · [Errors](errors.md) · [Back to README](../README.md)
