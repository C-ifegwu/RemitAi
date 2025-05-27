import time
import json
from typing import Dict, Any

# This would interact with the Soroban SDK or a similar library in a real Rust environment
# For Python, we'll mock the interaction.
class MockSorobanContractInterface:
    def __init__(self, contract_id: str):
        self.contract_id = contract_id
        self.locked_funds: Dict[str, Dict[str, Any]] = {}
        print(f"MockSorobanContractInterface initialized for contract: {contract_id}")

    def trigger_withdrawal_lock(self, user_wallet: str, transaction_id: str, usdc_amount: float) -> Dict[str, Any]:
        """
        Simulates triggering a function on the SmartWallet contract to lock USDC for withdrawal.
        In a real scenario, this would be an actual contract call.
        It would verify user balance, lock funds, and potentially emit an event.
        """
        print(f"[Contract {self.contract_id}] Attempting to lock {usdc_amount} USDC for user {user_wallet}, tx_id: {transaction_id}")
        # Mock balance check (not implemented here, assume sufficient)
        if transaction_id in self.locked_funds:
            print(f"[Contract {self.contract_id}] Error: Transaction ID {transaction_id} already has funds locked.")
            return {"success": False, "error": "Transaction ID already processed"}

        self.locked_funds[transaction_id] = {
            "user_wallet": user_wallet,
            "usdc_amount": usdc_amount,
            "status": "locked_for_withdrawal",
            "timestamp": time.time()
        }
        print(f"[Contract {self.contract_id}] Successfully locked {usdc_amount} USDC for tx_id: {transaction_id}")
        return {"success": True, "message": "Funds locked successfully", "lock_details": self.locked_funds[transaction_id]}

    def confirm_withdrawal_debit(self, transaction_id: str) -> Dict[str, Any]:
        """
        Simulates confirming the debit of USDC after successful fiat payout.
        This would typically be called after a webhook confirms payout.
        """
        print(f"[Contract {self.contract_id}] Attempting to confirm debit for tx_id: {transaction_id}")
        if transaction_id not in self.locked_funds or self.locked_funds[transaction_id]["status"] != "locked_for_withdrawal":
            print(f"[Contract {self.contract_id}] Error: No funds locked or invalid status for tx_id: {transaction_id}")
            return {"success": False, "error": "No funds locked or invalid status for this transaction"}

        self.locked_funds[transaction_id]["status"] = "debited_withdrawal_complete"
        self.locked_funds[transaction_id]["debit_timestamp"] = time.time()
        print(f"[Contract {self.contract_id}] Successfully debited funds for tx_id: {transaction_id}")
        # In a real contract, the funds would now be transferred out or made inaccessible to the user.
        return {"success": True, "message": "Funds debited successfully", "debit_details": self.locked_funds[transaction_id]}
    
    def release_locked_funds(self, transaction_id: str) -> Dict[str, Any]:
        """
        Simulates releasing locked funds if a withdrawal fails or expires.
        """
        print(f"[Contract {self.contract_id}] Attempting to release locked funds for tx_id: {transaction_id}")
        if transaction_id not in self.locked_funds or self.locked_funds[transaction_id]["status"] != "locked_for_withdrawal":
            print(f"[Contract {self.contract_id}] Error: No funds locked or invalid status for tx_id: {transaction_id} to release.")
            return {"success": False, "error": "No funds locked or invalid status for release"}

        self.locked_funds[transaction_id]["status"] = "released_withdrawal_failed"
        self.locked_funds[transaction_id]["release_timestamp"] = time.time()
        print(f"[Contract {self.contract_id}] Successfully released funds for tx_id: {transaction_id}")
        return {"success": True, "message": "Funds released successfully", "release_details": self.locked_funds[transaction_id]}

class WithdrawalConfirmationService:
    def __init__(self, smart_wallet_contract_id: str):
        # In a real application, this would be configured with the actual contract ID
        self.smart_wallet_contract = MockSorobanContractInterface(smart_wallet_contract_id)
        self.offramp_transactions: Dict[str, Dict[str, Any]] = {}
        print("WithdrawalConfirmationService initialized.")

    def initiate_usdc_withdrawal_on_contract(self, offramp_transaction_id: str, user_wallet_address: str, usdc_amount: float) -> Dict[str, Any]:
        """
        Coordinates with the smart contract to lock USDC for withdrawal.
        This would be called by the OffRampService after it has confirmed details with the user
        and before instructing the user to send USDC (or if USDC is already in the smart wallet).
        """
        print(f"[WCService] Initiating USDC withdrawal lock on contract for offramp_tx_id: {offramp_transaction_id}")
        # Assume offramp_transaction_id is unique and used as the reference on the contract
        lock_result = self.smart_wallet_contract.trigger_withdrawal_lock(
            user_wallet=user_wallet_address, 
            transaction_id=offramp_transaction_id, 
            usdc_amount=usdc_amount
        )
        
        if lock_result["success"]:
            self.offramp_transactions[offramp_transaction_id] = {
                "status": "contract_funds_locked",
                "user_wallet": user_wallet_address,
                "usdc_amount": usdc_amount,
                "contract_lock_details": lock_result["lock_details"],
                "initiated_at": time.time()
            }
            print(f"[WCService] Contract funds successfully locked for {offramp_transaction_id}.")
        else:
            print(f"[WCService] Failed to lock funds on contract for {offramp_transaction_id}: {lock_result.get('error')}")
            self.offramp_transactions[offramp_transaction_id] = {
                "status": "contract_lock_failed",
                "error": lock_result.get("error"),
                "initiated_at": time.time()
            }
        return lock_result

    def process_fiat_payout_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes an incoming webhook from a fiat payout provider (e.g., Flutterwave).
        Expected webhook_data: {
            "transaction_id": "offtx_12345...", // This is the ID from OffRampService
            "provider_reference": "flutterwave_tx_abc...",
            "status": "SUCCESSFUL" or "FAILED",
            "amount_paid_fiat": 12781.65,
            "currency_paid": "KES",
            "timestamp": "2025-05-15T14:30:00Z"
        }
        """
        print(f"[WCService] Received fiat payout webhook: {json.dumps(webhook_data)}")
        offramp_tx_id = webhook_data.get("transaction_id")
        payout_status = webhook_data.get("status")

        if not offramp_tx_id or not payout_status:
            print("[WCService] Webhook missing transaction_id or status.")
            return {"success": False, "error": "Missing transaction_id or status in webhook"}

        if offramp_tx_id not in self.offramp_transactions or self.offramp_transactions[offramp_tx_id]["status"] != "contract_funds_locked":
            print(f"[WCService] Transaction {offramp_tx_id} not found or not in expected state (contract_funds_locked). Current state: {self.offramp_transactions.get(offramp_tx_id, {}).get('status')}")
            # Potentially handle cases where webhook arrives before contract lock is recorded, or out of order.
            # For now, assume it must be in contract_funds_locked state.
            return {"success": False, "error": "Transaction not found or not in expected state for webhook processing"}

        if payout_status == "SUCCESSFUL":
            print(f"[WCService] Fiat payout SUCCESSFUL for {offramp_tx_id}. Confirming USDC debit on contract.")
            debit_result = self.smart_wallet_contract.confirm_withdrawal_debit(offramp_tx_id)
            if debit_result["success"]:
                self.offramp_transactions[offramp_tx_id]["status"] = "fiat_payout_confirmed_usdc_debited"
                self.offramp_transactions[offramp_tx_id]["webhook_data"] = webhook_data
                self.offramp_transactions[offramp_tx_id]["finalized_at"] = time.time()
                print(f"[WCService] USDC debit confirmed for {offramp_tx_id}.")
                return {"success": True, "message": "Webhook processed, USDC debit confirmed."}
            else:
                self.offramp_transactions[offramp_tx_id]["status"] = "fiat_payout_successful_debit_failed"
                self.offramp_transactions[offramp_tx_id]["webhook_data"] = webhook_data
                self.offramp_transactions[offramp_tx_id]["error_details"] = debit_result.get("error")
                print(f"[WCService] CRITICAL: Fiat payout was successful for {offramp_tx_id}, but FAILED to debit USDC on contract: {debit_result.get('error')}")
                # This state requires manual intervention/alerting
                return {"success": False, "error": "Fiat payout successful, but contract debit failed. Manual intervention required.", "details": debit_result}
        elif payout_status == "FAILED":
            print(f"[WCService] Fiat payout FAILED for {offramp_tx_id}. Releasing locked USDC on contract.")
            release_result = self.smart_wallet_contract.release_locked_funds(offramp_tx_id)
            if release_result["success"]:
                self.offramp_transactions[offramp_tx_id]["status"] = "fiat_payout_failed_usdc_released"
                self.offramp_transactions[offramp_tx_id]["webhook_data"] = webhook_data
                self.offramp_transactions[offramp_tx_id]["finalized_at"] = time.time()
                print(f"[WCService] Locked USDC released for {offramp_tx_id}.")
                return {"success": True, "message": "Webhook processed, fiat payout failed, USDC released."}
            else:
                self.offramp_transactions[offramp_tx_id]["status"] = "fiat_payout_failed_release_failed"
                self.offramp_transactions[offramp_tx_id]["webhook_data"] = webhook_data
                self.offramp_transactions[offramp_tx_id]["error_details"] = release_result.get("error")
                print(f"[WCService] CRITICAL: Fiat payout FAILED for {offramp_tx_id}, and FAILED to release locked USDC: {release_result.get('error')}")
                # This state requires manual intervention/alerting
                return {"success": False, "error": "Fiat payout failed, and contract fund release failed. Manual intervention required.", "details": release_result}
        else:
            print(f"[WCService] Unknown payout status \"{payout_status}\" in webhook for {offramp_tx_id}.")
            return {"success": False, "error": f"Unknown payout status: {payout_status}"}

# Example Usage:
if __name__ == "__main__":
    # Assume a SmartWallet contract ID (this would be a real ID on Soroban)
    MOCK_CONTRACT_ID = "CADXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    wc_service = WithdrawalConfirmationService(smart_wallet_contract_id=MOCK_CONTRACT_ID)

    # Simulate an off-ramp initiation (this would typically be part of OffRampService flow)
    test_offramp_tx_id = "offtx_test_12345"
    test_user_wallet = "GABC...XYZ"
    test_usdc_amount = 50.0

    print(f"\n--- Simulating Contract Lock for Withdrawal {test_offramp_tx_id} ---")
    lock_response = wc_service.initiate_usdc_withdrawal_on_contract(
        offramp_transaction_id=test_offramp_tx_id,
        user_wallet_address=test_user_wallet,
        usdc_amount=test_usdc_amount
    )
    print(f"Contract Lock Response: {json.dumps(lock_response)}")
    print(f"WCService Transaction State: {json.dumps(wc_service.offramp_transactions.get(test_offramp_tx_id))}")

    if lock_response["success"]:
        # Simulate receiving a SUCCESSFUL payout webhook
        print(f"\n--- Simulating SUCCESSFUL Fiat Payout Webhook for {test_offramp_tx_id} ---")
        successful_webhook = {
            "transaction_id": test_offramp_tx_id,
            "provider_reference": "flutterwave_tx_success_abc",
            "status": "SUCCESSFUL",
            "amount_paid_fiat": 6400.00,
            "currency_paid": "KES",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        webhook_response_success = wc_service.process_fiat_payout_webhook(successful_webhook)
        print(f"Webhook Processing Response (Success): {json.dumps(webhook_response_success)}")
        print(f"WCService Transaction State: {json.dumps(wc_service.offramp_transactions.get(test_offramp_tx_id))}")
        print(f"Contract Locked Funds State: {json.dumps(wc_service.smart_wallet_contract.locked_funds.get(test_offramp_tx_id))}")

    # Simulate another transaction for FAILED payout
    test_offramp_tx_id_fail = "offtx_test_67890"
    print(f"\n--- Simulating Contract Lock for Withdrawal {test_offramp_tx_id_fail} ---")
    lock_response_fail = wc_service.initiate_usdc_withdrawal_on_contract(
        offramp_transaction_id=test_offramp_tx_id_fail,
        user_wallet_address=test_user_wallet,
        usdc_amount=25.0
    )
    print(f"Contract Lock Response: {json.dumps(lock_response_fail)}")

    if lock_response_fail["success"]:
        print(f"\n--- Simulating FAILED Fiat Payout Webhook for {test_offramp_tx_id_fail} ---")
        failed_webhook = {
            "transaction_id": test_offramp_tx_id_fail,
            "provider_reference": "flutterwave_tx_fail_xyz",
            "status": "FAILED",
            "reason": "User bank account invalid",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        webhook_response_fail = wc_service.process_fiat_payout_webhook(failed_webhook)
        print(f"Webhook Processing Response (Fail): {json.dumps(webhook_response_fail)}")
        print(f"WCService Transaction State: {json.dumps(wc_service.offramp_transactions.get(test_offramp_tx_id_fail))}")
        print(f"Contract Locked Funds State: {json.dumps(wc_service.smart_wallet_contract.locked_funds.get(test_offramp_tx_id_fail))}")
