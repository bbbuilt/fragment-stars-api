"""
Minimal backend shop example: accept username/amount -> buy Telegram Stars.

Run:
  pip install fastapi uvicorn fragment-stars-api
  export FRAGMENT_WALLET_SEED="base64_seed_phrase"
  uvicorn shop_minimal:app --host 0.0.0.0 --port 8000

Test:
  curl -X POST http://127.0.0.1:8000/buy-stars \
    -H 'Content-Type: application/json' \
    -d '{"username":"@telegram_username","amount":100}'

No API key is required. Keep FRAGMENT_WALLET_SEED and FRAGMENT_COOKIES
on your backend only; never send them to a browser or mobile app.
"""

import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from fragment_api import FragmentAPIClient, FragmentAPIError

API_URL = os.getenv("FRAGMENT_API_BASE_URL", "https://api-fragment.duckdns.org")
WALLET_SEED = os.getenv("FRAGMENT_WALLET_SEED")
FRAGMENT_COOKIES = os.getenv("FRAGMENT_COOKIES")

app = FastAPI(title="Minimal Fragment Stars Shop")


class BuyStarsRequest(BaseModel):
    username: str = Field(..., examples=["@telegram_username"])
    amount: int = Field(..., ge=50, examples=[100])
    payment_method: Literal["ton", "usdt_ton"] = "ton"
    kyc: bool = False


@app.post("/buy-stars")
def buy_stars(request: BuyStarsRequest) -> dict:
    if not WALLET_SEED:
        raise HTTPException(
            status_code=500,
            detail="Set FRAGMENT_WALLET_SEED on the backend before accepting orders.",
        )

    username = request.username if request.username.startswith("@") else f"@{request.username}"
    cookies = FRAGMENT_COOKIES if request.kyc else None

    if request.kyc and not cookies:
        raise HTTPException(
            status_code=400,
            detail="KYC mode requires FRAGMENT_COOKIES on the backend.",
        )

    try:
        with FragmentAPIClient(API_URL, poll_timeout=300) as client:
            result = client.buy_stars(
                username=username,
                amount=request.amount,
                seed=WALLET_SEED,
                cookies=cookies,
                payment_method=request.payment_method,
            )
    except FragmentAPIError as exc:
        raise HTTPException(
            status_code=400,
            detail={"error_code": exc.error_code, "message": exc.message},
        ) from exc

    if not result.success:
        raise HTTPException(status_code=502, detail=result.error or "Purchase failed")

    return {
        "success": True,
        "username": result.username or username,
        "amount": result.amount,
        "payment_method": result.payment_method,
        "transaction_hash": result.transaction_hash or result.transaction_id,
        "invoice_id": result.invoice_id,
    }
