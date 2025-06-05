#![no_std]
use soroban_sdk::{
    contract, contractimpl, contracttype, symbol_short, token, Address, Env, Map, String, Val, Vec, U256
};

// --- Constants ---
const DAY_IN_LEDGERS: u32 = 17280; // Assuming 5 seconds per ledger
const MAX_LOCK_DURATION_DAYS: u64 = 365 * 2; // Max lock duration (e.g., 2 years)
const MIN_LOCK_DURATION_DAYS: u64 = 30;      // Min lock duration (e.g., 30 days)
const INTEREST_RATE_DENOMINATOR: u128 = 10_000; // For expressing APY (e.g., 500 = 5%)

// --- Data Structures ---

#[derive(Clone)]
#[contracttype]
pub enum DataKey {
    Admin,      // Address of the contract administrator
    Token,      // Address of the USDC token contract
    Vaults,     // Map<u64, Vault> - Stores individual vaults by ID
    NextVaultId, // u64 - Counter for the next vault ID
    APYRate,    // u128 - Current Annual Percentage Yield rate (e.g., 500 for 5.00%)
}

#[derive(Clone)]
#[contracttype]
pub enum VaultStatus {
    Locked,
    Unlocked, // Lock period ended, ready for withdrawal
    Withdrawn,
}

#[derive(Clone)]
#[contracttype]
pub struct Vault {
    id: u64,
    owner: Address,
    amount: i128,         // Principal amount deposited
    start_ledger: u32,    // Ledger number when the vault was created/locked
    end_ledger: u32,      // Ledger number when the vault unlocks
    apy_rate_at_lock: u128, // APY rate used for this specific vault
    status: VaultStatus,
}

// --- Helpers ---

fn get_admin(env: &Env) -> Address {
    env.storage().instance().get(&DataKey::Admin).unwrap()
}

fn is_admin(env: &Env, caller: &Address) -> bool {
    get_admin(env) == *caller
}

fn get_token_client(env: &Env) -> token::Client {
    let token_address = env.storage().instance().get(&DataKey::Token).unwrap();
    token::Client::new(env, &token_address)
}

fn get_next_vault_id(env: &Env) -> u64 {
    let key = DataKey::NextVaultId;
    let current_id: u64 = env.storage().instance().get(&key).unwrap_or(0);
    env.storage().instance().set(&key, &(current_id + 1));
    env.storage().instance().extend_ttl(100_000, 100_000); // Extend TTL for the counter
    current_id
}

fn get_vaults_map(env: &Env) -> Map<u64, Vault> {
    env.storage().persistent().get(&DataKey::Vaults).unwrap_or_else(|| Map::new(env))
}

fn save_vaults_map(env: &Env, vaults: &Map<u64, Vault>) {
    env.storage().persistent().set(&DataKey::Vaults, vaults);
    // Extend TTL for the vaults map itself
    env.storage().persistent().extend_ttl(&DataKey::Vaults, 100_000, 100_000);
}

// --- Contract ---

#[contract]
pub struct VaultContract;

#[contractimpl]
impl VaultContract {
    /// Initialize the vault contract.
    pub fn initialize(env: Env, admin: Address, token: Address, initial_apy_rate: u128) {
        if env.storage().instance().has(&DataKey::Admin) {
            panic!("Contract already initialized");
        }
        env.storage().instance().set(&DataKey::Admin, &admin);
        env.storage().instance().set(&DataKey::Token, &token);
        env.storage().instance().set(&DataKey::APYRate, &initial_apy_rate);
        env.storage().instance().set(&DataKey::NextVaultId, &0u64);
        // Initialize persistent storage for vaults map
        env.storage().persistent().set(&DataKey::Vaults, &Map::<u64, Vault>::new(&env));

        // Set TTLs
        env.storage().instance().extend_ttl(100_000, 100_000);
        env.storage().persistent().extend_ttl(&DataKey::Vaults, 100_000, 100_000);
    }

    /// Deposit funds into a new vault.
    /// `from`: The address depositing the funds.
    /// `amount`: The amount of USDC to deposit.
    /// `lock_duration_days`: The duration in days to lock the funds.
    pub fn deposit(env: Env, from: Address, amount: i128, lock_duration_days: u64) -> u64 {
        from.require_auth();

        if amount <= 0 {
            panic!("Amount must be positive");
        }
        if lock_duration_days < MIN_LOCK_DURATION_DAYS || lock_duration_days > MAX_LOCK_DURATION_DAYS {
            panic!("Invalid lock duration");
        }

        let token_client = get_token_client(&env);
        let contract_address = env.current_contract_address();

        // Transfer funds from user to contract
        token_client.transfer(&from, &contract_address, &amount);

        // Create and store the new vault
        let vault_id = get_next_vault_id(&env);
        let current_ledger = env.ledger().sequence();
        let end_ledger = current_ledger + (lock_duration_days as u32 * DAY_IN_LEDGERS);
        let current_apy_rate: u128 = env.storage().instance().get(&DataKey::APYRate).unwrap();

        let vault = Vault {
            id: vault_id,
            owner: from.clone(),
            amount,
            start_ledger: current_ledger,
            end_ledger,
            apy_rate_at_lock: current_apy_rate,
            status: VaultStatus::Locked,
        };

        let mut vaults = get_vaults_map(&env);
        vaults.set(vault_id, vault);
        save_vaults_map(&env, &vaults);

        env.events().publish((symbol_short!("deposit"), from, vault_id), amount);

        vault_id
    }

    /// Withdraw funds from an unlocked vault.
    /// `caller`: The address attempting the withdrawal (must be the vault owner).
    /// `vault_id`: The ID of the vault to withdraw from.
    pub fn withdraw(env: Env, caller: Address, vault_id: u64) {
        caller.require_auth();

        let mut vaults = get_vaults_map(&env);
        let mut vault = vaults.get(vault_id).expect("Vault not found");

        if vault.owner != caller {
            panic!("Caller is not the vault owner");
        }

        match vault.status {
            VaultStatus::Locked => {
                // Check if the lock period has ended
                if env.ledger().sequence() < vault.end_ledger {
                    panic!("Vault is still locked");
                }
                // Update status to Unlocked if lock period ended
                vault.status = VaultStatus::Unlocked;
            }
            VaultStatus::Unlocked => { /* Already unlocked, proceed */ }
            VaultStatus::Withdrawn => panic!("Vault already withdrawn"),
        }

        // Calculate yield
        let lock_duration_ledgers = vault.end_ledger.saturating_sub(vault.start_ledger);
        // Simple linear yield calculation (can be made more complex, e.g., compound)
        // yield = principal * rate * time
        // Using U256 for intermediate calculation to avoid overflow
        let principal_u256 = U256::from_u128(&env, vault.amount as u128);
        let rate_u256 = U256::from_u32(&env, vault.apy_rate_at_lock.try_into().unwrap());
        let duration_u256 = U256::from_u128(&env, lock_duration_ledgers as u128);
        let day_in_ledgers_u256 = U256::from_u32(&env, DAY_IN_LEDGERS as u32);
        let year_in_ledgers_u256 = day_in_ledgers_u256.mul(&U256::from_u32(&env, 365u32));
        let denominator_u256 = U256::from_u128(&env, INTEREST_RATE_DENOMINATOR);

        // yield = (principal * rate * duration_ledgers) / (year_in_ledgers * denominator)
        let numerator = principal_u256.mul(&rate_u256).mul(&duration_u256);
        let denominator = year_in_ledgers_u256.mul(&denominator_u256);
        let yield_amount: i128 = numerator.div(&denominator).to_u128().unwrap_or(0) as i128;

        let total_withdrawal_amount = vault.amount.checked_add(yield_amount).expect("Overflow calculating total withdrawal");

        // Transfer funds (principal + yield) back to owner
        let token_client = get_token_client(&env);
        let contract_address = env.current_contract_address();
        token_client.transfer(&contract_address, &vault.owner, &total_withdrawal_amount);

        // Update vault status to Withdrawn
        vault.status = VaultStatus::Withdrawn;
        vaults.set(vault_id, vault.clone());
        save_vaults_map(&env, &vaults);

        env.events().publish((symbol_short!("withdraw"), caller, vault_id), total_withdrawal_amount);
    }

    /// Get the details of a specific vault.
    pub fn get_vault(env: Env, vault_id: u64) -> Vault {
        get_vaults_map(&env).get(vault_id).expect("Vault not found")
    }

    /// Get a list of vault IDs owned by a specific address.
    pub fn get_user_vaults(env: Env, owner: Address) -> Vec<u64> {
        let vaults = get_vaults_map(&env);
        let mut user_vault_ids = Vec::new(&env);
        for (id, vault) in vaults.iter() {
            if vault.owner == owner {
                user_vault_ids.push_back(id);
            }
        }
        user_vault_ids
    }

    // --- Admin Functions ---

    /// Update the global APY rate for new deposits.
    pub fn set_apy_rate(env: Env, caller: Address, new_rate: u128) {
        caller.require_auth();
        if !is_admin(&env, &caller) {
            panic!("Caller is not the admin");
        }
        env.storage().instance().set(&DataKey::APYRate, &new_rate);
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Get the current global APY rate.
    pub fn get_apy_rate(env: Env) -> u128 {
        env.storage().instance().get(&DataKey::APYRate).unwrap()
    }

    /// Admin function to deposit funds into the contract (e.g., for yield payouts).
    pub fn admin_deposit(env: Env, caller: Address, from: Address, amount: i128) {
        caller.require_auth();
        if !is_admin(&env, &caller) {
            panic!("Caller is not the admin");
        }
        from.require_auth(); // Depositor must also authorize
        if amount <= 0 {
            panic!("Amount must be positive");
        }
        let token_client = get_token_client(&env);
        token_client.transfer(&from, &env.current_contract_address(), &amount);
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Admin function to withdraw surplus funds from the contract.
    pub fn admin_withdraw(env: Env, caller: Address, to: Address, amount: i128) {
        caller.require_auth();
        if !is_admin(&env, &caller) {
            panic!("Caller is not the admin");
        }
        if amount <= 0 {
            panic!("Amount must be positive");
        }
        let token_client = get_token_client(&env);
        let contract_address = env.current_contract_address();
        if token_client.balance(&contract_address) < amount {
            panic!("Insufficient balance");
        }
        token_client.transfer(&contract_address, &to, &amount);
        env.storage().instance().extend_ttl(100_000, 100_000);
    }
}

mod test;

