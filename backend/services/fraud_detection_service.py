import time
from collections import defaultdict, deque

# Mock database to store recent command history for fraud detection
# In a real application, use a more robust and scalable data store (e.g., Redis, a database).
MOCK_COMMAND_HISTORY = defaultdict(lambda: deque(maxlen=10)) # Store last 10 commands per user_id
MOCK_TRANSACTION_PATTERNS = defaultdict(lambda: {
    "timestamps": deque(maxlen=20), # Timestamps of recent transactions
    "recipient_counts": defaultdict(lambda: deque(maxlen=5)) # Timestamps for each recipient
})

# Thresholds for fraud detection (configurable in a real system)
DUPLICATE_COMMAND_TIME_WINDOW_SECONDS = 60  # 1 minute
DUPLICATE_COMMAND_MIN_SIMILARITY_SCORE = 0.9 # For text similarity (not implemented in this mock, using exact match)
MAX_COMMANDS_IN_WINDOW_FOR_DUPLICATE = 2 # More than 2 identical commands in window is suspicious

SPAM_TRANSACTION_FREQUENCY_WINDOW_SECONDS = 300 # 5 minutes
SPAM_MAX_TRANSACTIONS_IN_WINDOW = 10 # More than 10 transactions in 5 mins is suspicious
SPAM_MAX_NEW_RECIPIENTS_IN_WINDOW = 5 # Transactions to >5 new recipients in 5 mins is suspicious
SPAM_LOW_VALUE_THRESHOLD = 1.0 # Transactions below this amount might be part of spam (if frequent)

class FraudDetectionService:

    def __init__(self):
        self.command_history = MOCK_COMMAND_HISTORY
        self.transaction_patterns = MOCK_TRANSACTION_PATTERNS

    def _are_commands_similar(self, cmd1_text: str, cmd2_text: str) -> bool:
        """Mock similarity check. In a real app, use NLP techniques (e.g., Levenshtein, embeddings)."""
        # For this mock, we use exact match for simplicity after basic normalization.
        return cmd1_text.strip().lower() == cmd2_text.strip().lower()

    def check_duplicate_command(self, user_id: str, command_text: str, timestamp: float = None) -> tuple[bool, str]:
        """Checks for potentially duplicate commands made in rapid succession.

        Args:
            user_id: The unique identifier for the user.
            command_text: The transcribed text of the command.
            timestamp: The time the command was issued (Unix timestamp).

        Returns:
            A tuple (is_suspicious: bool, reason: str).
        """
        if timestamp is None:
            timestamp = time.time()

        history = self.command_history[user_id]
        duplicate_count = 0
        
        for prev_cmd_time, prev_cmd_text in list(history): # Iterate over a copy for safe modification if needed
            if (timestamp - prev_cmd_time) <= DUPLICATE_COMMAND_TIME_WINDOW_SECONDS:
                if self._are_commands_similar(command_text, prev_cmd_text):
                    duplicate_count += 1
            else:
                # Remove very old commands from consideration to keep deque size relevant
                # Though deque maxlen handles this, explicit removal can be done if needed for other logic
                pass 

        # Add current command to history *after* checking against past ones
        history.append((timestamp, command_text))

        if duplicate_count >= MAX_COMMANDS_IN_WINDOW_FOR_DUPLICATE: # Current command makes it N+1
            reason = (f"Potential duplicate command: Similar command issued {duplicate_count + 1} "
                      f"times within {DUPLICATE_COMMAND_TIME_WINDOW_SECONDS} seconds.")
            print(f"[FRAUD_DETECTION] User {user_id}: {reason}")
            return True, reason
        
        return False, "No duplicate command detected."

    def check_spam_transaction_patterns(self, user_id: str, amount: float, recipient_id: str, timestamp: float = None) -> tuple[bool, str]:
        """Checks for spam-like transaction patterns.

        Args:
            user_id: The unique identifier for the user.
            amount: The transaction amount.
            recipient_id: The unique identifier for the recipient.
            timestamp: The time of the transaction (Unix timestamp).

        Returns:
            A tuple (is_suspicious: bool, reason: str).
        """
        if timestamp is None:
            timestamp = time.time()

        user_patterns = self.transaction_patterns[user_id]
        user_patterns["timestamps"].append(timestamp)
        user_patterns["recipient_counts"][recipient_id].append(timestamp)

        # Rule 1: High frequency of transactions
        recent_tx_timestamps = [t for t in user_patterns["timestamps"] if (timestamp - t) <= SPAM_TRANSACTION_FREQUENCY_WINDOW_SECONDS]
        if len(recent_tx_timestamps) > SPAM_MAX_TRANSACTIONS_IN_WINDOW:
            reason = (f"Potential spam: High transaction frequency ({len(recent_tx_timestamps)} transactions "
                      f"within {SPAM_TRANSACTION_FREQUENCY_WINDOW_SECONDS} seconds).")
            print(f"[FRAUD_DETECTION] User {user_id}: {reason}")
            return True, reason

        # Rule 2: Transactions to many new/distinct recipients in a short period
        # (Simplified: counts distinct recipients with recent activity)
        active_recipients_in_window = 0
        for r_id, r_timestamps in user_patterns["recipient_counts"].items():
            if any((timestamp - rt) <= SPAM_TRANSACTION_FREQUENCY_WINDOW_SECONDS for rt in r_timestamps):
                active_recipients_in_window += 1
        
        if active_recipients_in_window > SPAM_MAX_NEW_RECIPIENTS_IN_WINDOW:
            reason = (f"Potential spam: Transactions to many distinct recipients ({active_recipients_in_window}) "
                      f"within {SPAM_TRANSACTION_FREQUENCY_WINDOW_SECONDS} seconds.")
            print(f"[FRAUD_DETECTION] User {user_id}: {reason}")
            return True, reason

        # Rule 3: High frequency of low-value transactions (can be combined with Rule 1)
        if amount < SPAM_LOW_VALUE_THRESHOLD and len(recent_tx_timestamps) > (SPAM_MAX_TRANSACTIONS_IN_WINDOW / 2):
            reason = (f"Potential spam: High frequency of low-value transactions (amount: {amount}, "
                      f"count: {len(recent_tx_timestamps)} within window).")
            print(f"[FRAUD_DETECTION] User {user_id}: {reason}")
            return True, reason

        return False, "No spam transaction pattern detected."

    def assess_transaction_risk(self, user_id: str, command_text: str, amount: float, recipient_id: str) -> dict:
        """Assesses overall risk for a given transaction based on command and pattern checks."""
        timestamp = time.time()
        
        is_duplicate, duplicate_reason = self.check_duplicate_command(user_id, command_text, timestamp)
        is_spam, spam_reason = self.check_spam_transaction_patterns(user_id, amount, recipient_id, timestamp)

        risk_score = 0 # Lower is better
        reasons = []

        if is_duplicate:
            risk_score += 50
            reasons.append(duplicate_reason)
        if is_spam:
            risk_score += 50
            reasons.append(spam_reason)
        
        return {
            "user_id": user_id,
            "is_suspicious": risk_score > 0,
            "risk_score": risk_score, # Max 100 for this mock
            "reasons": reasons,
            "timestamp": timestamp
        }

# Example Usage (for testing)
if __name__ == "__main__":
    service = FraudDetectionService()
    user1 = "user_fraud_test_001"

    print("--- Testing Duplicate Command Detection ---")
    cmd1 = "Send 10 USD to John Doe"
    print(f"Cmd1: {cmd1}")
    print(service.assess_transaction_risk(user1, cmd1, 10.0, "john_doe_1"))
    time.sleep(0.1) # Simulate small delay
    print(f"Cmd2 (same): {cmd1}")
    print(service.assess_transaction_risk(user1, cmd1, 10.0, "john_doe_1")) # Should not be duplicate yet
    time.sleep(0.1)
    print(f"Cmd3 (same): {cmd1}")
    print(service.assess_transaction_risk(user1, cmd1, 10.0, "john_doe_1")) # Now should be duplicate

    cmd_variant = "send 10 usd to john doe " # Test normalization
    print(f"Cmd4 (variant): {cmd_variant}")
    print(service.assess_transaction_risk(user1, cmd_variant, 10.0, "john_doe_1"))

    # Simulate time passing beyond window for duplicate check
    print("\nSimulating time passing for duplicate check reset...")
    service.command_history[user1].append((time.time() - DUPLICATE_COMMAND_TIME_WINDOW_SECONDS * 2, "old command"))
    print(f"Cmd5 (same after long time): {cmd1}")
    # Reset history for this specific test or use a new user
    service.command_history[user1].clear() 
    print(service.assess_transaction_risk(user1, cmd1, 10.0, "john_doe_1")) # First again
    print(service.assess_transaction_risk(user1, cmd1, 10.0, "john_doe_1")) # Second
    print(service.assess_transaction_risk(user1, cmd1, 10.0, "john_doe_1")) # Third, now duplicate


    print("\n--- Testing Spam Transaction Pattern Detection ---")
    user2 = "user_fraud_test_002"
    # High frequency
    print("Simulating high frequency transactions...")
    for i in range(SPAM_MAX_TRANSACTIONS_IN_WINDOW + 1):
        res = service.assess_transaction_risk(user2, f"tx {i}", 5.0, f"recipient_{i % 3}")
        if res["is_suspicious"] and any("High transaction frequency" in r for r in res["reasons"]):
            print(f"Transaction {i+1}: {res}")
            break
        time.sleep(0.01)
    
    # Many new recipients
    print("\nSimulating transactions to many new recipients...")
    user3 = "user_fraud_test_003"
    for i in range(SPAM_MAX_NEW_RECIPIENTS_IN_WINDOW + 1):
        res = service.assess_transaction_risk(user3, f"tx_new_recip {i}", 20.0, f"new_recipient_{i}")
        if res["is_suspicious"] and any("many distinct recipients" in r for r in res["reasons"]):
            print(f"Transaction {i+1} to new recipient: {res}")
            break
        time.sleep(0.01)

    # Low value, high frequency
    print("\nSimulating low-value, high-frequency transactions...")
    user4 = "user_fraud_test_004"
    # Need to hit more than half of SPAM_MAX_TRANSACTIONS_IN_WINDOW
    trigger_count = (SPAM_MAX_TRANSACTIONS_IN_WINDOW // 2) + 2 
    for i in range(trigger_count):
        res = service.assess_transaction_risk(user4, f"low_val_tx {i}", SPAM_LOW_VALUE_THRESHOLD - 0.1, f"recipient_low_val_{i % 2}")
        if res["is_suspicious"] and any("low-value transactions" in r for r in res["reasons"]):
            print(f"Low-value transaction {i+1}: {res}")
            break
        time.sleep(0.01)

    print("\n--- Testing Combined Risk ---")
    user5 = "user_fraud_test_005"
    # Make some commands to trigger duplicate later
    service.assess_transaction_risk(user5, "Urgent payment now", 100.0, "recip_A")
    service.assess_transaction_risk(user5, "Urgent payment now", 100.0, "recip_A")
    # Now, a third command that is duplicate, and also part of a rapid sequence of low value txns
    for i in range(trigger_count):
        final_command = "Urgent payment now" if i == (trigger_count -1) else f"small tx {i}"
        amount = 0.5 if i == (trigger_count -1) else 0.5 # ensure low value for the last one
        res = service.assess_transaction_risk(user5, final_command, amount, f"recip_spam_{i}")
        if res["is_suspicious"] and len(res["reasons"]) > 1:
            print(f"Combined risk transaction {i+1}: {res}")
            break
        time.sleep(0.01)

