"""
Example: Check commission rates
"""

from fragment_api import FragmentAPIClient

# Initialize client with your API server
API_URL = "https://your-api-server.com:8443"
client = FragmentAPIClient(API_URL)

rates = client.get_rates()

print("Commission Rates:")
print(f"  No KYC:   {rates.rate_no_kyc}% ({rates.rate_no_kyc_decimal})")
print(f"  With KYC: {rates.rate_with_kyc}% ({rates.rate_with_kyc_decimal})")
print(f"  Updated:  {rates.updated_at}")
