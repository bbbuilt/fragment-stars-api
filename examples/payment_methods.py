"""
Example: KYC / Non-KYC and TON / USDT-on-TON payment methods.

Rules:
- payment_method is optional; default is "ton".
- KYC mode is enabled when you pass Fragment cookies. API commission is 0%.
- Non-KYC mode is used when cookies are omitted.
- Non-KYC Stars supports "ton" and "usdt_ton".
- Non-KYC Premium currently uses TON only.
"""

from fragment_api import FragmentAPIClient

API_URL = "https://fragment-api.ydns.eu:8443"
client = FragmentAPIClient(API_URL)

SEED = "your_wallet_seed_base64"
COOKIES = "your_fragment_cookies_base64"  # only for KYC mode
USERNAME = "telegram_username"
AMOUNT = 100

# Optional: show live TON and USDT-on-TON prices before checkout.
prices = client.get_prices()
print("Current prices:")
print("  Stars TON:", prices["stars"]["price_per_star_ton"])
print("  Stars USDT-on-TON:", prices["stars"].get("price_per_star_usdt_ton"))

# 1. Non-KYC + TON: no cookies, default payment method.
no_kyc_ton = client.buy_stars(
    username=USERNAME,
    amount=AMOUNT,
    seed=SEED,
    payment_method="ton",  # optional, shown explicitly for clarity
)
print("Non-KYC TON:", no_kyc_ton.success, no_kyc_ton.transaction_id)

# 2. Non-KYC + USDT-on-TON: no cookies.
# The Stars base price is paid in USDT-on-TON; API commission is paid in TON.
no_kyc_usdt = client.buy_stars(
    username=USERNAME,
    amount=AMOUNT,
    seed=SEED,
    payment_method="usdt_ton",
)
print("Non-KYC USDT-on-TON:", no_kyc_usdt.success, no_kyc_usdt.transaction_id)

# 3. KYC + TON: pass Fragment cookies. API commission is 0%.
kyc_ton = client.buy_stars(
    username=USERNAME,
    amount=AMOUNT,
    seed=SEED,
    cookies=COOKIES,
    payment_method="ton",
)
print("KYC TON:", kyc_ton.success, kyc_ton.transaction_id)

# 4. KYC + USDT-on-TON: pass Fragment cookies and choose USDT.
kyc_usdt = client.buy_stars(
    username=USERNAME,
    amount=AMOUNT,
    seed=SEED,
    cookies=COOKIES,
    payment_method="usdt_ton",
)
print("KYC USDT-on-TON:", kyc_usdt.success, kyc_usdt.transaction_id)
