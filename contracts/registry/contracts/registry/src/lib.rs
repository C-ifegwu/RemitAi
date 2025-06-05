#![no_std]
use soroban_sdk::{contract, contractimpl, contracttype, symbol_short, Address, Env, String, Symbol, Val, Map};

#[derive(Clone)]
#[contracttype]
pub enum DataKey {
    Admin, // Address of the contract administrator (optional, for management)
    Usernames, // Map<String, Address> for username -> address mapping
    Addresses, // Map<Address, String> for address -> username mapping (reverse lookup)
}

fn get_admin(env: &Env) -> Option<Address> {
    env.storage().instance().get(&DataKey::Admin)
}

fn is_admin(env: &Env, caller: &Address) -> bool {
    if let Some(admin) = get_admin(env) {
        admin == *caller
    } else {
        false // No admin set, or caller is not admin
    }
}

#[contract]
pub struct RegistryContract;

#[contractimpl]
impl RegistryContract {
    /// Initialize the contract, optionally setting an administrator.
    pub fn initialize(env: Env, admin: Option<Address>) {
        if env.storage().instance().has(&DataKey::Usernames) {
            panic!("Contract already initialized");
        }
        if let Some(admin_addr) = admin {
            env.storage().instance().set(&DataKey::Admin, &admin_addr);
        }
        // Initialize the maps
        env.storage().persistent().set(&DataKey::Usernames, &Map::<String, Address>::new(&env));
        env.storage().persistent().set(&DataKey::Addresses, &Map::<Address, String>::new(&env));

        // Set TTL for instance and persistent storage
        env.storage().instance().extend_ttl(100_000, 100_000);
        env.storage().persistent().extend_ttl(&DataKey::Usernames, 100_000, 100_000);
        env.storage().persistent().extend_ttl(&DataKey::Addresses, 100_000, 100_000);
    }

    /// Register a username for the caller's address.
    /// Requires authorization from the caller.
    /// Panics if the username is already taken or the caller already has a username.
    pub fn register(env: Env, caller: Address, username: String) {
        caller.require_auth();

        let mut usernames: Map<String, Address> = env.storage().persistent().get(&DataKey::Usernames).unwrap();
        let mut addresses: Map<Address, String> = env.storage().persistent().get(&DataKey::Addresses).unwrap();

        // Basic validation for username (e.g., length, characters - can be expanded)
        if username.len() < 3 || username.len() > 32 {
            panic!("Username must be between 3 and 32 characters");
        }
        // Add more validation as needed (e.g., allowed characters)

        if usernames.contains_key(username.clone()) {
            panic!("Username already taken");
        }

        if addresses.contains_key(caller.clone()) {
            panic!("Address already registered with a username");
        }

        usernames.set(username.clone(), caller.clone());
        addresses.set(caller.clone(), username.clone());

        env.storage().persistent().set(&DataKey::Usernames, &usernames);
        env.storage().persistent().set(&DataKey::Addresses, &addresses);

        // Extend TTL for persistent storage on activity
        env.storage().persistent().extend_ttl(&DataKey::Usernames, 100_000, 100_000);
        env.storage().persistent().extend_ttl(&DataKey::Addresses, 100_000, 100_000);

        // Emit an event (optional)
        env.events().publish((symbol_short!("register"), caller), username);
    }

    /// Unregister the username associated with the caller's address.
    /// Requires authorization from the caller.
    pub fn unregister(env: Env, caller: Address) {
        caller.require_auth();

        let mut usernames: Map<String, Address> = env.storage().persistent().get(&DataKey::Usernames).unwrap();
        let mut addresses: Map<Address, String> = env.storage().persistent().get(&DataKey::Addresses).unwrap();

        if let Some(username) = addresses.get(caller.clone()) {
            addresses.remove(caller.clone());
            usernames.remove(username.clone());

            env.storage().persistent().set(&DataKey::Usernames, &usernames);
            env.storage().persistent().set(&DataKey::Addresses, &addresses);

            // Extend TTL for persistent storage on activity
            env.storage().persistent().extend_ttl(&DataKey::Usernames, 100_000, 100_000);
            env.storage().persistent().extend_ttl(&DataKey::Addresses, 100_000, 100_000);

            // Emit an event (optional)
            env.events().publish((symbol_short!("unreg"), caller), username);
        } else {
            panic!("Address not registered");
        }
    }

    /// Resolve an address by username.
    /// Returns the Address if found, otherwise panics.
    pub fn resolve(env: Env, username: String) -> Address {
        let usernames: Map<String, Address> = env.storage().persistent().get(&DataKey::Usernames).unwrap();
        usernames.get(username).expect("Username not found")
    }

    /// Look up a username by address (reverse lookup).
    /// Returns the username String if found, otherwise panics.
    pub fn lookup(env: Env, address: Address) -> String {
        let addresses: Map<Address, String> = env.storage().persistent().get(&DataKey::Addresses).unwrap();
        addresses.get(address).expect("Address not registered")
    }

    // --- Admin Functions (Optional) ---

    /// Set a new administrator for the contract.
    /// Requires authorization from the current admin.
    pub fn set_admin(env: Env, caller: Address, new_admin: Address) {
        if !is_admin(&env, &caller) {
            panic!("Caller is not the admin");
        }
        caller.require_auth();
        env.storage().instance().set(&DataKey::Admin, &new_admin);
        env.storage().instance().extend_ttl(100_000, 100_000);
    }

    /// Admin function to remove a registration.
    /// Requires authorization from the admin.
    pub fn admin_remove(env: Env, caller: Address, username_to_remove: String) {
         if !is_admin(&env, &caller) {
            panic!("Caller is not the admin");
        }
        caller.require_auth();

        let mut usernames: Map<String, Address> = env.storage().persistent().get(&DataKey::Usernames).unwrap();
        let mut addresses: Map<Address, String> = env.storage().persistent().get(&DataKey::Addresses).unwrap();

        if let Some(address_to_remove) = usernames.get(username_to_remove.clone()) {
            usernames.remove(username_to_remove.clone());
            addresses.remove(address_to_remove.clone());

            env.storage().persistent().set(&DataKey::Usernames, &usernames);
            env.storage().persistent().set(&DataKey::Addresses, &addresses);

            env.storage().persistent().extend_ttl(&DataKey::Usernames, 100_000, 100_000);
            env.storage().persistent().extend_ttl(&DataKey::Addresses, 100_000, 100_000);

            env.events().publish((symbol_short!("admin_rm"), username_to_remove), address_to_remove);
        } else {
            panic!("Username not found");
        }
    }
}

mod test;

