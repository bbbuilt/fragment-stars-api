# Fragment Cookies Guide

This guide explains how to get Fragment.com cookies for KYC mode (lower commission rate).

## What are Fragment Cookies?

Fragment cookies are authentication tokens that prove you're logged into fragment.com. When you provide these cookies to the API, it can make purchases on your behalf using your Fragment account.

## Why Use KYC Mode?

| Mode | Commission | Cookies Required | Prepayment |
|------|-----------|------------------|------------|
| **No KYC** | Higher (e.g., 10%) | ❌ No | ✅ Yes |
| **KYC** | Lower (e.g., 5%) | ✅ Yes | ❌ No |

KYC mode offers lower commission rates because purchases are made through your verified Fragment account.

## Required Cookies

You need these 4 cookies from fragment.com:

| Cookie Name | Required | Description |
|-------------|----------|-------------|
| `stel_token` | ✅ Yes | Main session authentication token |
| `stel_ssid` | ✅ Yes | Session ID |
| `stel_ton_token` | ✅ **CRITICAL** | TON wallet connection token - **required for purchases** |
| `stel_dt` | ✅ Yes | Timezone offset (usually `-180` or your local offset) |

> ⚠️ **IMPORTANT**: The `stel_ton_token` cookie is **absolutely required** for making purchases. Without it, purchases will fail with "wallet not connected" error.

## Step-by-Step Guide

### Step 1: Login to Fragment

1. Open **Chrome** or **Edge** browser (recommended)
2. Go to https://fragment.com
3. Click **"Log In"** button
4. Authorize via Telegram
5. You should see your profile in the top-right corner

### Step 2: Connect TON Wallet

**This step is CRITICAL for getting `stel_ton_token` cookie!**

1. On fragment.com, click **"Connect Wallet"** button
2. Choose your wallet:
   - **Tonkeeper** (recommended)
   - **MyTonWallet**
   - **Tonhub**
3. Scan QR code or use browser extension
4. Confirm connection in your wallet app
5. Verify wallet is connected (you should see wallet address on fragment.com)

> 💡 **Tip**: Make sure the wallet you connect has the same address as the seed phrase you'll use in the API!

### Step 3: Open Developer Tools

**Chrome/Edge:**
- Press `F12` or `Ctrl+Shift+I` (Windows/Linux)
- Press `Cmd+Option+I` (Mac)

**Firefox:**
- Press `F12` or `Ctrl+Shift+K`

### Step 4: Navigate to Cookies

1. In DevTools, click the **"Application"** tab (Chrome/Edge) or **"Storage"** tab (Firefox)
2. In the left sidebar, expand **"Cookies"**
3. Click on `https://fragment.com`

You should see a list of all cookies for fragment.com.

### Step 5: Copy Cookie Values

Find and copy the **Value** column for each required cookie:

#### Example Screenshot Reference:
```
Name                Value
----                -----
stel_token          1234567890abcdef...
stel_ssid           abcdef1234567890...
stel_ton_token      tonconnect_xyz123...  ← MUST be present!
stel_dt             -180
```

> ⚠️ **Check**: If you don't see `stel_ton_token`, go back to Step 2 and connect your TON wallet!

### Step 6: Create JSON File

Create a file named `cookies.json` with this structure:

```json
{
    "stel_token": "paste_your_stel_token_value_here",
    "stel_ssid": "paste_your_stel_ssid_value_here",
    "stel_ton_token": "paste_your_stel_ton_token_value_here",
    "stel_dt": "-180"
}
```

**Example with real values:**
```json
{
    "stel_token": "1234567890abcdef1234567890abcdef",
    "stel_ssid": "abcdef1234567890abcdef1234567890",
    "stel_ton_token": "tonconnect_xyz123abc456def789",
    "stel_dt": "-180"
}
```

> 💡 **Note**: `stel_dt` is your timezone offset in minutes. `-180` = UTC+3 (Moscow). Adjust if needed.

### Step 7: Encode to Base64

The API expects cookies in base64 format.

**Linux/Mac:**
```bash
cat cookies.json | base64 -w 0
```

**Windows PowerShell:**
```powershell
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content cookies.json -Raw)))
```

**Python:**
```python
import base64
import json

with open('cookies.json', 'r') as f:
    cookies = json.load(f)

encoded = base64.b64encode(json.dumps(cookies).encode()).decode()
print(encoded)
```

**Online Tool:**
- Go to https://www.base64encode.org/
- Paste your JSON
- Click "Encode"
- Copy the result

### Step 8: Use in Your Code

```python
from fragment_api import FragmentAPIClient

client = FragmentAPIClient("https://your-api-server.com:8443")

# Your base64-encoded cookies from Step 7
COOKIES = "eyJzdGVsX3Rva2VuIjoiMTIzNDU2Nzg5MGFiY2RlZiIsInN0ZWxfc3NpZCI6ImFiY2RlZjEyMzQ1Njc4OTAiLCJzdGVsX3Rvbl90b2tlbiI6InRvbmNvbm5lY3RfeHl6MTIzIiwic3RlbF9kdCI6Ii0xODAifQ=="

result = client.buy_stars(
    username="telegram_user",
    amount=100,
    seed="your_seed_base64",
    cookies=COOKIES  # ← Your encoded cookies here
)

if result.success:
    print(f"✅ Success! Mode: {result.mode}")  # Should show 'kyc'
    print(f"Commission rate: {result.commission_rate * 100}%")
else:
    print(f"❌ Error: {result.error}")
```

## Alternative Format: Array of Objects

The API also accepts cookies in array format:

```json
[
    {
        "name": "stel_token",
        "value": "your_value_here",
        "domain": ".fragment.com",
        "path": "/"
    },
    {
        "name": "stel_ssid",
        "value": "your_value_here",
        "domain": ".fragment.com",
        "path": "/"
    },
    {
        "name": "stel_ton_token",
        "value": "your_value_here",
        "domain": ".fragment.com",
        "path": "/"
    },
    {
        "name": "stel_dt",
        "value": "-180",
        "domain": ".fragment.com",
        "path": "/"
    }
]
```

This format is useful if you're exporting cookies from browser extensions like "EditThisCookie".

## Troubleshooting

### Error: "Invalid or expired cookies"

**Cause**: Cookies are expired or malformed.

**Solution**:
1. Get fresh cookies from fragment.com
2. Make sure you're still logged in
3. Check that all 4 cookies are present
4. Verify base64 encoding is correct

### Error: "Wallet not connected"

**Cause**: Missing `stel_ton_token` cookie.

**Solution**:
1. Go to fragment.com
2. Click "Connect Wallet"
3. Connect your TON wallet (Tonkeeper/MyTonWallet)
4. Get fresh cookies (including `stel_ton_token`)

### Error: "User not found"

**Cause**: The Telegram username doesn't exist or is incorrect.

**Solution**:
1. Check username spelling (without @)
2. Make sure the user has a public Telegram account
3. Try with a different username to test

### Cookies expire quickly

**Cause**: Fragment cookies typically expire after 30 days or when you logout.

**Solution**:
1. Get fresh cookies when needed
2. Store cookies securely
3. Implement automatic cookie refresh in your application
4. Consider using No-KYC mode if cookie management is too complex

## Security Best Practices

### ⚠️ NEVER share your cookies!

Fragment cookies provide **full access** to your Fragment account. Anyone with your cookies can:
- Make purchases on your behalf
- Access your Fragment balance
- View your transaction history
- Potentially drain your account

### Recommendations:

1. **Store securely**: Use environment variables or encrypted storage
2. **Don't commit**: Add `cookies.json` to `.gitignore`
3. **Rotate regularly**: Get fresh cookies every 30 days
4. **Monitor usage**: Check your Fragment account regularly
5. **Use separate account**: Consider using a dedicated Fragment account for API access

### Example `.gitignore`:
```
cookies.json
*.cookies
*_cookies.json
.env
```

## Cookie Lifetime

- **Typical lifetime**: 30 days
- **Expires when**: You logout from fragment.com
- **Refresh**: Get new cookies when expired

## FAQ

### Q: Can I use cookies from mobile browser?

**A**: Yes, but it's harder to extract cookies from mobile. Desktop browser is recommended.

### Q: Do I need to keep browser open?

**A**: No, once you have the cookies, you can close the browser. The API will use the cookies independently.

### Q: Can multiple people use the same cookies?

**A**: Technically yes, but it's not recommended for security reasons. Each user should have their own Fragment account and cookies.

### Q: What if I don't want to provide cookies?

**A**: Use No-KYC mode instead. It has higher commission but doesn't require cookies:

```python
result = client.buy_stars(
    username="user",
    amount=100,
    seed="your_seed_base64"
    # No cookies parameter = No-KYC mode
)
```

### Q: Can I automate cookie extraction?

**A**: Yes, you can use browser automation tools like Selenium or Playwright to extract cookies programmatically. However, you'll still need to handle the initial login and wallet connection manually.

## Need Help?

- **GitHub Issues**: [fragment-stars-api/issues](https://github.com/bbbuilt/fragment-stars-api/issues)
- **Telegram**: [@basebay](https://t.me/basebay)
- **Documentation**: See [README.md](README.md) for more examples

---

**Last updated**: January 2026
