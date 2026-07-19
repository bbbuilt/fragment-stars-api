# Changelog

All notable changes to this project will be documented in this file.

## [2.1.2] - 2026-07-19

### Changed
- KYC API commission remains permanently free at `0%`.
- No-KYC API commission is reduced to `0.25%` for new purchases.
- Updated SDK metadata, guides, AI integration skills, and examples with exact public rates.
- Added prominent lowest-cost positioning and refreshed repository preview artwork.

## [2.1.1] - 2026-05-31

### Fixed
- Updated documentation links to the primary site: `https://api-fragment.duckdns.org`.
- Added runnable KYC / Non-KYC examples for TON and USDT-on-TON payment methods.

## [2.1.0] - 2026-05-31

### Added
- Added optional `payment_method` argument to `buy_stars()` and `buy_premium()`.
- Supported values are `ton` and `usdt_ton`; default remains `ton` for backward compatibility.
- `PurchaseResult` now exposes `payment_method` and `cost_usdt_ton`.

### Changed
- Documentation now describes USDT-on-TON pricing and payment behavior.
- AI skill files now tell Codex/Claude not to invent auth tokens and how to use `payment_method`.

## [2.0.2] - 2026-05-08

### Fixed
- Updated `buy_premium()` for the current synchronous `/api/v1/premium/buy` API response.
- Fixed Premium eligibility checks so normal "not eligible" responses return a result instead of raising an exception.
- Updated queue status documentation and example for the current `queue_length` and `estimated_wait_seconds` fields.
- Fixed project URLs to point to `bbbuilt/fragment-stars-api`.

### Changed
- Added optional `local_storage` support to `buy_stars()` and `buy_premium()`.
- Expanded `PurchaseResult` fields for Premium responses, payment invoice data, and commission balance.

## [2.0.1] - 2026-01-24

### Added
- **Comprehensive Cookie Guide**: New detailed guides for getting Fragment cookies
  - `COOKIES_GUIDE.md` - English version with step-by-step instructions
  - `COOKIES_GUIDE.ru.md` - Russian version
  - Covers all 4 required cookies: `stel_token`, `stel_ssid`, `stel_ton_token`, `stel_dt`
  - Emphasizes critical importance of `stel_ton_token` for purchases
  - Includes troubleshooting section for common errors
  - Security best practices and FAQ

### Changed
- **Updated README.md**: Improved cookie documentation with link to detailed guide
- **Updated README.ru.md**: Improved Russian cookie documentation
- **Enhanced `with_kyc.py` example**: Added detailed comments about required cookies and error handling
- Clarified that `stel_ton_token` cookie is **required** for purchases (not optional)

### Fixed
- Documentation now clearly explains that TON wallet must be connected on fragment.com before extracting cookies
- Added warning about cookie expiration (30 days)

## [2.0.0] - 2025-01-21

### Added
- New method `get_queue_status()` - Get queue status and processing statistics
- New method `check_premium_eligibility(username)` - Check if user is eligible for Premium purchase
- New examples: `check_queue_status.py` and `check_eligibility.py`
- Updated documentation with new methods

### Changed
- Version bumped to 2.0.0 to match API v2.0.0
- Updated README.md and README.ru.md with new features

## [1.1.0] - 2024

### Added
- Initial release with core functionality
- Buy Telegram Stars
- Buy Telegram Premium
- Get commission rates
- Queue management
- KYC and non-KYC modes
