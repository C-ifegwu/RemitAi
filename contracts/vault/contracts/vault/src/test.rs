#![cfg(test)]

use super::*;
use soroban_sdk::testutils::{Address as _, AuthorizedFunction, AuthorizedInvocation, Ledger as _, Events as _};
use soroban_sdk::{symbol_short, token, Address, Env, IntoVal, Map, Val, Vec, BytesN};

// Helper to create a token contract
fn create_token_contract(env: &Env, admin: &Address) -> (Address, token::Client, token::StellarAssetClient) {
    let contract_address = env.register_stellar_asset_contract(admin.clone());
    let client = token::Client::new(env, &contract_address);
    let admin_client = token::StellarAssetClient::new(env, &contract_address);
    (contract_address, client, admin_client)
}

// Helper to create the vault contract
fn create_vault_contract(env: &Env) -> (Address, VaultContractClient) {
    let contract_id = env.register_contract(None, VaultContract);
    let client = VaultContractClient::new(env, &contract_id);
    (contract_id, client)
}

struct VaultTest {
    env: Env,
    admin: Address,
    user1: Address,
    user2: Address,
    token_address: Address,
    token_client: token::Client,
    token_admin_client: token::StellarAssetClient,
    contract_address: Address,
    client: VaultContractClient,
}

impl VaultTest {
    fn setup() -> Self {
        let env = Env::default();
        env.mock_all_auths();

        let admin = Address::random(&env);
        let user1 = Address::random(&env);
        let user2 = Address::random(&env);

        let (token_address, token_client, token_admin_client) = create_token_contract(&env, &admin);
        token_admin_client.mint(&admin, &1_000_000_000_000); // Mint funds for admin
        token_admin_client.mint(&user1, &1_000_000_000); // Mint 1000 USDC for user1
        token_admin_client.mint(&user2, &500_000_000);  // Mint 500 USDC for user2

        let (contract_address, client) = create_vault_contract(&env);

        VaultTest {
            env,
            admin,
            user1,
            user2,
            token_address,
            token_client,
            token_admin_client,
            contract_address,
            client,
        }
    }
}

const INITIAL_APY: u128 = 500; // 5.00%

#[test]
fn test_initialize() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    assert_eq!(test.client.get_apy_rate(), INITIAL_APY);
    // Check admin indirectly via admin functions
}

#[test]
#[should_panic(expected = "Contract already initialized")]
fn test_initialize_already_initialized() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
}

#[test]
fn test_deposit() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);

    let deposit_amount = 100_000_000; // 100 USDC
    let lock_duration = 90; // 90 days

    let vault_id = test.client.deposit(&test.user1, &deposit_amount, &lock_duration);
    assert_eq!(vault_id, 0);

    // Verify contract balance
    assert_eq!(test.token_client.balance(&test.contract_address), deposit_amount);
    // Verify user balance decreased
    assert_eq!(test.token_client.balance(&test.user1), 1_000_000_000 - deposit_amount);

    // Verify vault details
    let vault = test.client.get_vault(&vault_id);
    assert_eq!(vault.id, vault_id);
    assert_eq!(vault.owner, test.user1);
    assert_eq!(vault.amount, deposit_amount);
    assert_eq!(vault.apy_rate_at_lock, INITIAL_APY);
    assert_eq!(vault.status, VaultStatus::Locked);
    assert!(vault.start_ledger > 0);
    assert_eq!(vault.end_ledger, vault.start_ledger + (lock_duration as u32 * DAY_IN_LEDGERS));

     // Check auth
    assert_eq!(
        test.env.auths(),
        vec![&test.env, (
            test.user1.clone(),
            AuthorizedInvocation {
                function: AuthorizedFunction::Contract((
                    test.contract_address.clone(),
                    symbol_short!("deposit"),
                    (test.user1.clone(), deposit_amount, lock_duration).into_val(&test.env)
                )),
                sub_invocations: std::vec![AuthorizedInvocation {
                    function: AuthorizedFunction::Token((
                        test.token_address.clone(),
                        symbol_short!("transfer"),
                        (test.user1.clone(), test.contract_address.clone(), deposit_amount).into_val(&test.env)
                    )),
                    sub_invocations: std::vec![]
                }]
            }
        )]
    );
}

#[test]
#[should_panic(expected = "Amount must be positive")]
fn test_deposit_zero_amount() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    test.client.deposit(&test.user1, &0, &90);
}

#[test]
#[should_panic(expected = "Invalid lock duration")]
fn test_deposit_duration_too_short() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    test.client.deposit(&test.user1, &100_000_000, &(MIN_LOCK_DURATION_DAYS - 1));
}

#[test]
#[should_panic(expected = "Invalid lock duration")]
fn test_deposit_duration_too_long() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    test.client.deposit(&test.user1, &100_000_000, &(MAX_LOCK_DURATION_DAYS + 1));
}

#[test]
fn test_withdraw_unlocked() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);

    let deposit_amount = 100_000_000; // 100 USDC
    let lock_duration_days = 30;
    let vault_id = test.client.deposit(&test.user1, &deposit_amount, &lock_duration_days);

    // Simulate time passing beyond the lock duration
    let lock_duration_ledgers = lock_duration_days as u32 * DAY_IN_LEDGERS;
    test.env.ledger().with_mut(|li| {
        li.sequence_number += lock_duration_ledgers + 1; // Advance ledger sequence
    });

    // Withdraw
    test.client.withdraw(&test.user1, &vault_id);

    // Verify vault status
    let vault = test.client.get_vault(&vault_id);
    assert_eq!(vault.status, VaultStatus::Withdrawn);

    // Verify balances (user gets principal + yield)
    // Calculate expected yield (simplified linear for test)
    let principal_u256 = U256::from(deposit_amount);
    let rate_u256 = U256::from(INITIAL_APY);
    let duration_u256 = U256::from(lock_duration_ledgers);
    let day_in_ledgers_u256 = U256::from(DAY_IN_LEDGERS);
    let year_in_ledgers_u256 = day_in_ledgers_u256.mul(U256::from(365u64));
    let denominator_u256 = U256::from(INTEREST_RATE_DENOMINATOR);
    let numerator = principal_u256.mul(rate_u256).mul(duration_u256);
    let denominator = year_in_ledgers_u256.mul(denominator_u256);
    let expected_yield: i128 = numerator.div(denominator).try_into().unwrap_or(0);
    let expected_withdrawal = deposit_amount + expected_yield;

    assert_eq!(test.token_client.balance(&test.contract_address), 0); // Contract balance should be 0 after withdrawal
    assert_eq!(test.token_client.balance(&test.user1), 1_000_000_000 - deposit_amount + expected_withdrawal);

    // Check auth
    assert_eq!(
        test.env.auths(),
        vec![&test.env, (
            test.user1.clone(),
            AuthorizedInvocation {
                function: AuthorizedFunction::Contract((
                    test.contract_address.clone(),
                    symbol_short!("withdraw"),
                    (test.user1.clone(), vault_id).into_val(&test.env)
                )),
                sub_invocations: std::vec![AuthorizedInvocation {
                    function: AuthorizedFunction::Token((
                        test.token_address.clone(),
                        symbol_short!("transfer"),
                        (test.contract_address.clone(), test.user1.clone(), expected_withdrawal).into_val(&test.env)
                    )),
                    sub_invocations: std::vec![]
                }]
            }
        )]
    );
}

#[test]
#[should_panic(expected = "Vault is still locked")]
fn test_withdraw_still_locked() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);

    let deposit_amount = 100_000_000;
    let lock_duration_days = 30;
    let vault_id = test.client.deposit(&test.user1, &deposit_amount, &lock_duration_days);

    // Do not advance time
    test.client.withdraw(&test.user1, &vault_id);
}

#[test]
#[should_panic(expected = "Caller is not the vault owner")]
fn test_withdraw_not_owner() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);

    let deposit_amount = 100_000_000;
    let lock_duration_days = 30;
    let vault_id = test.client.deposit(&test.user1, &deposit_amount, &lock_duration_days);

    // Advance time
    test.env.ledger().with_mut(|li| {
        li.sequence_number += (lock_duration_days as u32 * DAY_IN_LEDGERS) + 1;
    });

    // User2 tries to withdraw
    test.client.withdraw(&test.user2, &vault_id);
}

#[test]
#[should_panic(expected = "Vault already withdrawn")]
fn test_withdraw_already_withdrawn() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);

    let deposit_amount = 100_000_000;
    let lock_duration_days = 30;
    let vault_id = test.client.deposit(&test.user1, &deposit_amount, &lock_duration_days);

    // Advance time & withdraw
    test.env.ledger().with_mut(|li| {
        li.sequence_number += (lock_duration_days as u32 * DAY_IN_LEDGERS) + 1;
    });
    test.client.withdraw(&test.user1, &vault_id);

    // Try to withdraw again
    test.client.withdraw(&test.user1, &vault_id);
}

#[test]
#[should_panic(expected = "Vault not found")]
fn test_withdraw_vault_not_found() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    test.client.withdraw(&test.user1, &999); // Non-existent ID
}

#[test]
fn test_get_user_vaults() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);

    let vault_id1 = test.client.deposit(&test.user1, &100_000_000, &30);
    let vault_id2 = test.client.deposit(&test.user2, &50_000_000, &60);
    let vault_id3 = test.client.deposit(&test.user1, &200_000_000, &90);

    let user1_vaults = test.client.get_user_vaults(&test.user1);
    assert_eq!(user1_vaults.len(), 2);
    assert!(user1_vaults.contains(vault_id1));
    assert!(user1_vaults.contains(vault_id3));

    let user2_vaults = test.client.get_user_vaults(&test.user2);
    assert_eq!(user2_vaults.len(), 1);
    assert!(user2_vaults.contains(vault_id2));
}

#[test]
fn test_admin_functions() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);

    // Set APY rate
    let new_apy = 600; // 6.00%
    test.client.set_apy_rate(&test.admin, &new_apy);
    assert_eq!(test.client.get_apy_rate(), new_apy);

    // Admin deposit
    let admin_deposit_amount = 500_000_000_000;
    test.client.admin_deposit(&test.admin, &test.admin, &admin_deposit_amount);
    assert_eq!(test.token_client.balance(&test.contract_address), admin_deposit_amount);

    // Admin withdraw
    let admin_withdraw_amount = 100_000_000_000;
    test.client.admin_withdraw(&test.admin, &test.user2, &admin_withdraw_amount);
    assert_eq!(test.token_client.balance(&test.contract_address), admin_deposit_amount - admin_withdraw_amount);
    assert_eq!(test.token_client.balance(&test.user2), 500_000_000 + admin_withdraw_amount);
}

#[test]
#[should_panic(expected = "Caller is not the admin")]
fn test_set_apy_rate_not_admin() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    test.client.set_apy_rate(&test.user1, &600);
}

#[test]
#[should_panic(expected = "Caller is not the admin")]
fn test_admin_deposit_not_admin() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    test.client.admin_deposit(&test.user1, &test.user1, &100_000_000);
}

#[test]
#[should_panic(expected = "Caller is not the admin")]
fn test_admin_withdraw_not_admin() {
    let test = VaultTest::setup();
    test.client.initialize(&test.admin, &test.token_address, &INITIAL_APY);
    test.client.admin_deposit(&test.admin, &test.admin, &1_000_000_000);
    test.client.admin_withdraw(&test.user1, &test.user2, &100_000_000);
}

