# Security Policy

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
