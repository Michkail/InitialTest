use jsonrpc_core::{IoHandler, Params, Value};
use jsonrpc_http_server::ServerBuilder;
use std::env;
use std::path::Path;
use std::sync::{Arc, Mutex};
use serde_json::json;

use dotenvy::from_path;

use crate::chain::Blockchain;
use crate::crypto::generate_keypair;
use crate::transaction::Transaction;

pub fn start_rpc_server(blockchain: Arc<Mutex<Blockchain>>) {
    let env_path = Path::new("/app/.env");
    from_path(env_path).expect("Failed to load .env file");

    let host = env::var("RPC_HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
    let port = env::var("RPC_PORT").unwrap_or_else(|_| "3030".to_string());
    let bind_addr = format!("{}:{}", host, port);

    let mut io = IoHandler::new();

    let blockchain_clone = blockchain.clone();
    io.add_sync_method("submitTransaction", move |params: Params| {
        let tx: Transaction = params.parse().unwrap();

        if !tx.is_signature_valid() {
            return Ok(Value::String("Invalid signature".into()));
        }

        let mut bc = blockchain_clone.lock().unwrap();
        bc.add_transaction(tx);

        Ok(Value::String("Transaction added to mempool".into()))
    });

    let blockchain_clone = blockchain.clone();
    io.add_sync_method("mineBlock", move |_| {
        let mut bc = blockchain_clone.lock().unwrap();
    
        if !bc.is_chain_valid() {
            return Ok(serde_json::json!({
                "error": "Chain is invalid. Mining aborted."
            }));
        }
    
        let block = bc.mine_block();
        Ok(serde_json::to_value(block).unwrap())
    });

    let blockchain_clone = blockchain.clone();
    io.add_sync_method("getLatestBlock", move |_| {
        let bc = blockchain_clone.lock().unwrap();
        let block = bc.get_latest_block();
        Ok(serde_json::to_value(block).unwrap())
    });

    let blockchain_clone = blockchain.clone();
    io.add_sync_method("getAllBlocks", move |_| {
        let bc = blockchain_clone.lock().unwrap();
        Ok(serde_json::to_value(&bc.chain).unwrap())
    });

    io.add_sync_method("generateKeypair", |_| {
        let (public_key, private_key) = generate_keypair();
        Ok(serde_json::json!({
            "publicKey": public_key,
            "privateKey": private_key,
        }))
    });

    io.add_sync_method("isChainValid", move |_| {
        let bc = blockchain.lock().unwrap();
        Ok(json!(bc.is_chain_valid()))
    });    

    let server = ServerBuilder::new(io)
        .start_http(&bind_addr.parse().unwrap())
        .unwrap();

    println!("RPC server running on http://{}", bind_addr);
    server.wait();
}
