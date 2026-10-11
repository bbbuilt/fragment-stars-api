# Telegram Stars API with Node.js

Use direct REST from Node.js or TypeScript server code. The endpoint is `https://api.fragment-api.space`; no Python dependency or API key is needed. Examples use built-in `fetch` (Node.js 18+ API; use a currently supported Node.js release for deployment).

## Read Prices First

```javascript
const response = await fetch("https://api.fragment-api.space/api/v1/prices");
if (!response.ok) throw new Error(`Price request failed: HTTP ${response.status}`);
console.log(await response.json());
```

Run this in an `.mjs` file or an ES-module project. It does not require a wallet and does not spend funds. API commission is available from `GET /api/v1/commission/rates`.

## Submit a Purchase from Your Backend

The following code makes a real purchase when valid credentials and a real recipient are provided. It sends the seed to the hosted API for signing; do not run it in a web page, Telegram Mini App, or public frontend bundle. Use a limited-balance operating wallet and follow [SECURITY.md](../SECURITY.md).

```javascript
const baseUrl = "https://api.fragment-api.space";
const seed = process.env.FRAGMENT_WALLET_SEED;
if (!seed) throw new Error("Set FRAGMENT_WALLET_SEED on the backend");

const response = await fetch(`${baseUrl}/api/v1/stars/buy`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: "@telegram_user",
    amount: 100,
    seed,
    payment_method: "ton",
    ...(process.env.FRAGMENT_COOKIES
      ? { fragment_cookies: process.env.FRAGMENT_COOKIES }
      : {}),
  }),
});
const accepted = await response.json();
if (!response.ok || accepted.success === false) {
  throw new Error(accepted.error?.message || `HTTP ${response.status}`);
}
if (!accepted.data?.request_id) throw new Error("Missing request_id: reconcile before retrying");
console.log(accepted.data.request_id); // Save to your order database before polling.
```

Without `FRAGMENT_COOKIES` this is no-KYC. With valid Fragment cookies it is KYC. For Stars paid in USDT on TON, use `payment_method: "usdt_ton"`; TON is still required for gas and any due commission.

## Poll, Do Not Repurchase

```javascript
const requestId = process.env.FRAGMENT_REQUEST_ID;
if (!requestId) throw new Error("Set the existing FRAGMENT_REQUEST_ID");
const response = await fetch(
  `https://api.fragment-api.space/api/v1/queue/${encodeURIComponent(requestId)}`,
);
if (!response.ok) throw new Error(`Status request failed: HTTP ${response.status}`);
const status = await response.json();
console.log(status.data);
```

This is a separate snippet that reads an existing request. Use bounded polling with delays; only a final result confirms completion. Preserve the request ID on polling timeouts. Aborting `fetch` stops waiting locally, not the server's purchase. A network error or non-JSON purchase response must not trigger an automatic second POST.

The [runnable Node.js example](../examples/javascript_fetch.js) combines submission and polling. Add persistent order state, request timeouts, error handling and checkout access controls before deploying it as a shop. Never log request bodies containing secrets.

## Other Integrations

- [REST schemas and Premium example](rest-api.md)
- [KYC/no-KYC comparison](no-kyc-vs-kyc.md)
- [Wallet index resolution](../examples/resolve_wallet_index.js)
- [PHP](../examples/php_curl.php) / [Go](../examples/go_net_http.go)
- [Errors](errors.md)

[Back to README](../README.md)
