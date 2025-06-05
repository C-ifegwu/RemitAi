#![no_std]
use soroban_sdk::{
    contract, contractimpl, contracttype, symbol_short, token, Address, Env, Map, String, Val, Vec
};

// Define storage keys
#[derive(Clone)]
#[contracttype]
pub enum DataKey {
    Admin,          // Address of the paymaster admin
    Token,          // Address of the token used for payments (e.g., USDC or XLM)
    SponsorshipRules, // Map<Address, bool> - Addresses allowed for sponsorship (example rule)
}

// Helper to get admin address
fn get_admin(env: &Env) -> Address {
    env.storage().instance().get(&DataKey::Admin).unwrap()
}

// Helper to check if caller is admin
fn is_admin(env: &Env, caller: &Address) -> bool {
    get_admin(env) == *caller
}

#[contract]
pub struct PaymasterContract;

#[contractimpl]
impl PaymasterContract {
    /// Initialize the paymaster contract with an admin and the payment token address.
    pub fn initialize(env: Env, admin: Address, token: Address) {
        if env.storage().instance().has(&DataKey::Admin) {
            panic!("Contract already initialized");
        }
        env.storage().instance().set(&DataKey::Admin, &admin);
        env.storage().instance().set(&DataKey::Token, &token);
        env.storage().instance().set(&DataKey::SponsorshipRules, &Map::<Address, bool>::new(&env));

        // Set TTL for instance storage
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Admin function to add an address to the sponsorship allowlist.
    pub fn allow_address(env: Env, caller: Address, address_to_allow: Address) {
        caller.require_auth();
        if !is_admin(&env, &caller) {
            panic!("Caller is not the admin");
        }

        let mut rules: Map<Address, bool> = env.storage().instance().get(&DataKey::SponsorshipRules).unwrap();
        rules.set(address_to_allow, true);
        env.storage().instance().set(&DataKey::SponsorshipRules, &rules);
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Admin function to remove an address from the sponsorship allowlist.
    pub fn disallow_address(env: Env, caller: Address, address_to_disallow: Address) {
        caller.require_auth();
        if !is_admin(&env, &caller) {
            panic!("Caller is not the admin");
        }

        let mut rules: Map<Address, bool> = env.storage().instance().get(&DataKey::SponsorshipRules).unwrap();
        rules.remove(address_to_disallow);
        env.storage().instance().set(&DataKey::SponsorshipRules, &rules);
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// The core paymaster function called by Soroban during transaction submission.
    /// Determines if the transaction should be sponsored.
    /// `_signature_payload`: The payload signed by the user for the transaction.
    /// `_user_signature`: The user's signature over the payload.
    /// `tx_context`: Contextual information about the transaction being submitted.
    pub fn pay(
        env: Env,
        _signature_payload: Val, // Placeholder for actual type if API changes
        _user_signature: Val,    // Placeholder for actual type if API changes
        tx_context: Val,       // Placeholder for actual type if API changes
    ) {
        // --- Authorization --- 
        // Ensure this paymaster contract itself is authorized to pay.
        // This might involve checking its own balance or other internal state.
        let contract_address = env.current_contract_address();
        contract_address.require_auth(); // The paymaster must authorize itself to pay.

        // --- Sponsorship Logic --- 
        // Extract relevant info from tx_context (e.g., source account, operations).
        // This part is highly dependent on the exact structure of `tx_context` provided by Soroban.
        // For this example, let's assume we can get the transaction source address.
        // !!! THIS IS A PLACEHOLDER - ACTUAL IMPLEMENTATION DEPENDS ON SOROBAN API !!!
        let tx_source_account: Address = Self::extract_source_account(&env, &tx_context);

        // Check if the source account is in our allowlist.
        let rules: Map<Address, bool> = env.storage().instance().get(&DataKey::SponsorshipRules).unwrap();
        if !rules.get(tx_source_account.clone()).unwrap_or(false) {
            panic!("Transaction source not allowed for sponsorship");
        }

        // --- Fee Payment Logic --- 
        // If sponsorship is approved, the Soroban runtime handles the fee payment
        // using this contract's funds after this function successfully completes.
        // We might need to check the paymaster's balance here.
        let token_address: Address = env.storage().instance().get(&DataKey::Token).unwrap();
        let token_client = token::Client::new(&env, &token_address);
        let required_fee = Self::extract_required_fee(&env, &tx_context); // Placeholder

        if token_client.balance(&contract_address) < required_fee {
            panic!("Paymaster has insufficient funds to sponsor this transaction");
        }

        // If all checks pass, the function completes, and Soroban proceeds with sponsorship.
        env.events().publish((symbol_short!("pay"), tx_source_account), required_fee);

        // Extend TTL
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Placeholder function to simulate extracting the source account from transaction context.
    /// !!! Replace with actual Soroban API call when available !!!
    fn extract_source_account(_env: &Env, _tx_context: &Val) -> Address {
        // In a real scenario, this would parse the tx_context.
        // Returning a dummy address for now.
        Address::from_string(&String::from_str(_env, "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF"))
    }

    /// Placeholder function to simulate extracting the required fee from transaction context.
    /// !!! Replace with actual Soroban API call when available !!!
    fn extract_required_fee(_env: &Env, _tx_context: &Val) -> i128 {
        // In a real scenario, this would parse the tx_context.
        // Returning a dummy fee for now.
        100_0000000 // Example fee (e.g., 0.1 XLM or USDC)
    }

    /// Deposit funds into the paymaster contract to cover future fees.
    /// Requires authorization from the depositor.
    pub fn deposit(env: Env, from: Address, amount: i128) {
        from.require_auth();
        if amount <= 0 {
            panic!("Amount must be positive");
        }
        let token_address: Address = env.storage().instance().get(&DataKey::Token).unwrap();
        let token_client = token::Client::new(&env, &token_address);
        token_client.transfer(&from, &env.current_contract_address(), &amount);
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Admin function to withdraw surplus funds from the paymaster.
    pub fn withdraw(env: Env, caller: Address, to: Address, amount: i128) {
        caller.require_auth();
        if !is_admin(&env, &caller) {
            panic!("Caller is not the admin");
        }
        if amount <= 0 {
            panic!("Amount must be positive");
        }
        let token_address: Address = env.storage().instance().get(&DataKey::Token).unwrap();
        let token_client = token::Client::new(&env, &token_address);
        let contract_address = env.current_contract_address();
        if token_client.balance(&contract_address) < amount {
            panic!("Insufficient balance");
        }
        token_client.transfer(&contract_address, &to, &amount);
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

     /// Get the current balance of the paymaster contract.
    pub fn balance(env: Env) -> i128 {
        let token_address: Address = env.storage().instance().get(&DataKey::Token).unwrap();
        let token_client = token::Client::new(&env, &token_address);
        token_client.balance(&env.current_contract_address())
    }

    /// Get the admin address.
    pub fn admin(env: Env) -> Address {
        get_admin(&env)
    }
}

mod test;

