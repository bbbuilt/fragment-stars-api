# Changelog

All notable changes to this project will be documented in this file.

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
