#![cfg(test)]

use super::*;
use soroban_sdk::testutils::{Address as _, AuthorizedFunction, AuthorizedInvocation};
use soroban_sdk::{symbol_short, token, Address, Env, IntoVal, vec};

// Corrected helper function signature
fn create_token_contract(env: &Env, admin: &Address) -> (Address, token::Client, token::StellarAssetClient) {
    let contract_address = env.register_stellar_asset_contract(admin.clone());
    let client = token::Client::new(env, &contract_address);
    let admin_client = token::StellarAssetClient::new(env, &contract_address);
    (contract_address, client, admin_client)
}

fn create_smart_wallet_contract(env: &Env) -> (Address, SmartWalletContractClient) {
    let contract_id = env.register_contract(None, SmartWalletContract);
    let client = SmartWalletContractClient::new(env, &contract_id);
    (contract_id, client)
}

struct SmartWalletTest {
    env: Env,
    admin: Address,
    user1: Address,
    user2: Address,
    token_admin_client: token::StellarAssetClient,
    token_address: Address,
    token_client: token::Client,
    contract_address: Address,
    client: SmartWalletContractClient,
}

impl SmartWalletTest {
    fn setup() -> Self {
        let env = Env::default();
        env.mock_all_auths(); // Make auth checks easier for testing

        let admin = Address::random(&env);
        let user1 = Address::random(&env);
        let user2 = Address::random(&env);

        // Create and setup the token contract (USDC)
        let (token_address, token_client, token_admin_client) = create_token_contract(&env, &admin);
        token_admin_client.mint(&user1, &1_000_000_000); // Mint 1000 USDC for user1
        token_admin_client.mint(&user2, &500_000_000);  // Mint 500 USDC for user2

        // Create and setup the smart wallet contract
        let (contract_address, client) = create_smart_wallet_contract(&env);

        SmartWalletTest {
            env,
            admin,
            user1,
            user2,
            token_admin_client,
            token_address,
            token_client,
            contract_address,
            client,
        }
    }
}

#[test]
fn test_initialize() {
    let test = SmartWalletTest::setup();

    // Initialize the contract
    test.client.initialize(&test.user1, &test.token_address);

    // Verify owner and token
    assert_eq!(test.client.owner(), test.user1);
    assert_eq!(test.client.token(), test.token_address);
}

#[test]
#[should_panic(expected = "Contract already initialized")]
fn test_initialize_already_initialized() {
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);
    // Try to initialize again
    test.client.initialize(&test.user2, &test.token_address);
}

#[test]
fn test_deposit() {
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);

    let deposit_amount = 100_000_000; // 100 USDC
    test.client.deposit(&test.user1, &deposit_amount);

    // Verify contract balance
    assert_eq!(test.client.balance(), deposit_amount);
    // Verify user1 balance decreased
    assert_eq!(test.token_client.balance(&test.user1), 1_000_000_000 - deposit_amount);

    // Check authorization
    assert_eq!(
        test.env.auths(),
        vec![&test.env, (
            test.user1.clone(),
            AuthorizedInvocation {
                function: AuthorizedFunction::Contract(( 
                    test.contract_address.clone(),
                    symbol_short!("deposit"),
                    (test.user1.clone(), deposit_amount).into_val(&test.env)
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
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);
    test.client.deposit(&test.user1, &0);
}

#[test]
#[should_panic(expected = "Amount must be positive")]
fn test_deposit_negative_amount() {
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);
    test.client.deposit(&test.user1, &-100);
}

#[test]
fn test_withdraw() {
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);

    let deposit_amount = 200_000_000; // 200 USDC
    test.client.deposit(&test.user1, &deposit_amount);
    assert_eq!(test.client.balance(), deposit_amount);

    let withdraw_amount = 50_000_000; // 50 USDC
    test.client.withdraw(&test.user2, &withdraw_amount);

    // Verify contract balance decreased
    assert_eq!(test.client.balance(), deposit_amount - withdraw_amount);
    // Verify user2 balance increased
    assert_eq!(test.token_client.balance(&test.user2), 500_000_000 + withdraw_amount);

    // Check authorization (only owner user1 should authorize withdraw)
     assert_eq!(
        test.env.auths(),
        vec![&test.env, (
            test.user1.clone(), // Owner authorizes
            AuthorizedInvocation {
                function: AuthorizedFunction::Contract(( 
                    test.contract_address.clone(),
                    symbol_short!("withdraw"),
                    (test.user2.clone(), withdraw_amount).into_val(&test.env)
                )),
                sub_invocations: std::vec![AuthorizedInvocation {
                    function: AuthorizedFunction::Token(( 
                        test.token_address.clone(),
                        symbol_short!("transfer"),
                        (test.contract_address.clone(), test.user2.clone(), withdraw_amount).into_val(&test.env)
                    )),
                    sub_invocations: std::vec![]
                }]
            }
        )]
    );
}

#[test]
#[should_panic(expected = "Insufficient balance")]
fn test_withdraw_insufficient_funds() {
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);

    let deposit_amount = 50_000_000; // 50 USDC
    test.client.deposit(&test.user1, &deposit_amount);

    let withdraw_amount = 100_000_000; // Try to withdraw 100 USDC
    test.client.withdraw(&test.user2, &withdraw_amount);
}

#[test]
#[should_panic(expected = "Amount must be positive")]
fn test_withdraw_zero_amount() {
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);
    test.client.deposit(&test.user1, &100_000_000);
    test.client.withdraw(&test.user2, &0);
}

#[test]
#[should_panic(expected = "Amount must be positive")]
fn test_withdraw_negative_amount() {
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);
    test.client.deposit(&test.user1, &100_000_000);
    test.client.withdraw(&test.user2, &-50);
}


#[test]
fn test_transfer() {
    // Transfer uses the same logic as withdraw in this implementation
    // So we just do a basic check, relying on withdraw tests for thoroughness
    let test = SmartWalletTest::setup();
    test.client.initialize(&test.user1, &test.token_address);

    let deposit_amount = 300_000_000; // 300 USDC
    test.client.deposit(&test.user1, &deposit_amount);
    assert_eq!(test.client.balance(), deposit_amount);

    let transfer_amount = 75_000_000; // 75 USDC
    test.client.transfer(&test.user2, &transfer_amount);

    // Verify contract balance decreased
    assert_eq!(test.client.balance(), deposit_amount - transfer_amount);
    // Verify user2 balance increased
    assert_eq!(test.token_client.balance(&test.user2), 500_000_000 + transfer_amount);
}

// Note: Auth testing for withdraw/transfer needs refinement if using
// env.mock_all_auths(). Specific auth mocking per call might be needed
// for more granular checks, but mock_all_auths simplifies basic functional tests.

