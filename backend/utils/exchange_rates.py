import requests
import json
import time

# Mock data for initial development or if API fails
MOCK_RATES = {
    "NGN_USDC": {"price": "0.00065", "last_updated": time.time()},
    "KES_USDC": {"price": "0.0077", "last_updated": time.time()},
    "GHS_USDC": {"price": "0.0070", "last_updated": time.time()}, # Adjusted GHS for more variance
    "USD_USDC": {"price": "1.0", "last_updated": time.time()},
    # Inverse for USDC to fiat (less common for P2P direct quote but useful for conversion)
    "USDC_NGN": {"price": "1530.00", "last_updated": time.time()},
    "USDC_KES": {"price": "130.00", "last_updated": time.time()},
    "USDC_GHS": {"price": "142.00", "last_updated": time.time()}
}

CACHE_DURATION = 300 # Cache duration in seconds (5 minutes)

class ExchangeRateUtil:
    def __init__(self, use_mock=False):
        self.use_mock = use_mock
        self.cache = MOCK_RATES if use_mock else {}

    def _get_from_cache(self, pair: str):
        if pair in self.cache:
            cached_data = self.cache[pair]
            if time.time() - cached_data.get("last_updated", 0) < CACHE_DURATION:
                return float(cached_data["price"])
        return None

    def _update_cache(self, pair: str, price: float):
        self.cache[pair] = {"price": str(price), "last_updated": time.time()}

    def get_live_fx_rate_binance_p2p(self, fiat_currency: str, asset: str = "USDT", trade_type: str = "BUY"):
        """
        Fetches live P2P rates from Binance. 
        Note: Binance P2P API is not officially public and might be unstable or require specific headers.
        This is a conceptual implementation. For production, a reliable, official API is recommended.
        For RemitAI, we are primarily interested in FIAT -> USDC (or USDT as proxy) and USDC -> FIAT.
        If asset is USDC and trade_type is BUY, it means user is buying USDC with FIAT (e.g., NGN -> USDC).
        If asset is USDC and trade_type is SELL, it means user is selling USDC for FIAT (e.g., USDC -> NGN).
        """
        if self.use_mock:
            pair_key = f"{fiat_currency.upper()}_{asset.upper()}" if trade_type == "BUY" else f"{asset.upper()}_{fiat_currency.upper()}"
            if pair_key in MOCK_RATES:
                print(f"Using mock rate for {pair_key}")
                return float(MOCK_RATES[pair_key]["price"])
            else:
                print(f"Mock rate for {pair_key} not found, returning None.")
                return None

        pair_key_cache = f"{fiat_currency.upper()}_{asset.upper()}_{trade_type}" # More specific cache key
        cached_rate = self._get_from_cache(pair_key_cache)
        if cached_rate is not None:
            print(f"Using cached rate for {pair_key_cache}: {cached_rate}")
            return cached_rate

        # This is a simplified conceptual API call structure for Binance P2P
        # The actual API endpoint and parameters can change and are not officially documented for public use.
        url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        }
        payload = {
            "page": 1,
            "rows": 5, # Fetch a few ads to get an idea of the rate
            "payTypes": [], # Can specify payment types if needed
            "countries": [], # Can specify country if needed
            "tradeType": trade_type, # BUY (user buys asset with fiat) or SELL (user sells asset for fiat)
            "asset": asset, # e.g., USDT, USDC, BTC
            "fiat": fiat_currency, # e.g., NGN, KES, GHS
            "publisherType": None # or "merchant"
        }

        try:
            print(f"Attempting to fetch live P2P rate for {fiat_currency}/{asset} ({trade_type}) from Binance...")
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes
            data = response.json()
            
            if data.get("code") == "000000" and data.get("data"):
                ads = data["data"]
                if ads:
                    # Get the price from the first (often best) ad
                    # Prices can vary, so averaging or selecting the best might be needed
                    price = float(ads[0]["adv"]["price"])
                    print(f"Live rate for {fiat_currency}/{asset} ({trade_type}): {price}")
                    self._update_cache(pair_key_cache, price)
                    return price
                else:
                    print(f"No P2P ads found for {fiat_currency}/{asset} ({trade_type}).")
                    return None
            else:
                print(f"Error from Binance P2P API: {data.get('message', 'Unknown error')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching live P2P rate: {e}")
            print("Falling back to mock rates for this request if available.")
            # Fallback to mock if API fails for this specific request
            pair_key_mock = f"{fiat_currency.upper()}_{asset.upper()}" if trade_type == "BUY" else f"{asset.upper()}_{fiat_currency.upper()}"
            if pair_key_mock in MOCK_RATES:
                return float(MOCK_RATES[pair_key_mock]["price"])
            return None

    def convert_to_usdc(self, amount: float, from_currency: str):
        """Converts a given amount of local currency to USDC."""
        if from_currency.upper() == "USDC":
            return amount
        
        # We are buying USDC with from_currency
        rate = self.get_live_fx_rate_binance_p2p(fiat_currency=from_currency, asset="USDC", trade_type="BUY")
        if rate and rate > 0: # Rate here is how much FIAT for 1 USDC
            return amount / rate 
        print(f"Could not get conversion rate for {from_currency} to USDC.")
        return None

    def convert_from_usdc(self, usdc_amount: float, to_currency: str):
        """Converts a given amount of USDC to local currency."""
        if to_currency.upper() == "USDC":
            return usdc_amount
        
        # We are selling USDC for to_currency
        rate = self.get_live_fx_rate_binance_p2p(fiat_currency=to_currency, asset="USDC", trade_type="SELL")
        if rate: # Rate here is how much FIAT for 1 USDC
            return usdc_amount * rate
        print(f"Could not get conversion rate for USDC to {to_currency}.")
        return None

# Example Usage:
if __name__ == "__main__":
    # Set use_mock=True to always use mock data without attempting API calls
    # Set use_mock=False to attempt API calls (might fail in sandbox or due to API changes)
    exchange_util = ExchangeRateUtil(use_mock=True) 

    print("--- Testing Fiat to USDC Conversion (User Buys USDC) ---")
    ngn_amount = 100000
    usdc_from_ngn = exchange_util.convert_to_usdc(ngn_amount, "NGN")
    if usdc_from_ngn is not None:
        print(f"{ngn_amount} NGN is approximately {usdc_from_ngn:.2f} USDC\n")
    else:
        print(f"Could not convert NGN to USDC.\n")

    kes_amount = 5000
    usdc_from_kes = exchange_util.convert_to_usdc(kes_amount, "KES")
    if usdc_from_kes is not None:
        print(f"{kes_amount} KES is approximately {usdc_from_kes:.2f} USDC\n")
    else:
        print(f"Could not convert KES to USDC.\n")

    print("--- Testing USDC to Fiat Conversion (User Sells USDC) ---")
    usdc_to_sell = 100
    ngn_from_usdc = exchange_util.convert_from_usdc(usdc_to_sell, "NGN")
    if ngn_from_usdc is not None:
        print(f"{usdc_to_sell} USDC is approximately {ngn_from_usdc:.2f} NGN\n")
    else:
        print(f"Could not convert USDC to NGN.\n")
        
    ghs_from_usdc = exchange_util.convert_from_usdc(usdc_to_sell, "GHS")
    if ghs_from_usdc is not None:
        print(f"{usdc_to_sell} USDC is approximately {ghs_from_usdc:.2f} GHS\n")
    else:
        print(f"Could not convert USDC to GHS.\n")

    # Example of direct rate fetching (conceptual, may use mock if use_mock=True)
    print("--- Direct Rate Fetching Example (BUY USDC with NGN) ---")
    rate_ngn_usdc_buy = exchange_util.get_live_fx_rate_binance_p2p(fiat_currency="NGN", asset="USDC", trade_type="BUY")
    if rate_ngn_usdc_buy:
        print(f"Rate to BUY 1 USDC with NGN: {rate_ngn_usdc_buy} NGN\n")
    else:
        print(f"Could not fetch rate to BUY USDC with NGN.\n")

    print("--- Direct Rate Fetching Example (SELL USDC for KES) ---")
    rate_usdc_kes_sell = exchange_util.get_live_fx_rate_binance_p2p(fiat_currency="KES", asset="USDC", trade_type="SELL")
    if rate_usdc_kes_sell:
        print(f"Rate to SELL 1 USDC for KES: {rate_usdc_kes_sell} KES\n")
    else:
        print(f"Could not fetch rate to SELL USDC for KES.\n")

