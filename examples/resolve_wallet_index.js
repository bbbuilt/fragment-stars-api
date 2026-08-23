// Resolve a wallet index from a trusted Node.js backend, never from browser code.

const apiUrl = process.env.FRAGMENT_API_BASE_URL || "https://api.fragment-api.space";

const response = await fetch(`${apiUrl}/api/v1/wallet/resolve`, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({
    seed: process.env.FRAGMENT_WALLET_SEED,
    wallet_address: process.env.FRAGMENT_WALLET_ADDRESS,
  }),
});

if (!response.ok) {
  throw new Error(`Wallet resolution failed: ${response.status} ${await response.text()}`);
}

const wallet = (await response.json()).data;
console.log({
  wallet_address: wallet.wallet_address,
  wallet_version: wallet.wallet_version,
  account_index: wallet.account_index,
});

// Resolution is free and performs no purchase. The paid step is opt-in.
if ((process.env.RUN_PURCHASE || "").toLowerCase() === "true") {
  const purchase = await fetch(`${apiUrl}/api/v1/stars/buy`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      username: process.env.TELEGRAM_RECIPIENT,
      amount: Number(process.env.STARS_AMOUNT || "50"),
      seed: process.env.FRAGMENT_WALLET_SEED,
      account_index: wallet.account_index,
    }),
  });
  if (!purchase.ok) {
    throw new Error(`Purchase failed: ${purchase.status} ${await purchase.text()}`);
  }
  console.log(await purchase.json());
} else {
  console.log("Purchase skipped. Set RUN_PURCHASE=true to submit the Stars request.");
}
