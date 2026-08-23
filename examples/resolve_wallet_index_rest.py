"""Resolve a wallet index with direct REST. Keep the seed on the backend."""

import os

import requests

api_url = os.getenv("FRAGMENT_API_BASE_URL", "https://api.fragment-api.space")
response = requests.post(
    f"{api_url}/api/v1/wallet/resolve",
    json={
        "seed": os.environ["FRAGMENT_WALLET_SEED"],
        "wallet_address": os.environ["FRAGMENT_WALLET_ADDRESS"],
    },
    timeout=30,
)
response.raise_for_status()
wallet = response.json()["data"]
print({key: wallet[key] for key in ("wallet_address", "wallet_version", "account_index")})

# Resolution is free and performs no purchase. The paid step is opt-in.
if os.getenv("RUN_PURCHASE", "").lower() == "true":
    purchase = requests.post(
        f"{api_url}/api/v1/stars/buy",
        json={
            "username": os.environ["TELEGRAM_RECIPIENT"],
            "amount": int(os.getenv("STARS_AMOUNT", "50")),
            "seed": os.environ["FRAGMENT_WALLET_SEED"],
            "account_index": wallet["account_index"],
        },
        timeout=30,
    )
    purchase.raise_for_status()
    print(purchase.json())
else:
    print("Purchase skipped. Set RUN_PURCHASE=true to submit the Stars request.")
