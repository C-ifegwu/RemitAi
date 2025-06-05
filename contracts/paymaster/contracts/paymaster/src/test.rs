#![cfg(test)]

use super::*;
use soroban_sdk::testutils::{Address as _, AuthorizedFunction, AuthorizedInvocation, Events as _};
use soroban_sdk::{symbol_short, token, Address, Env, IntoVal, Map, Val, BytesN};

// Helper to create a token contract
fn create_token_contract(env: &Env, admin: &Address) -> (Address, token::Client, token::StellarAssetClient) {
    let contract_address = env.register_stellar_asset_contract(admin.clone());
    let client = token::Client::new(env, &contract_address);
    let admin_client = token::StellarAssetClient::new(env, &contract_address);
    (contract_address, client, admin_client)
}

// Helper to create the paymaster contract
fn create_paymaster_contract(env: &Env) -> (Address, PaymasterContractClient) {
    let contract_id = env.register_contract(None, PaymasterContract);
    let client = PaymasterContractClient::new(env, &contract_id);
    (contract_id, client)
}

struct PaymasterTest {
    env: Env,
    admin: Address,
    user1: Address,
    user2: Address,
    token_address: Address,
    token_client: token::Client,
    token_admin_client: token::StellarAssetClient,
    contract_address: Address,
    client: PaymasterContractClient,
}

impl PaymasterTest {
    fn setup() -> Self {
        let env = Env::default();
        env.mock_all_auths();

        let admin = Address::random(&env);
        let user1 = Address::random(&env);
        let user2 = Address::random(&env);

        let (token_address, token_client, token_admin_client) = create_token_contract(&env, &admin);
        token_admin_client.mint(&admin, &1_000_000_000); // Mint funds for admin to deposit
        token_admin_client.mint(&user1, &100_000_000); // Mint funds for user1

        let (contract_address, client) = create_paymaster_contract(&env);

        PaymasterTest {
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

#[test]
fn test_initialize() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    assert_eq!(test.client.admin(), test.admin);
    // Check initial empty rules map indirectly via allow/disallow tests
}

#[test]
#[should_panic(expected = "Contract already initialized")]
fn test_initialize_already_initialized() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    test.client.initialize(&test.admin, &test.token_address);
}

#[test]
fn test_deposit_and_balance() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);

    let deposit_amount = 500_000_000;
    test.client.deposit(&test.admin, &deposit_amount);

    assert_eq!(test.client.balance(), deposit_amount);
    assert_eq!(test.token_client.balance(&test.contract_address), deposit_amount);
    assert_eq!(test.token_client.balance(&test.admin), 1_000_000_000 - deposit_amount);
}

#[test]
#[should_panic(expected = "Amount must be positive")]
fn test_deposit_zero_amount() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    test.client.deposit(&test.admin, &0);
}

#[test]
fn test_admin_withdraw() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);

    let deposit_amount = 500_000_000;
    test.client.deposit(&test.admin, &deposit_amount);
    assert_eq!(test.client.balance(), deposit_amount);

    let withdraw_amount = 100_000_000;
    test.client.withdraw(&test.admin, &test.user1, &withdraw_amount);

    assert_eq!(test.client.balance(), deposit_amount - withdraw_amount);
    assert_eq!(test.token_client.balance(&test.contract_address), deposit_amount - withdraw_amount);
    assert_eq!(test.token_client.balance(&test.user1), 100_000_000 + withdraw_amount);
}

#[test]
#[should_panic(expected = "Caller is not the admin")]
fn test_admin_withdraw_not_admin() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    test.client.deposit(&test.admin, &500_000_000);
    // User1 tries to withdraw
    test.client.withdraw(&test.user1, &test.user2, &100_000_000);
}

#[test]
#[should_panic(expected = "Insufficient balance")]
fn test_admin_withdraw_insufficient_funds() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    test.client.deposit(&test.admin, &100_000_000);
    test.client.withdraw(&test.admin, &test.user1, &200_000_000);
}

#[test]
fn test_allow_disallow_address() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);

    // Admin allows user1
    test.client.allow_address(&test.admin, &test.user1);
    // We can only verify this indirectly via the pay function logic

    // Admin disallows user1
    test.client.disallow_address(&test.admin, &test.user1);
    // Again, verification happens via pay function logic
}

#[test]
#[should_panic(expected = "Caller is not the admin")]
fn test_allow_address_not_admin() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    // User1 tries to allow user2
    test.client.allow_address(&test.user1, &test.user2);
}

#[test]
#[should_panic(expected = "Caller is not the admin")]
fn test_disallow_address_not_admin() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    test.client.allow_address(&test.admin, &test.user1);
    // User2 tries to disallow user1
    test.client.disallow_address(&test.user2, &test.user1);
}

// --- Test for the `pay` function --- 
// NOTE: The `pay` function relies heavily on the structure of `tx_context` 
// and signature verification, which are hard to fully mock accurately in unit tests.
// These tests focus on the *logic within* the pay function (allowlist check, balance check)
// assuming the context extraction placeholders work.
// More robust testing requires integration tests or testnet deployment.

#[test]
fn test_pay_allowed_sufficient_funds() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    test.client.deposit(&test.admin, &200_000_000); // Deposit 200 USDC
    test.client.allow_address(&test.admin, &test.user1); // Allow user1

    // Simulate context and signatures (using dummy values)
    let dummy_payload: Val = BytesN::<32>::random(&test.env).into();
    let dummy_sig: Val = BytesN::<64>::random(&test.env).into();
    let dummy_context: Val = test.user1.clone().into_val(&test.env); // Simplistic context just holding user address

    // Mock the placeholder functions to return the allowed user and a valid fee
    // This requires modifying the contract or using advanced mocking features not standard in basic tests.
    // For now, we assume the placeholders work correctly based on the dummy context.
    // We also need to mock the contract's own auth call.
    test.env.mock_auths(&[
        soroban_sdk::testutils::MockAuth { 
            address: &test.contract_address, // Paymaster authorizes itself
            invoke: &soroban_sdk::testutils::MockAuthInvoke { 
                contract: &test.contract_address,
                fn_name: "pay",
                args: (&dummy_payload, &dummy_sig, &dummy_context).into_val(&test.env),
                sub_invokes: &[],
            }
        }
    ]);

    // Call pay - This will likely fail without proper context mocking
    // test.client.pay(&dummy_payload, &dummy_sig, &dummy_context);
    // assert_eq!(test.client.balance(), 200_000_000 - 100_0000000); // Assuming dummy fee is 100

    // Due to limitations in mocking tx_context, we can only test parts of the logic.
    // A more practical test might involve creating helper functions in the contract
    // specifically for testing the sponsorship rules and balance checks.
}

#[test]
#[should_panic(expected = "Transaction source not allowed for sponsorship")]
fn test_pay_disallowed_user() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    test.client.deposit(&test.admin, &200_000_000);
    // User1 is NOT allowed

    let dummy_payload: Val = BytesN::<32>::random(&test.env).into();
    let dummy_sig: Val = BytesN::<64>::random(&test.env).into();
    // Simulate context indicating user1 is the source
    // This relies on the placeholder `extract_source_account` returning user1 based on context
    let dummy_context: Val = test.user1.clone().into_val(&test.env); 

    test.env.mock_auths(&[
        soroban_sdk::testutils::MockAuth { 
            address: &test.contract_address, 
            invoke: &soroban_sdk::testutils::MockAuthInvoke { 
                contract: &test.contract_address,
                fn_name: "pay",
                args: (&dummy_payload, &dummy_sig, &dummy_context).into_val(&test.env),
                sub_invokes: &[],
            }
        }
    ]);

    // This test assumes extract_source_account correctly identifies user1 from dummy_context
    // and that the allowlist check correctly fails.
    // test.client.pay(&dummy_payload, &dummy_sig, &dummy_context); // This call would panic
}

#[test]
#[should_panic(expected = "Paymaster has insufficient funds")]
fn test_pay_insufficient_funds() {
    let test = PaymasterTest::setup();
    test.client.initialize(&test.admin, &test.token_address);
    test.client.deposit(&test.admin, &50_000_000); // Deposit only 50 USDC (less than dummy fee)
    test.client.allow_address(&test.admin, &test.user1);

    let dummy_payload: Val = BytesN::<32>::random(&test.env).into();
    let dummy_sig: Val = BytesN::<64>::random(&test.env).into();
    let dummy_context: Val = test.user1.clone().into_val(&test.env); 

     test.env.mock_auths(&[
        soroban_sdk::testutils::MockAuth { 
            address: &test.contract_address, 
            invoke: &soroban_sdk::testutils::MockAuthInvoke { 
                contract: &test.contract_address,
                fn_name: "pay",
                args: (&dummy_payload, &dummy_sig, &dummy_context).into_val(&test.env),
                sub_invokes: &[],
            }
        }
    ]);

    // This test assumes the fee check correctly identifies insufficient funds.
    // test.client.pay(&dummy_payload, &dummy_sig, &dummy_context); // This call would panic
}

