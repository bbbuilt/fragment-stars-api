# KYC vs No-KYC Mode

Fragment Stars API supports two integration modes. Existing clients stay compatible because `payment_method` defaults to `ton` and cookies are optional.

## Comparison

| Mode | Requires Fragment cookies | API commission | Payment methods | Best for |
|------|---------------------------|----------------|-----------------|----------|
| KYC | Yes | `0%` forever | TON, USDT on TON where supported | Lowest cost, advanced users, own Fragment account |
| No-KYC | No | `0.25%` | TON, USDT on TON for Stars | Fast onboarding, shops that do not want user cookies |

## KYC Mode

Use KYC mode when the customer or shop owner can provide Fragment cookies from a Fragment account with a connected TON wallet.

Required cookies:

- `stel_token`
- `stel_ssid`
- `stel_ton_token`
- `stel_dt`

KYC mode is permanently free from API commission. You can still call `GET /api/v1/commission/rates` or `client.get_rates()` before purchase if you want to display current rates.

## No-KYC Mode

Use no-KYC mode when you want the simplest integration and do not want to collect Fragment cookies from users.

For Stars purchases:

- `payment_method="ton"` uses TON for the Stars price and API commission.
- `payment_method="usdt_ton"` uses USDT on TON for the Stars base price and TON for the API commission.

No-KYC uses a `0.25%` API commission and requires enough wallet balance for the selected payment method plus TON gas. The rate is public and can be verified through `GET /api/v1/commission/rates`.

### Accumulated commission

The API accumulates no-KYC commission per TON wallet and collects the full balance when it reaches `1 TON`. This avoids a small TON commission transaction and extra gas on every order.

- Below `1 TON`, a successful order adds its commission to `commission_balance_ton` without a separate commission transfer.
- For TON purchases that reach the threshold, the accumulated commission is included in the main no-KYC prepayment.
- For USDT-on-TON Stars purchases that reach the threshold, the Stars base price remains in USDT and the accumulated commission is collected with one TON transaction.
- KYC purchases never add commission debt and remain `0%` forever.
- If a collection transaction has an uncertain relay status, the API blocks another no-KYC purchase from that wallet instead of risking a duplicate transfer.

The `1 TON` threshold is a collection threshold, not an extra fee. The commission rate remains `0.25%`.

## Safety Rule

If a request returns an uncertain TON transaction status, check the wallet or TON explorer before retrying. A blind retry can duplicate a purchase.
