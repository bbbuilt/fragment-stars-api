// Direct REST example for Go net/http.
//
// Run:
//
//	export FRAGMENT_WALLET_SEED="base64_seed_phrase"
//	export FRAGMENT_USERNAME="@telegram_username"
//	go run examples/go_net_http.go
//
// No API key is required. Keep wallet seeds and Fragment cookies backend-only.
package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
)

var apiURL = getEnv("FRAGMENT_API_BASE_URL", "https://fragment-api.ydns.eu:8443")

type apiError struct {
	Code      any    `json:"code"`
	ErrorCode string `json:"error_code"`
	Message   string `json:"message"`
}

type apiResponse struct {
	Success bool                   `json:"success"`
	Data    map[string]any         `json:"data"`
	Error   *apiError              `json:"error"`
	Raw     map[string]interface{} `json:"-"`
}

func main() {
	payload := map[string]any{
		"username":       normalizeUsername(getEnv("FRAGMENT_USERNAME", "@telegram_username")),
		"amount":         mustAtoi(getEnv("FRAGMENT_STARS", "100")),
		"seed":           requireEnv("FRAGMENT_WALLET_SEED"),
		"payment_method": getEnv("FRAGMENT_PAYMENT_METHOD", "ton"),
	}

	if cookies := os.Getenv("FRAGMENT_COOKIES"); cookies != "" {
		payload["fragment_cookies"] = cookies
	}

	accepted, err := request("POST", "/api/v1/stars/buy", payload)
	if err != nil {
		panic(err)
	}

	requestID, ok := accepted.Data["request_id"].(string)
	if !ok || requestID == "" {
		panic("API response did not contain request_id")
	}

	result, err := pollResult(requestID)
	if err != nil {
		panic(err)
	}

	pretty, _ := json.MarshalIndent(result, "", "  ")
	fmt.Println(string(pretty))
}

func request(method, path string, payload any) (*apiResponse, error) {
	var body io.Reader
	if payload != nil {
		encoded, err := json.Marshal(payload)
		if err != nil {
			return nil, err
		}
		body = bytes.NewReader(encoded)
	}

	req, err := http.NewRequest(method, apiURL+path, body)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	raw, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var decoded apiResponse
	if err := json.Unmarshal(raw, &decoded); err != nil {
		return nil, fmt.Errorf("API returned non-JSON response: %s", string(raw[:previewLen(raw, 200)]))
	}

	if resp.StatusCode >= 400 || !decoded.Success {
		if decoded.Error != nil {
			return nil, fmt.Errorf("%s: %s", decoded.Error.ErrorCode, decoded.Error.Message)
		}
		return nil, fmt.Errorf("API request failed: HTTP %d", resp.StatusCode)
	}

	return &decoded, nil
}

func pollResult(requestID string) (map[string]any, error) {
	for i := 0; i < 150; i++ {
		response, err := request("GET", "/api/v1/queue/"+requestID, nil)
		if err != nil {
			return nil, err
		}

		status, _ := response.Data["status"].(string)
		switch status {
		case "completed":
			if result, ok := response.Data["result"].(map[string]any); ok {
				return result, nil
			}
			return response.Data, nil
		case "failed":
			if message, ok := response.Data["error"].(string); ok && message != "" {
				return nil, errors.New(message)
			}
			return nil, errors.New("purchase failed")
		}

		time.Sleep(2 * time.Second)
	}

	return nil, errors.New("purchase polling timed out")
}

func previewLen(data []byte, limit int) int {
	if len(data) < limit {
		return len(data)
	}
	return limit
}

func normalizeUsername(username string) string {
	if strings.HasPrefix(username, "@") {
		return username
	}
	return "@" + username
}

func requireEnv(name string) string {
	value := os.Getenv(name)
	if value == "" {
		panic("Set " + name)
	}
	return value
}

func getEnv(name, fallback string) string {
	if value := os.Getenv(name); value != "" {
		return value
	}
	return fallback
}

func mustAtoi(value string) int {
	var result int
	if _, err := fmt.Sscanf(value, "%d", &result); err != nil {
		panic(err)
	}
	return result
}
