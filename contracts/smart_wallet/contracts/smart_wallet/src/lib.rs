#![no_std]
use soroban_sdk::{contract, contractimpl, contracttype, token, Address, Env};

#[derive(Clone)]
#[contracttype]
pub enum DataKey {
    Owner,      // Address of the wallet owner
    Token,      // Address of the USDC token contract
}

fn get_owner(env: &Env) -> Address {
    env.storage().instance().get(&DataKey::Owner).unwrap()
}

fn get_token_client(env: &Env) -> token::Client {
    let token_address = env.storage().instance().get(&DataKey::Token).unwrap();
    token::Client::new(env, &token_address)
}

#[contract]
pub struct SmartWalletContract;

#[contractimpl]
impl SmartWalletContract {
    /// Initialize the contract with the owner and the USDC token address.
    /// Can only be called once.
    pub fn initialize(env: Env, owner: Address, token: Address) {
        if env.storage().instance().has(&DataKey::Owner) {
            panic!("Contract already initialized");
        }
        env.storage().instance().set(&DataKey::Owner, &owner);
        env.storage().instance().set(&DataKey::Token, &token);
        // Set TTL for instance storage
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Deposit USDC into the smart wallet.
    /// Requires authorization from the `from` address.
    /// The amount is transferred from `from` to this contract.
    pub fn deposit(env: Env, from: Address, amount: i128) {
        from.require_auth();

        if amount <= 0 {
            panic!("Amount must be positive");
        }

        let token_client = get_token_client(&env);
        let recipient = env.current_contract_address();

        // Transfer the specified amount from the sender to this contract
        token_client.transfer(&from, &recipient, &amount);

        // Extend TTL for instance storage on activity
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Withdraw USDC from the smart wallet to a specified address.
    /// Requires authorization from the contract owner.
    /// The amount is transferred from this contract to `to`.
    pub fn withdraw(env: Env, to: Address, amount: i128) {
        let owner = get_owner(&env);
        owner.require_auth(); // Only the owner can withdraw

        if amount <= 0 {
            panic!("Amount must be positive");
        }

        let token_client = get_token_client(&env);
        let contract_address = env.current_contract_address();

        // Check if the contract has enough balance
        let current_balance = token_client.balance(&contract_address);
        if current_balance < amount {
            panic!("Insufficient balance");
        }

        // Transfer the specified amount from this contract to the recipient
        token_client.transfer(&contract_address, &to, &amount);

        // Extend TTL for instance storage on activity
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Transfer USDC from the smart wallet to another address.
    /// Functionally similar to withdraw, but perhaps intended for different semantics.
    /// Requires authorization from the contract owner.
    pub fn transfer(env: Env, to: Address, amount: i128) {
        // Re-use withdraw logic for now, can be differentiated later if needed
        Self::withdraw(env, to, amount);
    }

    /// Get the current USDC balance held by the smart wallet contract.
    pub fn balance(env: Env) -> i128 {
        let token_client = get_token_client(&env);
        let contract_address = env.current_contract_address();
        token_client.balance(&contract_address)
    }

    /// Get the owner of the smart wallet.
    pub fn owner(env: Env) -> Address {
        get_owner(&env)
    }

    /// Get the USDC token address used by the smart wallet.
    pub fn token(env: Env) -> Address {
        env.storage().instance().get(&DataKey::Token).unwrap()
    }
}

mod test;

