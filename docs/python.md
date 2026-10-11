# Telegram Stars API with Python

Use `fragment-stars-api` from a bot server, aiogram worker, FastAPI application, or another Python backend. The SDK defaults to `https://api.fragment-api.space`; no issued API key is required.

## Start Without Spending Funds

```bash
pip install fragment-stars-api
```

```python
from fragment_api import FragmentAPIClient

with FragmentAPIClient() as client:
    print(client.get_prices())
    print(client.get_rates())
```

These calls need no wallet or Fragment session. `rate_with_kyc` and `rate_no_kyc` are percentages, while their `_decimal` counterparts are calculation factors.

## Submit One Stars Order

Purchase calls transmit your seed to the hosted API for signing. Use a dedicated operating wallet, HTTPS, and backend environment variables; read the [security boundaries](../SECURITY.md) first. The following code spends funds once supplied with valid credentials and a real recipient.

```python
import os
from fragment_api import FragmentAPIClient

with FragmentAPIClient() as client:
    accepted = client.buy_stars(
        username="@telegram_user",
        amount=100,
        seed=os.environ["FRAGMENT_WALLET_SEED"],
        payment_method="ton",
        wait=False,
    )
    print(accepted.request_id)  # Persist against your own order_id.
```

The seed must be a supported value encoded as Base64. Stars amounts start at 50. Omitting cookies selects no-KYC; add `cookies=os.environ["FRAGMENT_COOKIES"]` for KYC. For USDT on TON, change `payment_method` to `usdt_ton`. [Four payment/mode combinations](../examples/payment_methods.py).

Persist your order intent before sending the purchase, then persist the returned `request_id`. A connection error before the ID arrives does not prove that the API did not receive the request. Do not automatically resubmit it.

## Read the Existing Request

This check does not submit a new purchase:

```python
import os
from fragment_api import FragmentAPIClient, QueueStatus

with FragmentAPIClient() as client:
    status = client.get_status(os.environ["FRAGMENT_REQUEST_ID"])
    if status.status == QueueStatus.COMPLETED:
        print(status.result)
    elif status.status in (QueueStatus.FAILED, QueueStatus.TIMEOUT):
        print(status.error)
    else:
        print("Pending:", status.status.value)
```

Poll at a bounded interval, such as every 2-5 seconds, rather than a busy loop. `queued` and `processing` are not completion. A failed or timed-out request needs its error details checked before any new purchase, especially when a transaction may already have been signed or sent.

### Recover a Polling Failure (SDK 2.1.7+)

`QueueTimeoutError.request_id` preserves the existing request for both a server timeout and a local polling deadline. API and Requests transport exceptions raised during SDK polling also retain `request_id`, without changing their exception type. Read that existing request; do not submit another purchase automatically. If the initial submission failed before an ID was received, the SDK cannot invent one or prove that no payment happened.

`RateLimitError.retry_after` contains the number of seconds indicated by a valid HTTP `Retry-After` header, or `None` when absent/invalid. This is advisory information only: the SDK does not sleep and repeat the purchase for you.

`buy_stars(wait=True)` is convenient for scripts: the SDK polls and returns `PurchaseResult`. For a durable shop, `wait=False` makes it easier to save the API ID before waiting. In an async aiogram handler, move the synchronous SDK call into your job worker or a thread rather than blocking the event loop. A cancelled handler or thread wait does not cancel the remote purchase.

## Wallet Accounts and Premium

Use `resolve_wallet(seed=..., wallet_address=...)` if a 12-word V5R1 wallet's account index is unknown, then pass the returned index to purchase methods. Resolution transmits the seed too; it is not a frontend operation. [Resolver example](../examples/resolve_wallet_index.py).

Premium uses `buy_premium()` and currently returns a final result directly. Do not assume it has the Stars queue contract. [Premium integration](telegram-premium-api.md).

## Next Steps

- [Minimal shop and production checklist](telegram-stars-shop.md)
- [Errors and uncertain-payment handling](errors.md)
- [REST reference](rest-api.md)
- [KYC cookies guide](../COOKIES_GUIDE.md)

[Back to README](../README.md)
