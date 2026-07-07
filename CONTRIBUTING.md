# Contributing

Thanks for improving Fragment Stars API.

## Good Contributions

- Clear bug reports with `request_id`, error code, payment method, and expected behavior.
- Documentation fixes that make integration easier.
- Examples for other backend languages.
- Safe SDK improvements that do not expose wallet seeds or Fragment cookies.

## Security and Secrets

Never post these in issues, pull requests, screenshots, logs, or examples:

- Wallet seed phrase
- Fragment cookies
- Private keys
- Full localStorage dumps
- Customer personal data

If you need help debugging, share only safe data: `request_id`, username, Stars amount, payment method, error code, and sanitized logs.

## Development

```bash
python -m py_compile fragment_api/*.py examples/*.py
python -m build
```

Keep runtime compatibility for existing clients. Do not change public request fields or defaults without documenting migration steps.

## Pull Requests

- Keep changes focused.
- Update README/docs/examples when behavior changes.
- Add or update examples for client-facing integration changes.
- Explain whether the change affects SDK users, direct REST users, or both.
