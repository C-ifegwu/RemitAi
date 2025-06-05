#![cfg(test)]

use super::*;
use soroban_sdk::testutils::{Address as _, AuthorizedFunction, AuthorizedInvocation, Events as _};
use soroban_sdk::{symbol_short, Address, Env, String, IntoVal};

struct RegistryTest {
    env: Env,
    admin: Address,
    user1: Address,
    user2: Address,
    contract_address: Address,
    client: RegistryContractClient,
}

impl RegistryTest {
    fn setup() -> Self {
        let env = Env::default();
        env.mock_all_auths();

        let admin = Address::random(&env);
        let user1 = Address::random(&env);
        let user2 = Address::random(&env);

        let contract_address = env.register_contract(None, RegistryContract);
        let client = RegistryContractClient::new(&env, &contract_address);

        RegistryTest {
            env,
            admin,
            user1,
            user2,
            contract_address,
            client,
        }
    }
}

#[test]
fn test_initialize() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    // No direct way to check admin from outside easily without adding a get_admin function
    // We rely on admin functions failing/succeeding later
}

#[test]
fn test_initialize_no_admin() {
    let test = RegistryTest::setup();
    test.client.initialize(&None);
    // Check that admin functions fail if no admin is set
}

#[test]
#[should_panic(expected = "Contract already initialized")]
fn test_initialize_already_initialized() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    test.client.initialize(&Some(test.admin.clone()));
}

#[test]
fn test_register_resolve_lookup() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));

    let username1 = String::from_str(&test.env, "userone");
    test.client.register(&test.user1, &username1);

    // Verify resolution and lookup
    assert_eq!(test.client.resolve(&username1), test.user1);
    assert_eq!(test.client.lookup(&test.user1), username1);

    // Check auth for registration
    assert_eq!(
        test.env.auths(),
        vec![&test.env, (
            test.user1.clone(),
            AuthorizedInvocation {
                function: AuthorizedFunction::Contract((
                    test.contract_address.clone(),
                    symbol_short!("register"),
                    (test.user1.clone(), username1.clone()).into_val(&test.env)
                )),
                sub_invocations: std::vec![]
            }
        )]
    );

    // Check events
    let events = test.env.events().all();
    assert_eq!(events.len(), 1);
    assert_eq!(events.get(0).unwrap().topics.get(0).unwrap().unwrap_val(), symbol_short!("register").into_val(&test.env));
    assert_eq!(events.get(0).unwrap().topics.get(1).unwrap().unwrap_val(), test.user1.clone().into_val(&test.env));
    assert_eq!(events.get(0).unwrap().data.unwrap_val(), username1.into_val(&test.env));
}

#[test]
#[should_panic(expected = "Username already taken")]
fn test_register_username_taken() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));

    let username = String::from_str(&test.env, "takenuser");
    test.client.register(&test.user1, &username);
    // User2 tries to register the same username
    test.client.register(&test.user2, &username);
}

#[test]
#[should_panic(expected = "Address already registered")]
fn test_register_address_already_registered() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));

    test.client.register(&test.user1, &String::from_str(&test.env, "userone"));
    // User1 tries to register another username
    test.client.register(&test.user1, &String::from_str(&test.env, "anothername"));
}

#[test]
#[should_panic(expected = "Username must be between 3 and 32 characters")]
fn test_register_username_too_short() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    test.client.register(&test.user1, &String::from_str(&test.env, "us"));
}

#[test]
#[should_panic(expected = "Username must be between 3 and 32 characters")]
fn test_register_username_too_long() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    let long_name = "a".repeat(33);
    test.client.register(&test.user1, &String::from_str(&test.env, &long_name));
}

#[test]
fn test_unregister() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));

    let username = String::from_str(&test.env, "toberemoved");
    test.client.register(&test.user1, &username);

    // Verify registration exists
    assert_eq!(test.client.resolve(&username), test.user1);
    assert_eq!(test.client.lookup(&test.user1), username);

    // Unregister
    test.client.unregister(&test.user1);

    // Verify removal (expect panic on resolve/lookup)
    // Note: We need to catch the panic in the test
    let resolve_result = test.client.try_resolve(&username);
    assert!(resolve_result.is_err());

    let lookup_result = test.client.try_lookup(&test.user1);
    assert!(lookup_result.is_err());

    // Check auth
    assert_eq!(
        test.env.auths(),
        vec![&test.env, (
            test.user1.clone(),
            AuthorizedInvocation {
                function: AuthorizedFunction::Contract((
                    test.contract_address.clone(),
                    symbol_short!("unregister"),
                    (test.user1.clone(),).into_val(&test.env)
                )),
                sub_invocations: std::vec![]
            }
        )]
    );
}

#[test]
#[should_panic(expected = "Address not registered")]
fn test_unregister_not_registered() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    test.client.unregister(&test.user1);
}

#[test]
#[should_panic(expected = "Username not found")]
fn test_resolve_not_found() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    test.client.resolve(&String::from_str(&test.env, "nonexistent"));
}

#[test]
#[should_panic(expected = "Address not registered")]
fn test_lookup_not_found() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    test.client.lookup(&test.user1);
}

#[test]
fn test_admin_functions() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));

    let username = String::from_str(&test.env, "usertest");
    test.client.register(&test.user1, &username);

    // Admin removes the user
    test.client.admin_remove(&test.admin, &username);

    // Verify removal
    let resolve_result = test.client.try_resolve(&username);
    assert!(resolve_result.is_err());
    let lookup_result = test.client.try_lookup(&test.user1);
    assert!(lookup_result.is_err());

    // Set new admin
    let new_admin = Address::random(&test.env);
    test.client.set_admin(&test.admin, &new_admin);

    // Try removing another user with the new admin
    let username2 = String::from_str(&test.env, "user2test");
    test.client.register(&test.user2, &username2);
    test.client.admin_remove(&new_admin, &username2);
    let resolve_result2 = test.client.try_resolve(&username2);
    assert!(resolve_result2.is_err());
}

#[test]
#[should_panic(expected = "Caller is not the admin")]
fn test_admin_remove_not_admin() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    let username = String::from_str(&test.env, "usertest");
    test.client.register(&test.user1, &username);
    // User1 tries to remove
    test.client.admin_remove(&test.user1, &username);
}

#[test]
#[should_panic(expected = "Caller is not the admin")]
fn test_set_admin_not_admin() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    let new_admin = Address::random(&test.env);
    // User1 tries to set admin
    test.client.set_admin(&test.user1, &new_admin);
}

#[test]
#[should_panic(expected = "Username not found")]
fn test_admin_remove_username_not_found() {
    let test = RegistryTest::setup();
    test.client.initialize(&Some(test.admin.clone()));
    test.client.admin_remove(&test.admin, &String::from_str(&test.env, "nonexistent"));
}

