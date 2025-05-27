import requests
import json
import time
from typing import Dict, List, Optional, Union, Any

# Mock data for initial development or if API fails
MOCK_ONRAMP_PROVIDERS = {
    "binance_p2p": {
        "name": "Binance P2P",
        "description": "Peer-to-peer marketplace for buying and selling cryptocurrencies",
        "supported_countries": ["NG", "KE", "GH", "ZA"],
        "supported_currencies": ["NGN", "KES", "GHS", "ZAR"],
        "payment_methods": ["Bank Transfer", "Mobile Money", "Cash"],
        "min_amount": {"NGN": 5000, "KES": 1000, "GHS": 100, "ZAR": 500},
        "max_amount": {"NGN": 10000000, "KES": 1000000, "GHS": 100000, "ZAR": 500000},
        "fees": {"percentage": 0.1, "fixed": {"NGN": 0, "KES": 0, "GHS": 0, "ZAR": 0}},
        "processing_time": "10-30 minutes",
        "kyc_required": False,
        "api_available": True
    },
    "paxful": {
        "name": "Paxful",
        "description": "P2P marketplace with escrow protection",
        "supported_countries": ["NG", "KE", "GH", "ZA"],
        "supported_currencies": ["NGN", "KES", "GHS", "ZAR"],
        "payment_methods": ["Bank Transfer", "Mobile Money", "Gift Cards", "Cash"],
        "min_amount": {"NGN": 2000, "KES": 500, "GHS": 50, "ZAR": 200},
        "max_amount": {"NGN": 5000000, "KES": 500000, "GHS": 50000, "ZAR": 250000},
        "fees": {"percentage": 0.5, "fixed": {"NGN": 100, "KES": 20, "GHS": 5, "ZAR": 10}},
        "processing_time": "15-45 minutes",
        "kyc_required": True,
        "api_available": True
    },
    "localbitcoins": {
        "name": "LocalBitcoins",
        "description": "P2P Bitcoin marketplace",
        "supported_countries": ["NG", "KE", "GH", "ZA"],
        "supported_currencies": ["NGN", "KES", "GHS", "ZAR"],
        "payment_methods": ["Bank Transfer", "Mobile Money", "Cash"],
        "min_amount": {"NGN": 3000, "KES": 700, "GHS": 70, "ZAR": 300},
        "max_amount": {"NGN": 7000000, "KES": 700000, "GHS": 70000, "ZAR": 350000},
        "fees": {"percentage": 0.3, "fixed": {"NGN": 50, "KES": 10, "GHS": 2, "ZAR": 5}},
        "processing_time": "20-60 minutes",
        "kyc_required": True,
        "api_available": True
    },
    "remitai_mock": {
        "name": "RemitAI Mock Provider",
        "description": "Mock on-ramp provider for development and testing",
        "supported_countries": ["NG", "KE", "GH", "ZA", "ET", "TZ", "UG", "RW"],
        "supported_currencies": ["NGN", "KES", "GHS", "ZAR", "ETB", "TZS", "UGX", "RWF"],
        "payment_methods": ["Bank Transfer", "Mobile Money", "USSD", "QR Code"],
        "min_amount": {"NGN": 1000, "KES": 200, "GHS": 20, "ZAR": 100, "ETB": 500, "TZS": 5000, "UGX": 5000, "RWF": 2000},
        "max_amount": {"NGN": 20000000, "KES": 2000000, "GHS": 200000, "ZAR": 1000000, "ETB": 1000000, "TZS": 10000000, "UGX": 10000000, "RWF": 5000000},
        "fees": {"percentage": 0.05, "fixed": {"NGN": 0, "KES": 0, "GHS": 0, "ZAR": 0, "ETB": 0, "TZS": 0, "UGX": 0, "RWF": 0}},
        "processing_time": "1-5 minutes",
        "kyc_required": False,
        "api_available": True
    }
}

class OnRampService:
    def __init__(self, use_mock: bool = True, preferred_provider: str = "remitai_mock"):
        """
        Initialize the On-Ramp service.
        
        Args:
            use_mock: Whether to use mock data instead of real API calls
            preferred_provider: Default provider to use for on-ramp operations
        """
        self.use_mock = use_mock
        self.preferred_provider = preferred_provider
        self.providers = MOCK_ONRAMP_PROVIDERS if use_mock else self._fetch_real_providers()
        
    def _fetch_real_providers(self) -> Dict[str, Any]:
        """
        In a real implementation, this would fetch actual provider data from APIs or a database.
        For now, we'll return the mock data.
        """
        # This would be replaced with actual API calls in production
        print("Note: Using mock provider data as real API integration is not implemented.")
        return MOCK_ONRAMP_PROVIDERS
    
    def get_available_providers(self, country_code: str, currency: str) -> List[Dict[str, Any]]:
        """
        Get a list of available on-ramp providers for the specified country and currency.
        
        Args:
            country_code: ISO country code (e.g., 'NG' for Nigeria)
            currency: Currency code (e.g., 'NGN' for Nigerian Naira)
            
        Returns:
            List of provider details dictionaries
        """
        available_providers = []
        
        for provider_id, provider_data in self.providers.items():
            if (country_code.upper() in provider_data["supported_countries"] and 
                currency.upper() in provider_data["supported_currencies"]):
                # Create a copy with the provider_id included
                provider_info = provider_data.copy()
                provider_info["id"] = provider_id
                available_providers.append(provider_info)
        
        return available_providers
    
    def get_provider_details(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific provider.
        
        Args:
            provider_id: Identifier for the provider
            
        Returns:
            Provider details dictionary or None if not found
        """
        if provider_id in self.providers:
            provider_info = self.providers[provider_id].copy()
            provider_info["id"] = provider_id
            return provider_info
        return None
    
    def calculate_fees(self, provider_id: str, amount: float, currency: str) -> Dict[str, Union[float, str]]:
        """
        Calculate the fees for a given transaction amount with the specified provider.
        
        Args:
            provider_id: Identifier for the provider
            amount: Transaction amount
            currency: Currency code
            
        Returns:
            Dictionary with fee details
        """
        if provider_id not in self.providers:
            return {"error": f"Provider {provider_id} not found"}
        
        provider = self.providers[provider_id]
        currency = currency.upper()
        
        if currency not in provider["supported_currencies"]:
            return {"error": f"Currency {currency} not supported by {provider['name']}"}
        
        # Calculate fees
        percentage_fee = amount * (provider["fees"]["percentage"] / 100)
        fixed_fee = provider["fees"]["fixed"].get(currency, 0)
        total_fee = percentage_fee + fixed_fee
        
        return {
            "provider": provider["name"],
            "amount": amount,
            "currency": currency,
            "percentage_fee": percentage_fee,
            "fixed_fee": fixed_fee,
            "total_fee": total_fee,
            "amount_after_fees": amount - total_fee
        }
    
    def initiate_onramp_transaction(
        self, 
        provider_id: str, 
        amount: float, 
        currency: str,
        payment_method: str,
        recipient_address: str,
        user_details: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        Initiate an on-ramp transaction to buy USDC.
        
        Args:
            provider_id: Identifier for the provider
            amount: Amount in local currency to convert to USDC
            currency: Local currency code
            payment_method: Payment method to use
            recipient_address: Wallet address to receive USDC
            user_details: Optional user details for KYC if required
            
        Returns:
            Transaction details dictionary
        """
        if self.use_mock:
            # Generate a mock transaction for development/testing
            transaction_id = f"tx_{int(time.time())}_{hash(recipient_address) % 10000}"
            
            # Calculate fees
            fee_info = self.calculate_fees(provider_id, amount, currency)
            if "error" in fee_info:
                return {"error": fee_info["error"]}
            
            # Mock exchange rate (this would come from exchange_rates.py in production)
            mock_exchange_rates = {
                "NGN_USDC": 0.00065,
                "KES_USDC": 0.0077,
                "GHS_USDC": 0.0070,
                "ZAR_USDC": 0.055,
                "ETB_USDC": 0.018,
                "TZS_USDC": 0.00039,
                "UGX_USDC": 0.00026,
                "RWF_USDC": 0.00085
            }
            
            exchange_rate = mock_exchange_rates.get(f"{currency.upper()}_USDC", 0.0001)
            usdc_amount = (amount - fee_info["total_fee"]) * exchange_rate
            
            # Mock payment instructions
            payment_instructions = {
                "Bank Transfer": {
                    "account_name": "RemitAI Payment Processor",
                    "account_number": "1234567890",
                    "bank_name": "Mock Bank",
                    "reference": transaction_id
                },
                "Mobile Money": {
                    "phone_number": "+1234567890",
                    "provider": "Mock Mobile Money",
                    "reference": transaction_id
                },
                "USSD": {
                    "code": "*123*4#",
                    "reference": transaction_id
                },
                "QR Code": {
                    "qr_data": f"mockqr://{transaction_id}",
                    "reference": transaction_id
                }
            }
            
            return {
                "transaction_id": transaction_id,
                "status": "pending",
                "provider": self.providers[provider_id]["name"],
                "amount": amount,
                "currency": currency.upper(),
                "fees": fee_info["total_fee"],
                "exchange_rate": exchange_rate,
                "usdc_amount": usdc_amount,
                "recipient_address": recipient_address,
                "payment_method": payment_method,
                "payment_instructions": payment_instructions.get(payment_method, {"message": "Contact support for payment instructions"}),
                "estimated_completion_time": self.providers[provider_id]["processing_time"],
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                "expires_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() + 3600))  # 1 hour expiry
            }
        else:
            # In a real implementation, this would make API calls to the selected provider
            # For now, we'll return an error
            return {"error": "Real API integration not implemented. Use mock mode for development."}
    
    def check_transaction_status(self, transaction_id: str) -> Dict[str, Any]:
        """
        Check the status of an on-ramp transaction.
        
        Args:
            transaction_id: Transaction identifier
            
        Returns:
            Transaction status dictionary
        """
        if self.use_mock:
            # Parse the timestamp from the mock transaction ID
            try:
                tx_time = int(transaction_id.split('_')[1])
                elapsed_seconds = time.time() - tx_time
                
                # Simulate different statuses based on elapsed time
                if elapsed_seconds < 60:  # Less than 1 minute
                    status = "pending"
                    message = "Waiting for payment confirmation"
                elif elapsed_seconds < 120:  # 1-2 minutes
                    status = "processing"
                    message = "Payment received, processing transaction"
                elif elapsed_seconds < 180:  # 2-3 minutes
                    status = "completed"
                    message = "Transaction completed successfully"
                else:
                    # Randomly decide if transaction failed (10% chance)
                    if hash(transaction_id) % 10 == 0:
                        status = "failed"
                        message = "Transaction failed. Please contact support."
                    else:
                        status = "completed"
                        message = "Transaction completed successfully"
                
                return {
                    "transaction_id": transaction_id,
                    "status": status,
                    "message": message,
                    "last_updated": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                }
            except (IndexError, ValueError):
                return {"error": "Invalid transaction ID format"}
        else:
            # In a real implementation, this would make API calls to check status
            return {"error": "Real API integration not implemented. Use mock mode for development."}

# Example Usage
if __name__ == "__main__":
    onramp_service = OnRampService(use_mock=True)
    
    print("=== Available On-Ramp Providers in Nigeria for NGN ===")
    nigeria_providers = onramp_service.get_available_providers("NG", "NGN")
    for provider in nigeria_providers:
        print(f"- {provider['name']}: {provider['description']}")
        print(f"  Supported payment methods: {', '.join(provider['payment_methods'])}")
        print(f"  Processing time: {provider['processing_time']}")
        print(f"  KYC required: {provider['kyc_required']}")
        print()
    
    print("=== Fee Calculation Example ===")
    fee_details = onramp_service.calculate_fees("remitai_mock", 100000, "NGN")
    print(f"Provider: {fee_details['provider']}")
    print(f"Amount: {fee_details['amount']} {fee_details['currency']}")
    print(f"Fees: {fee_details['total_fee']} {fee_details['currency']} ({fee_details['percentage_fee']} + {fee_details['fixed_fee']})")
    print(f"Amount after fees: {fee_details['amount_after_fees']} {fee_details['currency']}")
    print()
    
    print("=== Mock Transaction Initiation ===")
    transaction = onramp_service.initiate_onramp_transaction(
        provider_id="remitai_mock",
        amount=100000,
        currency="NGN",
        payment_method="Bank Transfer",
        recipient_address="0x1234567890abcdef1234567890abcdef12345678"
    )
    print(f"Transaction ID: {transaction['transaction_id']}")
    print(f"Status: {transaction['status']}")
    print(f"Amount: {transaction['amount']} {transaction['currency']}")
    print(f"USDC Amount: {transaction['usdc_amount']:.2f} USDC")
    print(f"Payment Method: {transaction['payment_method']}")
    print(f"Payment Instructions: {json.dumps(transaction['payment_instructions'], indent=2)}")
    print(f"Estimated Completion Time: {transaction['estimated_completion_time']}")
    print()
    
    print("=== Transaction Status Check ===")
    # Use the transaction ID from above
    status = onramp_service.check_transaction_status(transaction['transaction_id'])
    print(f"Transaction ID: {status['transaction_id']}")
    print(f"Status: {status['status']}")
    print(f"Message: {status['message']}")
    print(f"Last Updated: {status['last_updated']}")
