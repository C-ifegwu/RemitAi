import time
import json
from typing import Dict, List, Optional, Union, Any

# Mock data for initial development or if API fails
MOCK_OFFRAMP_PROVIDERS = {
    "flutterwave_mock": {
        "name": "Flutterwave (Mock)",
        "description": "Mock off-ramp provider simulating Flutterwave for development and testing",
        "supported_countries": ["NG", "KE", "GH", "ZA", "UG", "TZ"],
        "supported_currencies": ["NGN", "KES", "GHS", "ZAR", "UGX", "TZS"],
        "payout_methods": ["Bank Transfer", "Mobile Money"],
        "min_amount_usdc": 10,
        "max_amount_usdc": 5000,
        "fees": {"percentage": 0.8, "fixed_usdc": 0.5},
        "processing_time": "15-60 minutes",
        "kyc_required": True,
        "api_available": True
    },
    "stellar_anchor_mock": {
        "name": "Stellar Anchor (Mock)",
        "description": "Mock off-ramp provider simulating a Stellar Anchor for development and testing",
        "supported_countries": ["NG", "KE"],
        "supported_currencies": ["NGN", "KES"],
        "payout_methods": ["Bank Transfer", "Mobile Money (via anchor)"],
        "min_amount_usdc": 5,
        "max_amount_usdc": 2000,
        "fees": {"percentage": 0.5, "fixed_usdc": 0.2},
        "processing_time": "5-30 minutes",
        "kyc_required": True,
        "api_available": True
    }
}

# Mock exchange rates (USDC to Fiat)
# In a real scenario, this would come from the ExchangeRateUtil or the provider itself
MOCK_USDC_TO_FIAT_RATES = {
    "USDC_NGN": 1520.00,
    "USDC_KES": 129.50,
    "USDC_GHS": 141.00,
    "USDC_ZAR": 18.50,
    "USDC_UGX": 3800.00,
    "USDC_TZS": 2500.00
}

class OffRampService:
    def __init__(self, use_mock: bool = True, preferred_provider: str = "flutterwave_mock"):
        self.use_mock = use_mock
        self.preferred_provider = preferred_provider
        self.providers = MOCK_OFFRAMP_PROVIDERS if use_mock else self._fetch_real_providers()

    def _fetch_real_providers(self) -> Dict[str, Any]:
        print("Note: Using mock provider data as real API integration for off-ramp is not implemented.")
        return MOCK_OFFRAMP_PROVIDERS

    def get_available_providers(self, country_code: str, currency: str) -> List[Dict[str, Any]]:
        available_providers = []
        for provider_id, provider_data in self.providers.items():
            if (country_code.upper() in provider_data["supported_countries"] and
                currency.upper() in provider_data["supported_currencies"]):
                provider_info = provider_data.copy()
                provider_info["id"] = provider_id
                available_providers.append(provider_info)
        return available_providers

    def get_provider_details(self, provider_id: str) -> Optional[Dict[str, Any]]:
        if provider_id in self.providers:
            provider_info = self.providers[provider_id].copy()
            provider_info["id"] = provider_id
            return provider_info
        return None

    def calculate_offramp_details(self, provider_id: str, usdc_amount: float, target_currency: str) -> Dict[str, Union[float, str, None]]:
        if provider_id not in self.providers:
            return {"error": f"Provider {provider_id} not found"}

        provider = self.providers[provider_id]
        target_currency = target_currency.upper()

        if target_currency not in provider["supported_currencies"]:
            return {"error": f"Currency {target_currency} not supported by {provider['name']}"}
        
        if usdc_amount < provider["min_amount_usdc"] or usdc_amount > provider["max_amount_usdc"]:
            return {"error": f"Amount {usdc_amount} USDC is outside provider limits ({provider['min_amount_usdc']}-{provider['max_amount_usdc']} USDC)"}

        percentage_fee_usdc = usdc_amount * (provider["fees"]["percentage"] / 100)
        fixed_fee_usdc = provider["fees"]["fixed_usdc"]
        total_fee_usdc = percentage_fee_usdc + fixed_fee_usdc
        net_usdc_to_convert = usdc_amount - total_fee_usdc

        exchange_rate_pair = f"USDC_{target_currency}"
        exchange_rate = MOCK_USDC_TO_FIAT_RATES.get(exchange_rate_pair)

        if exchange_rate is None:
            return {"error": f"Exchange rate for {exchange_rate_pair} not available."}

        fiat_amount_after_conversion = net_usdc_to_convert * exchange_rate

        return {
            "provider_name": provider["name"],
            "initial_usdc_amount": usdc_amount,
            "total_fee_usdc": total_fee_usdc,
            "net_usdc_to_convert": net_usdc_to_convert,
            "exchange_rate_used": exchange_rate,
            "target_currency": target_currency,
            "estimated_fiat_received": fiat_amount_after_conversion,
            "processing_time": provider["processing_time"]
        }

    def initiate_offramp_transaction(
        self,
        provider_id: str,
        usdc_amount: float,
        target_currency: str,
        payout_method: str,
        payout_details: Dict[str, str], # e.g., {"bank_account": "123", "bank_code": "011", "recipient_name": "John Doe"} or {"mobile_number": "07...", "network": "Safaricom"}
        sender_wallet_address: str # Stellar/Soroban address sending USDC
    ) -> Dict[str, Any]:
        if self.use_mock:
            calc_details = self.calculate_offramp_details(provider_id, usdc_amount, target_currency)
            if "error" in calc_details:
                return {"error": calc_details["error"]}

            transaction_id = f"offtx_{int(time.time())}_{hash(sender_wallet_address) % 10000}"
            provider_name = self.providers[provider_id]["name"]

            return {
                "transaction_id": transaction_id,
                "status": "pending_usdc_transfer", # User needs to send USDC to a specified address
                "provider": provider_name,
                "usdc_amount_due": usdc_amount, # This is the gross amount the user should send
                "target_currency": target_currency,
                "estimated_fiat_payout": calc_details["estimated_fiat_received"],
                "fees_in_usdc": calc_details["total_fee_usdc"],
                "payout_method": payout_method,
                "payout_details_provided": payout_details,
                "deposit_address_for_usdc": f"STELLAR_ADDRESS_FOR_{provider_id.upper()}_DEPOSITS", # Mock deposit address
                "memo_required": f"REMITAI_{transaction_id}", # Mock memo
                "estimated_completion_time": self.providers[provider_id]["processing_time"],
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                "expires_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() + 3600)) # 1 hour expiry
            }
        else:
            return {"error": "Real API integration for off-ramp not implemented. Use mock mode."}

    def check_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        if self.use_mock:
            try:
                tx_time = int(transaction_id.split("_")[1])
                elapsed_seconds = time.time() - tx_time
                status = "pending_usdc_transfer"
                message = "Waiting for user to transfer USDC to the provided address."

                if elapsed_seconds > 60: # Assume user sent USDC after 1 min
                    status = "usdc_received_processing_fiat"
                    message = "USDC received. Processing fiat payout."
                if elapsed_seconds > 180: # Assume fiat payout processed after 3 mins
                    status = "completed"
                    message = "Fiat payout completed successfully."
                if elapsed_seconds > 3600 and status != "completed": # Expired if not completed
                    status = "expired"
                    message = "Transaction expired before USDC transfer or completion."
                
                # Simulate a failure for some transactions
                if hash(transaction_id) % 15 == 0 and status not in ["pending_usdc_transfer", "expired"]:
                    status = "failed"
                    message = "Fiat payout failed. Please contact support."

                return {
                    "transaction_id": transaction_id,
                    "status": status,
                    "message": message,
                    "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                }
            except (IndexError, ValueError):
                return {"error": "Invalid transaction ID format for mock status check."}
        else:
            return {"error": "Real API integration for off-ramp not implemented."}

# Example Usage:
if __name__ == "__main__":
    offramp_service = OffRampService(use_mock=True)

    print("=== Available Off-Ramp Providers in Kenya for KES ===")
    kenya_providers = offramp_service.get_available_providers("KE", "KES")
    for provider in kenya_providers:
        print(f"- {provider['name']}: {provider['description']}")
        print(f"  Supported payout methods: {', '.join(provider['payout_methods'])}")
        print(f"  Min USDC: {provider['min_amount_usdc']}, Max USDC: {provider['max_amount_usdc']}")
        print()

    print("=== Off-Ramp Calculation Example (Flutterwave Mock) ===")
    usdc_to_offramp = 100.0
    target_fiat = "KES"
    calc_details = offramp_service.calculate_offramp_details("flutterwave_mock", usdc_to_offramp, target_fiat)
    if "error" in calc_details:
        print(f"Error: {calc_details['error']}")
    else:
        print(f"Off-ramping {calc_details['initial_usdc_amount']} USDC via {calc_details['provider_name']}:")
        print(f"  Total Fees (USDC): {calc_details['total_fee_usdc']}")
        print(f"  Net USDC to Convert: {calc_details['net_usdc_to_convert']}")
        print(f"  Exchange Rate (USDC to {calc_details['target_currency']}): {calc_details['exchange_rate_used']}")
        print(f"  Estimated Fiat Received: {calc_details['estimated_fiat_received']:.2f} {calc_details['target_currency']}")
        print(f"  Processing Time: {calc_details['processing_time']}")
    print()

    print("=== Mock Off-Ramp Transaction Initiation ===")
    transaction = offramp_service.initiate_offramp_transaction(
        provider_id="flutterwave_mock",
        usdc_amount=usdc_to_offramp,
        target_currency=target_fiat,
        payout_method="Mobile Money",
        payout_details={"mobile_number": "+254712345678", "recipient_name": "Jane Doe"},
        sender_wallet_address="GABC...XYZ"
    )
    if "error" in transaction:
        print(f"Error initiating transaction: {transaction['error']}")
    else:
        print(f"Transaction ID: {transaction['transaction_id']}")
        print(f"Status: {transaction['status']}")
        print(f"Provider: {transaction['provider']}")
        print(f"USDC Amount Due: {transaction['usdc_amount_due']} USDC")
        print(f"Deposit Address for USDC: {transaction['deposit_address_for_usdc']}")
        print(f"Memo Required: {transaction['memo_required']}")
        print(f"Estimated Fiat Payout: {transaction['estimated_fiat_payout']:.2f} {transaction['target_currency']}")
        print(f"Payout Method: {transaction['payout_method']}")
        print(f"Payout Details: {json.dumps(transaction['payout_details_provided'], indent=2)}")
    print()

    if "transaction_id" in transaction and "error" not in transaction:
        print("=== Transaction Status Check (after a short delay) ===")
        # Simulate some time passing
        # In a real app, this would be checked periodically or via webhooks
        time.sleep(2) # Short delay for example
        status_check = offramp_service.check_transaction_status(transaction["transaction_id"])
        print(f"Transaction ID: {status_check.get('transaction_id')}")
        print(f"Status: {status_check.get('status')}")
        print(f"Message: {status_check.get('message')}")
        print(f"Last Updated: {status_check.get('last_updated')}")
