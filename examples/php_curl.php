<?php
/**
 * Direct REST example for PHP cURL.
 *
 * Run:
 *   export FRAGMENT_WALLET_SEED="base64_seed_phrase"
 *   export FRAGMENT_USERNAME="@telegram_username"
 *   php examples/php_curl.php
 *
 * No API key is required. Keep wallet seeds and Fragment cookies backend-only.
 */

$apiUrl = getenv('FRAGMENT_API_BASE_URL') ?: 'https://api.fragment-api.space';

function require_env(string $name): string {
    $value = getenv($name);
    if (!$value) {
        throw new RuntimeException("Set {$name}");
    }
    return $value;
}

function normalize_username(string $username): string {
    return str_starts_with($username, '@') ? $username : '@' . $username;
}

function api_request(string $method, string $path, ?array $payload = null): array {
    global $apiUrl;

    $ch = curl_init($apiUrl . $path);
    curl_setopt_array($ch, [
        CURLOPT_CUSTOMREQUEST => $method,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_TIMEOUT => 30,
    ]);

    if ($payload !== null) {
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload, JSON_UNESCAPED_SLASHES));
    }

    $raw = curl_exec($ch);
    $statusCode = curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    if ($raw === false) {
        throw new RuntimeException($curlError ?: 'cURL request failed');
    }

    $data = json_decode($raw, true);
    if (!is_array($data)) {
        throw new RuntimeException('API returned non-JSON response: ' . substr($raw, 0, 200));
    }

    if ($statusCode >= 400 || ($data['success'] ?? true) === false) {
        $error = $data['error'] ?? [];
        $code = $error['error_code'] ?? $statusCode;
        $message = $error['message'] ?? 'API request failed';
        throw new RuntimeException("{$code}: {$message}");
    }

    return $data;
}

function poll_result(string $requestId): array {
    for ($i = 0; $i < 150; $i++) {
        $response = api_request('GET', "/api/v1/queue/{$requestId}");
        $status = $response['data'];

        if ($status['status'] === 'completed') {
            return $status['result'] ?? $status;
        }
        if ($status['status'] === 'failed') {
            throw new RuntimeException($status['error'] ?? 'Purchase failed');
        }

        sleep(2);
    }

    throw new RuntimeException('Purchase polling timed out');
}

$payload = [
    'username' => normalize_username(getenv('FRAGMENT_USERNAME') ?: '@telegram_username'),
    'amount' => intval(getenv('FRAGMENT_STARS') ?: 100),
    'seed' => require_env('FRAGMENT_WALLET_SEED'),
    'payment_method' => getenv('FRAGMENT_PAYMENT_METHOD') ?: 'ton',
];

if (getenv('FRAGMENT_COOKIES')) {
    $payload['fragment_cookies'] = getenv('FRAGMENT_COOKIES');
}

$accepted = api_request('POST', '/api/v1/stars/buy', $payload);
$result = poll_result($accepted['data']['request_id']);

echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . PHP_EOL;
