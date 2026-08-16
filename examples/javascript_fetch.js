/**
 * Direct REST example for Node.js 18+.
 *
 * Run:
 *   export FRAGMENT_WALLET_SEED="base64_seed_phrase"
 *   export FRAGMENT_USERNAME="@telegram_username"
 *   node examples/javascript_fetch.js
 *
 * No API key is required. Do not put wallet seeds or Fragment cookies
 * into frontend JavaScript; run this from your backend only.
 */

const API_URL = process.env.FRAGMENT_API_BASE_URL || "https://api.fragment-api.space";

function requireEnv(name) {
  const value = process.env[name];
  if (!value) throw new Error(`Set ${name}`);
  return value;
}

function normalizeUsername(username) {
  return username.startsWith("@") ? username : `@${username}`;
}

async function request(method, path, body) {
  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await response.json();
  if (!response.ok || data.success === false) {
    const error = data.error || {};
    throw new Error(`${error.error_code || response.status}: ${error.message || response.statusText}`);
  }
  return data;
}

async function pollResult(requestId) {
  for (let i = 0; i < 150; i += 1) {
    const response = await request("GET", `/api/v1/queue/${requestId}`);
    const status = response.data;

    if (status.status === "completed") return status.result || status;
    if (status.status === "failed") throw new Error(status.error || "Purchase failed");

    await new Promise((resolve) => setTimeout(resolve, 2000));
  }
  throw new Error("Purchase polling timed out");
}

async function main() {
  const payload = {
    username: normalizeUsername(process.env.FRAGMENT_USERNAME || "@telegram_username"),
    amount: Number(process.env.FRAGMENT_STARS || "100"),
    seed: requireEnv("FRAGMENT_WALLET_SEED"),
    payment_method: process.env.FRAGMENT_PAYMENT_METHOD || "ton",
  };

  if (process.env.FRAGMENT_COOKIES) {
    payload.fragment_cookies = process.env.FRAGMENT_COOKIES;
  }

  const accepted = await request("POST", "/api/v1/stars/buy", payload);
  const finalResult = await pollResult(accepted.data.request_id);
  console.log(JSON.stringify(finalResult, null, 2));
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
