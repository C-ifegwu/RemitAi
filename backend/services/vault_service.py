import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from ..api.v1.schemas.vault_schemas import VaultCreate, Vault, VaultStatusResponse

# --- Mock Data Store --- 
# In a real application, this would be a database.
# Key: user_id, Value: Dict[vault_id, Vault]
mock_vault_db: Dict[str, Dict[str, Vault]] = {}

# --- Mock Conversion Rates --- 
# In a real application, fetch this from an API.
MOCK_RATES = {
    "NGN_USD": 1/1500.0,
    "KES_USD": 1/130.0,
    "USD_NGN": 1550.0, # Slightly different for withdrawal simulation
    "USD_KES": 135.0,
}

# --- Mock Yield Rate (Annual) ---
MOCK_ANNUAL_YIELD_RATE = 0.05 # 5% annual yield

class VaultService:

    def _get_mock_conversion_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        key = f"{from_currency}_{to_currency}"
        return MOCK_RATES.get(key)

    def _calculate_mock_yield(self, usdc_amount: float, duration_days: int) -> float:
        daily_rate = MOCK_ANNUAL_YIELD_RATE / 365.0
        mock_yield = usdc_amount * daily_rate * duration_days
        return round(mock_yield, 2)

    def create_vault(self, user_id: str, vault_data: VaultCreate) -> Optional[Vault]:
        """Creates a new vault with mocked conversion and yield calculation."""
        # Mock conversion to USDC
        rate_to_usd = self._get_mock_conversion_rate(vault_data.local_currency, "USD")
        if rate_to_usd is None:
            print(f"Error: Mock conversion rate not found for {vault_data.local_currency} to USD")
            # In a real app, raise an HTTPException
            return None 
        usdc_amount = round(vault_data.local_amount * rate_to_usd, 2)

        # Calculate dates
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=vault_data.lock_duration_days)
        vault_id = str(uuid.uuid4())

        # Calculate mock yield
        mock_yield = self._calculate_mock_yield(usdc_amount, vault_data.lock_duration_days)

        new_vault = Vault(
            id=vault_id,
            user_id=user_id,
            local_currency=vault_data.local_currency,
            local_amount=vault_data.local_amount,
            lock_duration_days=vault_data.lock_duration_days,
            usdc_amount=usdc_amount,
            start_date=start_date,
            end_date=end_date,
            status="LOCKED",
            mock_yield_earned=mock_yield
        )

        # Store in mock DB
        if user_id not in mock_vault_db:
            mock_vault_db[user_id] = {}
        mock_vault_db[user_id][vault_id] = new_vault
        print(f"Vault created: {new_vault.dict()}") # Debugging
        return new_vault

    def get_vault_status(self, user_id: str, vault_id: str) -> Optional[VaultStatusResponse]:
        """Gets the status of a specific vault."""
        user_vaults = mock_vault_db.get(user_id, {})
        vault = user_vaults.get(vault_id)

        if not vault:
            return None

        now = datetime.utcnow()
        is_withdrawable = vault.status == "LOCKED" and now >= vault.end_date
        current_withdrawal_value = None

        if is_withdrawable:
            vault.status = "UNLOCKED" # Update status if time has passed
            rate_from_usd = self._get_mock_conversion_rate("USD", vault.local_currency)
            if rate_from_usd:
                total_usdc = vault.usdc_amount + vault.mock_yield_earned
                current_withdrawal_value = round(total_usdc * rate_from_usd, 2)

        return VaultStatusResponse(
            id=vault.id,
            local_currency=vault.local_currency,
            original_local_amount=vault.local_amount,
            usdc_amount=vault.usdc_amount,
            start_date=vault.start_date,
            end_date=vault.end_date,
            status=vault.status,
            mock_yield_earned=vault.mock_yield_earned,
            is_withdrawable=is_withdrawable,
            mock_current_withdrawal_value_local=current_withdrawal_value
        )

    def list_user_vaults(self, user_id: str) -> List[VaultStatusResponse]:
        """Lists all vaults for a given user."""
        user_vaults_dict = mock_vault_db.get(user_id, {})
        status_list = []
        for vault_id in user_vaults_dict.keys():
            status = self.get_vault_status(user_id, vault_id)
            if status:
                status_list.append(status)
        return status_list

    def withdraw_vault(self, user_id: str, vault_id: str) -> Optional[Dict]:
        """Withdraws funds from an unlocked vault."""
        user_vaults = mock_vault_db.get(user_id, {})
        vault = user_vaults.get(vault_id)

        if not vault:
            return {"error": "Vault not found"}

        now = datetime.utcnow()
        if vault.status == "WITHDRAWN":
             return {"error": "Vault already withdrawn"}
             
        if vault.status == "LOCKED" and now < vault.end_date:
            return {"error": f"Vault is locked until {vault.end_date.isoformat()}"}

        # Mark as unlocked if time is up
        if vault.status == "LOCKED" and now >= vault.end_date:
             vault.status = "UNLOCKED"

        if vault.status != "UNLOCKED":
             return {"error": f"Vault not in withdrawable state (Status: {vault.status})"}

        # Perform mock withdrawal conversion
        rate_from_usd = self._get_mock_conversion_rate("USD", vault.local_currency)
        if rate_from_usd is None:
            return {"error": f"Mock conversion rate not found for USD to {vault.local_currency}"}

        total_usdc_withdrawn = vault.usdc_amount + vault.mock_yield_earned
        final_local_amount = round(total_usdc_withdrawn * rate_from_usd, 2)

        # Update vault status in mock DB
        vault.status = "WITHDRAWN"
        vault.mock_withdrawal_local_amount = final_local_amount
        mock_vault_db[user_id][vault_id] = vault # Update the stored vault

        return {
            "message": "Withdrawal successful",
            "vault_id": vault_id,
            "withdrawn_usdc_amount": round(total_usdc_withdrawn, 2),
            "mock_final_local_amount": final_local_amount,
            "status": vault.status
        }

# Instantiate the service for use in endpoints
vault_service = VaultService()

