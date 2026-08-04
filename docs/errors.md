# Errors and Troubleshooting

Use this page when a client receives a failed API response or a failed queue status.

## Where to Read the Error

Python SDK:

```python
from fragment_api import FragmentAPIError

try:
    result = client.buy_stars("@telegram_user", 100, seed="your_wallet_seed_base64")
except FragmentAPIError as exc:
    print(exc.error_code)
    print(exc.message)
```

Direct REST:

```json
{
  "success": false,
  "error": {
    "error_code": "VALIDATION_ERROR",
    "message": "Validation failed"
  }
}
```

Queue status can also include `data.error` and `data.error_details`.

## Common Error Codes

| Error | Cause | Client action |
|-------|-------|---------------|
| `VALIDATION_ERROR` | Bad JSON, username format, amount below 50, or payment method | Fix request body. Use `@telegram_user` and at least 50 Stars. |
| `INVALID_FRAGMENT_COOKIES` / `INVALID_FRAGMENT_LOCAL_STORAGE` | Base64 value does not decode to the required JSON container | Export session JSON again and Base64-encode the complete value. |
| `API_BUSY` | A Premium browser purchase is already active | Wait at least the `Retry-After` interval and submit manually; do not loop automatically. |
| `INVALID_SEED` / `INVALID_WALLET_SEED` | Seed is missing, malformed, or not base64 encoded | Re-encode the 24-word wallet seed on backend. |
| `INSUFFICIENT_BALANCE` / `INSUFFICIENT_WALLET_BALANCE` | Not enough TON, USDT on TON, or gas | Top up wallet and create a new request. |
| `USER_NOT_FOUND` / `TELEGRAM_USER_NOT_FOUND` | Fragment did not find recipient | Check username and create a new request. |
| `FRAGMENT_ADDITIONAL_VERIFICATION_REQUIRED` | Fragment wants account verification | Open Fragment manually and complete verification. |
| `TEMPORARY_FRAGMENT_CONNECTION_ERROR` | Temporary issue between API server and Fragment.com | Submit a new request later. Do not reuse old `request_id`. |
| `TEMPORARY_FRAGMENT_FORM_NOT_READY` | Fragment page/form did not become ready | Submit a new request later. |
| `TON_TRANSACTION_CONFIRMATION_UNCERTAIN` | Transaction state is uncertain | Check wallet/TON explorer before retrying. |

## Do Not Retry Blindly

If a transaction may have been signed or sent, check the wallet first. A blind retry can duplicate a Stars or Premium purchase.

Requests below 50 Stars are rejected before wallet initialization, invoice creation, or browser work. Do not round a customer order down below 50.

## What to Include in Support Requests

Safe to share:

- API `request_id`
- Your internal `order_id`
- Username and Stars amount
- Payment method
- Error code and message

Never share publicly:

- Wallet seed phrase
- Fragment cookies
- Private keys
- Full localStorage dumps
