"""Resolve a 12-word BIP39 V5R1 account index with the Python SDK."""

import os

from fragment_api import FragmentAPIClient

seed = os.environ["FRAGMENT_WALLET_SEED"]
wallet_address = os.environ["FRAGMENT_WALLET_ADDRESS"]
client = FragmentAPIClient()

wallet = client.resolve_wallet(
    seed=seed,
    wallet_address=wallet_address,
)

print(f"wallet_address={wallet.wallet_address}")
print(f"wallet_version={wallet.wallet_version}")
print(f"account_index={wallet.account_index}")

# Resolution is free and performs no purchase. The paid step is opt-in.
if os.getenv("RUN_PURCHASE", "").lower() == "true":
    result = client.buy_stars(
        username=os.environ["TELEGRAM_RECIPIENT"],
        amount=int(os.getenv("STARS_AMOUNT", "50")),
        seed=seed,
        account_index=wallet.account_index,
    )
    print(result)
else:
    print("Purchase skipped. Set RUN_PURCHASE=true to use this account for a Stars purchase.")
