# Security Policy

## Hosted API Trust Boundary

This repository distributes a client SDK and examples for an independently operated hosted service. It is not an official Telegram or Fragment product, and it does not include the hosted backend.

Purchase requests send your wallet seed to the API service for transaction signing. KYC requests also send Fragment session cookies and optional localStorage. Backend-only integration means secrets stay out of your browser/client application; it does **not** mean they never leave your backend or that signing happens locally in this SDK.

- Use a dedicated operating wallet with a limited balance, not your main savings wallet.
- Only provide wallets and sessions you own or are authorized to operate.
- Base64 is encoding, not encryption. Use HTTPS and a trusted secret store.
- Do not submit seeds or cookies to analytics, error trackers, support chats, or screenshots.
- Validate the recipient and amount before purchase. Unknown transaction outcomes require reconciliation, not an automatic new purchase.
- Public price and commission requests need no seed or cookies and are the safest first integration test.

## Reporting a Vulnerability

If you found a security issue, do not open a public issue with secrets or exploit details.

Contact: [@makecodev](https://t.me/makecodev)

Please include:

- A concise description of the issue
- Impacted endpoint or SDK method
- Safe reproduction steps
- Sanitized logs without wallet seeds, Fragment cookies, private keys, or customer data

## Sensitive Data Rules

Fragment Stars API integrations must keep secrets backend-only:

- Wallet seed phrases
- Fragment cookies
- Fragment localStorage
- Private keys
- Customer payment data

Never embed these values in frontend JavaScript, mobile apps, public repositories, screenshots, or issue reports.
