use jsonrpc_core::{IoHandler, Params, Value};
use std::sync::{Arc, Mutex};
use std::env;
use std::path::Path;
use dotenvy::from_path;

use crate::chain::Blockchain;
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
        let mut bc = blockchain_clone.lock().unwrap();
        bc.add_transaction(tx);
        Ok(Value::String("Transaction received".into()))
    });

    let blockchain_clone = blockchain.clone();
    io.add_sync_method("mineBlock", move |_| {
        let mut bc = blockchain_clone.lock().unwrap();
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

    let server = jsonrpc_http_server::ServerBuilder::new(io)
        .start_http(&bind_addr.parse().unwrap())
        .unwrap();

    println!("RPC server running on http://{}", bind_addr);
    server.wait();
}
