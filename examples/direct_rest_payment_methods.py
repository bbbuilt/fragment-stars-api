"""
Example: direct REST calls without the Python SDK.

This shows the exact JSON body for all common Stars modes.
"""

import requests

API_URL = "https://api-fragment.duckdns.org"
SEED = "your_wallet_seed_base64"
COOKIES = "your_fragment_cookies_base64"


def buy_stars(payload: dict) -> dict:
    response = requests.post(f"{API_URL}/api/v1/stars/buy", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


# Non-KYC + TON: omit fragment_cookies, default payment_method is ton.
print(buy_stars({
    "username": "@telegram_username",
    "amount": 100,
    "seed": SEED,
    "payment_method": "ton",
}))

# Non-KYC + USDT-on-TON: Stars base price in USDT-on-TON. API commission
# accumulates in TON and is collected only when the balance reaches 1 TON.
print(buy_stars({
    "username": "@telegram_username",
    "amount": 100,
    "seed": SEED,
    "payment_method": "usdt_ton",
}))

# KYC + TON: provide Fragment cookies, API commission is 0%.
print(buy_stars({
    "username": "@telegram_username",
    "amount": 100,
    "seed": SEED,
    "fragment_cookies": COOKIES,
    "payment_method": "ton",
}))

# KYC + USDT-on-TON: provide Fragment cookies and choose USDT.
print(buy_stars({
    "username": "@telegram_username",
    "amount": 100,
    "seed": SEED,
    "fragment_cookies": COOKIES,
    "payment_method": "usdt_ton",
}))
