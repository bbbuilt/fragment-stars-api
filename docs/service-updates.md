# Public Service Updates

Client-visible updates to the hosted API. This is separate from the [Python SDK changelog](../CHANGELOG.md): a service update does not necessarily require a new package version. No internal deployment or administrative details are published here.

## 2026-10-04 - Fragment Page Recovery

- Bounded recovery for temporary Fragment page errors before purchase creation/signing.
- Missing post-reload API state is classified as `TEMPORARY_FRAGMENT_CONNECTION_ERROR` rather than a generic failure.
- This does not authorize blind resubmission of a purchase; always inspect uncertain transaction outcomes.

## 2026-09-24 - Session Recovery

- Improved recovery from temporary recipient-lookup errors before checkout.
- Wallet authentication has bounded recovery without assuming that an unverified wallet was accepted.
- Additional Fragment verification remains a user action, not something the API bypasses.

## 2026-08-24 - Multi-Account Wallet Selection

- Added 12-word BIP39 V5R1 account selection with `account_index` and `wallet_address`.
- Added `POST /api/v1/wallet/resolve`; Python SDK support is available in 2.1.6.

## 2026-08-16 - Canonical Endpoint

- Primary endpoint: `https://api.fragment-api.space`.
- Documentation: [fragment-api.space](https://fragment-api.space).
- Previously documented endpoints remain compatible.

## Current Fee Policy

KYC API commission is 0% permanently; no-KYC API commission is 0.25%. Purchase prices and blockchain fees are separate. Check live rates with `GET /api/v1/commission/rates`.

[Back to README](../README.md)
